"""Agent-behavior eval — grades the LLM-DRIVEN decisions, not just the tool logic.

The deterministic runner (`runner.py`) tests the tool functions in isolation. THIS harness runs the
three Track-A demo prompts through the *real model* (Claude Code headless) and grades, with code:
  1. TOOL SELECTION  — did the agent call the right mcp__centerline__* tool, with the right borrower?
  2. §4.2 ON OUTPUT  — does the agent's actual narration contain credit-adjacent language? (the gap the
                       unit tests can't see — we scan the model's own reply with guards.scan_credit_language)
  3. FACT FAITHFULNESS — does the narration carry the correct figures (e.g. DSCR 1.03, the 78-day gap)?

The grader is deterministic Python (no LLM judge); the *thing being graded* is the model. Because the
model is non-deterministic, you can run each prompt N times and read the pass-rate (--runs N).

Run the real eval (you run this — it invokes Claude Code headless on YOUR account):
    PYTHONPATH=mcp python3 evals/agent_eval.py --runs 1

Prove the GRADING works without any model call (fixture-based, deterministic):
    PYTHONPATH=mcp python3 evals/agent_eval.py --selftest

Notes
-----
* Uses scoped `--allowedTools` (read-only centerline tools) — NOT `--dangerously-skip-permissions`.
* Needs the Claude Code CLI (`claude`) on PATH and the repo's `.mcp.json` + `centerline-plugin`.
* Known limit: the §4.2-on-output scan can't distinguish use from mention — if the agent *quotes* a
  blocked phrase while explaining it, that's a (rare, prompt-specific) false positive; flagged, not fatal.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "mcp"))
from centerline_mcp import guards  # noqa: E402  (reuse the SAME §4.2 scanner the server uses)

_REPORTS_DIR = os.path.join(_REPO, "reports")

_CENTERLINE_TOOLS = [
    "get_borrower_dossier",
    "get_loan_performance",
    "get_activity_log",
    "get_emails",
    "screen_and_finalize",
    "check_covenant_compliance",
    "detect_deterioration_signals",
    "measure_engagement_coverage",
    "assemble_watchlist",
    "run_evals",
]
_ALLOWED = ",".join(f"mcp__centerline__{t}" for t in _CENTERLINE_TOOLS)

# The three Track-A demo prompts + what a correct agentic response must exhibit.
PROMPTS = [
    {
        "id": "A1",
        "prompt": "Who in my portfolio needs attention this week? Rank them and show the facts behind "
        "each — don't characterize their credit, just the numbers and the gaps.",
        "required_tools": {"assemble_watchlist"},
        "borrower": None,
        "required_facts": ["meridian"],
        "order_before": ("meridian", "crestwood"),  # Meridian must be discussed before Crestwood
    },
    {
        "id": "A2",
        "prompt": "Is Meridian covenant-compliant as of the latest month? Show DSCR against the covenant "
        "minimum with the cushion, and whether the reported status matches the trend.",
        "required_tools": {"check_covenant_compliance"},
        "bonus_tools": {"detect_deterioration_signals"},
        "borrower": "meridian",
        "required_facts": ["1.03", "breach"],
        "order_before": None,
    },
    {
        "id": "A3",
        "prompt": "Which of my distressed borrowers have I actually gone quiet on? For Meridian, count days "
        "since the last real two-way contact — a one-way notice or a missed call doesn't count.",
        "required_tools": {"measure_engagement_coverage"},
        "borrower": "meridian",
        "required_facts": ["78"],
        "order_before": None,
    },
]


def _claude_cmd(prompt, model=None, mcp_config=None):
    cmd = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "stream-json",
        "--verbose",
        "--mcp-config",
        mcp_config or os.path.join(_REPO, ".mcp.json"),
        "--plugin-dir",
        os.path.join(_REPO, "centerline-plugin"),
        "--strict-mcp-config",
        "--setting-sources",
        "project",
        "--allowedTools",
        _ALLOWED,
    ]
    if model:
        cmd += ["--model", model]
    return cmd


def _parse_stream(stdout):
    """Return (tool_calls, final_text). tool_calls = [{name, input}] with the mcp__centerline__ prefix stripped."""
    tool_calls, texts, final = [], [], None
    for ln in stdout.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            m = json.loads(ln)
        except json.JSONDecodeError:
            continue
        t = m.get("type")
        if t == "assistant":
            for b in m.get("message", {}).get("content", []):
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use":
                    name = b.get("name", "")
                    tool_calls.append({"name": name.replace("mcp__centerline__", ""), "input": b.get("input", {})})
                elif b.get("type") == "text":
                    texts.append(b.get("text", ""))
        elif t == "result":
            final = m.get("result")
    final_text = final if final else "\n".join(texts)
    return tool_calls, (final_text or "")


def _grade(spec, tool_calls, final_text):
    called = {c["name"] for c in tool_calls}
    checks = {}

    # 1. tool selection (+ borrower arg)
    missing = spec["required_tools"] - called
    sel_ok = not missing
    if sel_ok and spec.get("borrower"):
        b = spec["borrower"]
        sel_ok = any(
            b in json.dumps(c.get("input", {})).lower() for c in tool_calls if c["name"] in spec["required_tools"]
        )
    checks["tool_selection"] = {
        "ok": sel_ok,
        "called": sorted(called),
        "missing_required": sorted(missing),
        "bonus_called": sorted(spec.get("bonus_tools", set()) & called),
    }

    # 2. §4.2 on the agent's OWN narration (the gap unit tests can't see)
    hits = guards.scan_credit_language(final_text)
    checks["section_4_2_output"] = {"ok": not hits, "hits": sorted(set(hits))}

    # 3. fact faithfulness
    lo = final_text.lower()
    missing_facts = [f for f in spec["required_facts"] if f.lower() not in lo]
    fact_ok = not missing_facts
    if spec.get("order_before"):
        a, b = spec["order_before"]
        fact_ok = fact_ok and (a in lo and b in lo and lo.index(a) < lo.index(b))
    checks["fact_faithfulness"] = {"ok": fact_ok, "missing_facts": missing_facts}

    checks["passed"] = all(c["ok"] for c in checks.values() if isinstance(c, dict) and "ok" in c)
    return checks


def _run_prompt(spec, timeout, model=None, mcp_config=None):
    try:
        proc = subprocess.run(
            _claude_cmd(spec["prompt"], model, mcp_config), cwd=_REPO, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "tool_calls": [], "final_text": "", "checks": {"passed": False}}
    except FileNotFoundError:
        return {
            "error": "claude CLI not found on PATH",
            "tool_calls": [],
            "final_text": "",
            "checks": {"passed": False},
        }
    tool_calls, final_text = _parse_stream(proc.stdout)
    if not tool_calls and not final_text:
        return {
            "error": f"no parseable output (exit {proc.returncode}); stderr: {proc.stderr[-300:]}",
            "tool_calls": [],
            "final_text": "",
            "checks": {"passed": False},
        }
    return {
        "error": None,
        "tool_calls": tool_calls,
        "final_text": final_text,
        "checks": _grade(spec, tool_calls, final_text),
    }


# --- fixture for --selftest: a synthetic "good" A2 trace, to prove the grader works with no model call ---
_FIXTURE_STREAM = "\n".join(
    [
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "t1",
                            "name": "mcp__centerline__check_covenant_compliance",
                            "input": {"borrower_name": "Meridian"},
                        }
                    ]
                },
            }
        ),
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "t2",
                            "name": "mcp__centerline__detect_deterioration_signals",
                            "input": {"borrower_name": "Meridian"},
                        }
                    ]
                },
            }
        ),
        json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "result": "Meridian's DSCR is 1.03 vs the 1.20 covenant minimum (cushion -0.17) -> Covenant Breach "
                "(loan_performance, 2025-05). The reported status lagged the declining trend.",
            }
        ),
    ]
)


def _selftest():
    spec = PROMPTS[1]  # A2
    tc, ft = _parse_stream(_FIXTURE_STREAM)
    checks = _grade(spec, tc, ft)
    print("SELF-TEST (fixture, no model call):")
    print("  parsed tool calls:", [c["name"] for c in tc])
    print("  §4.2 hits in narration:", checks["section_4_2_output"]["hits"])
    print("  checks:", json.dumps({k: v for k, v in checks.items()}, default=str))
    # also prove the §4.2 scan CATCHES a bad narration
    bad_checks = _grade(spec, tc, ft + " This borrower is high credit risk and likely to default.")
    print("  negative (credit-adjacent narration) -> §4.2 ok should be False:", bad_checks["section_4_2_output"]["ok"])
    good = checks["passed"] and (bad_checks["section_4_2_output"]["ok"] is False)
    print("SELF-TEST", "PASSED" if good else "FAILED")
    return 0 if good else 1


def _write_report(results, runs, model=None):
    # versioned history: reports/agent_eval/agent_eval-<UTC stamp>.md + a stable latest.md pointer
    out_dir = os.path.join(_REPORTS_DIR, "agent_eval")
    os.makedirs(out_dir, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y%m%d-%H%M%SZ")  # sortable -> "latest" == max(filename)
    human = now.strftime("%Y-%m-%d %H:%M UTC")
    L = [
        "# Agent-behavior eval (the LLM-driven decisions)",
        "",
        f"_Run {human} · model: {model or 'CLI default'} · {runs} run(s)/prompt · via `evals/agent_eval.py`._",
        "",
        "Grades the **model's** decisions with deterministic code: tool selection, §4.2 on the agent's own "
        "narration, and fact faithfulness. Complements `runner.py` (which unit-tests the tool logic).",
        "",
        "| Prompt | Runs passed | Tool selection | §4.2 on output | Facts |",
        "|---|---|---|---|---|",
    ]
    for pid, runs_list in results.items():
        npass = sum(1 for r in runs_list if r["checks"].get("passed"))

        def frac(key):
            return f"{sum(1 for r in runs_list if r['checks'].get(key, {}).get('ok'))}/{len(runs_list)}"

        L.append(
            f"| **{pid}** | {npass}/{len(runs_list)} | {frac('tool_selection')} | {frac('section_4_2_output')} | {frac('fact_faithfulness')} |"
        )
    L += ["", "## Per-run detail (with the model's captured analysis)", ""]
    trans_dir = os.path.join(_REPO, "traces", "agent_eval", stamp)
    os.makedirs(trans_dir, exist_ok=True)
    for pid, runs_list in results.items():
        L.append(f"### {pid}")
        for i, r in enumerate(runs_list, 1):
            if r["error"]:
                L.append(f"- run {i}: ⚠️ ERROR — {r['error']}")
                continue
            c = r["checks"]
            L.append(
                f"- run {i}: {'✅ PASS' if c['passed'] else '❌ FAIL'} · "
                f"tools={c['tool_selection']['called']} · "
                f"§4.2 hits={c['section_4_2_output']['hits']} · "
                f"missing facts={c['fact_faithfulness']['missing_facts']}"
            )
            # the model's actual analysis text (what was graded) — inline + a raw transcript on disk
            narration = (r.get("final_text") or "").strip()
            with open(os.path.join(trans_dir, f"{pid}-run{i}.md"), "w", encoding="utf-8") as fh:
                fh.write(f"# {pid} run {i}\n\ntools: {c['tool_selection']['called']}\n\n---\n\n{narration}\n")
            L.append("")
            L.append(f"  <details><summary>run {i} — model's analysis</summary>\n")
            L.append("  > " + (narration.replace("\n", "\n  > ") if narration else "_(empty)_"))
            L.append("\n  </details>")
        L.append("")
    L += [
        "## Honest limits",
        "",
        "- **Non-deterministic** — the model can vary run to run; read the pass-rate, run with `--runs N`.",
        "- **§4.2 use-vs-mention** — the scanner flags a blocked phrase even if the agent is *quoting* it to "
        "explain a block; rare for A1/A2/A3, noted not fatal.",
        "- **Small prompt set** — the three Track-A prompts; Track-B prompts (emails/memos) will add a "
        "generative-quality layer that may warrant an LLM-as-judge (a signal, not ground truth).",
        "",
    ]
    body = "\n".join(L) + "\n"
    ts_path = os.path.join(out_dir, f"agent_eval-{stamp}.md")
    latest_path = os.path.join(out_dir, "latest.md")
    for p in (ts_path, latest_path):
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
    return ts_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1, help="runs per prompt (model is non-deterministic)")
    ap.add_argument("--timeout", type=int, default=240, help="per-run timeout (seconds)")
    ap.add_argument("--model", default=None, help="model override, e.g. claude-sonnet-4-6 (CI uses Sonnet for cost)")
    ap.add_argument(
        "--mcp-config", default=None, help="path to an MCP config (default: repo .mcp.json; CI: evals/ci.mcp.json)"
    )
    ap.add_argument(
        "--min-pass-rate",
        type=float,
        default=1.0,
        help="exit 0 if overall pass-rate >= this (default 1.0 strict; CI may relax for non-determinism)",
    )
    ap.add_argument("--selftest", action="store_true", help="grade a fixture trace (no model call)")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    if args.model:
        print(f"(model override: {args.model})")
    results = {}
    for spec in PROMPTS:
        runs_list = []
        for i in range(args.runs):
            print(f"[{spec['id']}] run {i + 1}/{args.runs} ...", flush=True)
            r = _run_prompt(spec, args.timeout, args.model, args.mcp_config)
            c = r["checks"]
            tag = "ERROR:" + str(r["error"]) if r["error"] else ("PASS" if c.get("passed") else "FAIL")
            print(f"   -> {tag}")
            runs_list.append(r)
        results[spec["id"]] = runs_list

    path = _write_report(results, args.runs, args.model)
    total_runs = sum(len(v) for v in results.values())
    total_pass = sum(1 for v in results.values() for r in v if r["checks"].get("passed"))
    rate = (total_pass / total_runs) if total_runs else 0.0
    print(
        f"\n{total_pass}/{total_runs} runs passed (rate {rate:.2f}, threshold {args.min_pass_rate:.2f}) "
        f"— wrote {os.path.relpath(path, _REPO)} (+ reports/agent_eval/latest.md)"
    )
    return 0 if rate >= args.min_pass_rate else 1


if __name__ == "__main__":
    sys.exit(main())
