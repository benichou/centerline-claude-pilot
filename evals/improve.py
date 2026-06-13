"""Improvement analyst — reads the agent-eval report HISTORY and writes an ADVISORY improvements report.

"AI flags, human decides" in its purest form: this script NEVER edits code, skills, guards, or eval cases.
It only writes a timestamped markdown report to reports/improvements/ describing what failed (or recurs),
the root cause, and a proposed PROMPT/SKILL change for a human to apply by hand. It runs Claude Code headless
with READ-ONLY tools (so the analyst can inspect the skill library) and captures its prose.

History-aware: it feeds the LATEST eval report in full + summaries of the prior runs, so the analyst can tell
a one-off from a RECURRING/flaky pattern (e.g. "A3 fails ~1 in 3 nights on the same phrasing") — worth fixing
even when the latest run happened to pass.

Run (real):  python3 evals/improve.py [--model claude-sonnet-4-6] [--max-history 8]
Single file: python3 evals/improve.py --source reports/agent_eval/latest.md
Dry run:     python3 evals/improve.py --dry-run     # build the input + write a stub report, NO model call
"""

import argparse
import datetime
import glob
import json
import os
import subprocess
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUT_DIR = os.path.join(_REPO, "reports", "improvements")
_HISTORY_DIR = os.path.join(_REPO, "reports", "agent_eval")

# Read-only tools so the analyst can inspect the skill library; it has NO write/edit/MCP access.
_ALLOWED = "Read,Grep,Glob"

ANALYST_PROMPT = """You are a compliance-aware engineering analyst for the Centerline Bank Claude pilot \
(a synthetic-data demo). You are reviewing the agent-behavior eval (Layer 3) HISTORY to propose improvements \
to the COMPLIANCE SKILL LIBRARY. Your output is an ADVISORY report only — a human applies anything approved.

HARD RULES (do not violate):
- Propose changes ONLY to the prompt/skill library (centerline-plugin/skills/**/SKILL.md) or the demo prompts.
- NEVER propose editing or weakening the compliance guards (mcp/centerline_mcp/guards.py, the deterministic \
logic in mcp/centerline_mcp/core.py), the MCP tools, or the eval answer key (evals/cases/, evals/*.py). \
If a failure seems to require touching those, FLAG it for human attention with your reasoning instead of \
proposing the change — weakening a guard or a test to make the eval pass is forbidden.
- Distinguish a real behavior problem from an eval false positive (e.g. a §4.2 'use-vs-mention' hit where the \
model merely named a forbidden word in a disclaimer). Say which it is.
- Use the PRIOR-RUN summaries to judge whether a failure is a one-off or RECURRING across runs.
- Advisory only; phrase it so a non-engineer compliance reviewer can follow it. Do NOT manufacture suggestions \
or churn compliance prompts without cause — a clean library with nothing concrete to fix is a valid outcome.

You have READ-ONLY tools — inspect centerline-plugin/skills/ to ground your suggestions in the actual files.

Output ONLY a markdown report with these sections:
1. **Summary** — a table: | Finding | Type (must-fix / proactive) | Real issue or eval artifact? | Recurring? | Proposed change (file) |
2. **Must-fix** — findings tied to an actual FAILED or FLAKY run (include runs that failed even though the job \
passed the threshold, and patterns that RECUR across the prior runs). Per finding: **Finding**, **Root cause**, \
**Proposed skill/prompt change** (exact SKILL.md + the concrete wording to add/adjust), **Compliance rationale \
(§)**, **Why this does NOT weaken any guard or test**. If there are none, write "None — no failed or recurring runs."
3. **Proactive (optional)** — concrete hardening only (ambiguous skill wording, a coverage gap, a near-miss). \
SEVERITY-GATED: include an item ONLY if it is specific and actionable. If nothing concrete, write \
"No proactive items — the skill library looks sound for what the eval covers."
4. If there are NO must-fix findings AND no concrete proactive items, state plainly at the top: \
"No action needed — latest run clean, no recurring failures, nothing concrete to harden."

Here is the eval-report history to analyze (latest in full, then prior-run summaries, newest first):

"""


def _claude_cmd(prompt, model=None):
    cmd = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--allowedTools",
        _ALLOWED,
        "--setting-sources",
        "project",
    ]
    if model:
        cmd += ["--model", model]
    return cmd


def _summary_head(text):
    """The part of an eval report BEFORE the per-run narration (header + the runs-passed table) — compact."""
    return text.split("## Per-run detail")[0].rstrip()


def _build_input(source, history_dir, max_history):
    """Return (input_text, n_reports, source_label, err). Single-file mode if --source given; else history mode."""
    if source:
        if not os.path.exists(source):
            return None, 0, None, f"source report not found: {source}"
        return open(source, encoding="utf-8").read(), 1, os.path.relpath(source, _REPO), None

    files = sorted(glob.glob(os.path.join(history_dir, "agent_eval-*.md")), reverse=True)
    if not files:
        rel = os.path.relpath(history_dir, _REPO)
        return None, 0, None, f"no timestamped agent-eval reports in {rel} — run evals/agent_eval.py first"
    files = files[:max_history]
    parts = ["## LATEST RUN — full report\n\n" + open(files[0], encoding="utf-8").read()]
    if len(files) > 1:
        parts.append("\n\n## PRIOR RUNS — summaries (newest first), to spot RECURRING/flaky patterns\n")
        for f in files[1:]:
            parts.append(f"\n### {os.path.basename(f)}\n\n{_summary_head(open(f, encoding='utf-8').read())}")
    label = f"{os.path.relpath(history_dir, _REPO)} (latest {len(files)} report(s))"
    return "\n".join(parts), len(files), label, None


def _analyze(input_text, model, timeout):
    prompt = ANALYST_PROMPT + input_text
    try:
        proc = subprocess.run(_claude_cmd(prompt, model), cwd=_REPO, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return None, "claude CLI not found on PATH"
    except subprocess.TimeoutExpired:
        return None, "timeout"
    out = proc.stdout.strip()
    try:
        return json.loads(out).get("result", "").strip(), None
    except json.JSONDecodeError:
        for ln in reversed(out.splitlines()):
            try:
                return json.loads(ln).get("result", "").strip(), None
            except json.JSONDecodeError:
                continue
        return (out or None), (None if out else f"no output (exit {proc.returncode}); stderr: {proc.stderr[-300:]}")


def _write(report_body, model, source_label):
    os.makedirs(_OUT_DIR, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y%m%d-%H%M%SZ")
    header = (
        f"# Proposed improvements (advisory — AI flags, human decides)\n\n"
        f"_Generated {now.strftime('%Y-%m-%d %H:%M UTC')} · model: {model or 'CLI default'} · "
        f"source: `{source_label}` · via `evals/improve.py`._\n\n"
        f"> **Advisory only.** Nothing here is applied automatically. A human reviews and, if approved, edits "
        f"the skill library by hand (through the normal pre-commit + eval-validation gate). This analyst has "
        f"**no write access** to code, guards, or the eval answer key.\n\n---\n\n"
    )
    body = header + report_body + "\n"
    ts_path = os.path.join(_OUT_DIR, f"improvements-{stamp}.md")
    latest_path = os.path.join(_OUT_DIR, "latest.md")
    for p in (ts_path, latest_path):
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
    return ts_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=None, help="analyze a single eval report instead of the history")
    ap.add_argument("--history-dir", default=_HISTORY_DIR, help="dir of timestamped agent-eval reports")
    ap.add_argument("--max-history", type=int, default=8, help="how many recent eval reports to consider")
    ap.add_argument("--model", default=None, help="model override, e.g. claude-sonnet-4-6")
    ap.add_argument("--timeout", type=int, default=300, help="per-call timeout (seconds)")
    ap.add_argument("--dry-run", action="store_true", help="build the input + write a stub report (no model call)")
    args = ap.parse_args()

    input_text, n, source_label, err = _build_input(args.source, args.history_dir, args.max_history)
    if err:
        print(err, file=sys.stderr)
        return 1

    if args.dry_run:
        stub = (
            "_(dry run — no model call)_\n\n"
            f"Reports considered: {n}. Input length: {len(ANALYST_PROMPT) + len(input_text)} chars. "
            f"Read-only tools: {_ALLOWED}."
        )
        path = _write(stub, args.model, source_label)
        print(f"dry-run wrote {os.path.relpath(path, _REPO)} (+ reports/improvements/latest.md)")
        return 0

    body, aerr = _analyze(input_text, args.model, args.timeout)
    if aerr or not body:
        print(f"analysis failed: {aerr}", file=sys.stderr)
        return 1
    path = _write(body, args.model, source_label)
    print(f"wrote {os.path.relpath(path, _REPO)} (+ reports/improvements/latest.md) — analyzed {n} eval report(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
