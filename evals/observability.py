"""Observability report generator — writes reports/observability.md.

Combines three real signals into a per-prompt scorecard (no fabricated dashboards):
  - T3 expected-trace: the skills / MCP tools / guards each demo prompt SHOULD exercise (authored here),
  - T1/T2 eval results: the source-grounded case pass/fail from evals/runner.py (the live tool logic),
  - the run-trace ledger: what the PreToolUse hook actually recorded (honest about its limits).

Run:  PYTHONPATH=mcp python3 evals/observability.py
"""

import datetime
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "mcp"))
sys.path.insert(0, os.path.join(_REPO, "evals"))

from runner import run_all  # noqa: E402

_REPORTS_DIR = os.path.join(_REPO, "reports")
_LEDGER = os.path.join(_REPO, "traces", "run-ledger.log")

# T3 expected-trace: the orchestration each demo prompt should exercise (catches wrong/skipped steps).
_PROMPT_SPECS = [
    {
        "id": "A1",
        "title": "Who needs attention this week?",
        "skills": ["assembling-watchlist-triage"],
        "tools": [
            "assemble_watchlist (composes check_covenant_compliance + detect_deterioration_signals + measure_engagement_coverage)"
        ],
        "guards": ["§2.1 strip", "§5 gate", "screen_and_finalize (§4.2 + footer + §4.3)"],
        "reliability": "Grounded — every line cited; ranking is deterministic, not a credit rating",
    },
    {
        "id": "A2",
        "title": "Is Meridian covenant-compliant — cushion and trend?",
        "skills": ["checking-covenant-compliance", "detecting-deterioration-signals"],
        "tools": ["check_covenant_compliance", "detect_deterioration_signals"],
        "guards": ["§2.1 strip", "§5 gate", "screen_and_finalize (§4.2 + footer + §4.3)"],
        "reliability": "Grounded — math computed in code; status-vs-trend mislabel surfaced",
    },
    {
        "id": "A3",
        "title": "Which distressed borrowers have I gone quiet on? ★",
        "skills": ["measuring-engagement-coverage"],
        "tools": ["measure_engagement_coverage"],
        "guards": ["§2.1 strip", "§5 gate", "screen_and_finalize (§4.2 + footer + §4.3)"],
        "reliability": "Grounded — one-way notices excluded; 78d vs naive 33d",
    },
    {
        "id": "B1",
        "title": "Prep me for Crestwood — retention radar ★ (the inverse of early-warning)",
        "skills": ["flagging-renewal-and-retention", "building-client-360"],
        "tools": ["flag_renewal_and_retention (reuses check_covenant_compliance + detect_deterioration_signals)"],
        "guards": ["§2.1 strip", "§5 gate", "screen_and_finalize (§4.2 + footer + §4.3)"],
        "reliability": "Grounded — facts + 'engage'; never a rate (pricing committee owns that); §4.1 for automation",
    },
    {
        "id": "B2",
        "title": "Meridian covenant-package intake (doc-intel)",
        "skills": ["reviewing-covenant-package"],
        "tools": [
            "cross_validate_covenant + review_package (deterministic — graded here); classify_document + extract_document_fields (model/API — graded by the live agent-eval + unit tests)"
        ],
        "guards": ["§2.1 guarantor refusal (pre-screen)", "screen_and_finalize (§4.2 + footer + §4.3)"],
        "reliability": "Partial — certified-vs-recomputed mismatch + missing/unsigned/withheld surfaced; extraction is model-driven",
    },
    {
        "id": "B3",
        "title": "Reconcile Arcadia emails vs the CRM log ★ (close-the-loop)",
        "skills": ["detecting-cross-source-discrepancies", "verifying-commitment-fulfillment"],
        "tools": ["get_relationship_timeline", "get_emails", "get_activity_log", "detect_deterioration_signals"],
        "guards": ["§2.1 redaction", "§5 gate", "scribe-not-author (§4.2)", "screen_and_finalize"],
        "reliability": "Partial — synthesis kept honest by grounding + scribe-not-author + footer (not pretend-deterministic)",
    },
    {
        "id": "B4",
        "title": "Summit annual relationship-review memo (decomposed §4.2)",
        "skills": ["drafting-relationship-review-memos", "building-client-360"],
        "tools": [
            "get_loan_performance",
            "check_covenant_compliance",
            "detect_deterioration_signals",
            "get_activity_log",
        ],
        "guards": ["RM-authored assessment required (§4.2 origination)", "screen_and_finalize (§4.2 + footer + §4.3)"],
        "reliability": "T4 (generative) — rubric + HITL: facts cited, assessment RM-authored & non-empty; no deterministic golden case",
    },
    {
        "id": "foundation",
        "title": "Cross-cutting compliance guards (every prompt routes through these)",
        "skills": ["redacting-restricted-fields", "screening-and-gating-output", "assessing-output-reliability"],
        "tools": ["(server-side guards) + screen_and_finalize"],
        "guards": ["§2.1 strip", "§5 gate", "guarantor refusal", "§4.2 output block", "reliability footer"],
        "reliability": "n/a — these ARE the reliability/compliance layer",
    },
]


def _ledger_summary():
    if not os.path.exists(_LEDGER):
        return "no ledger yet (`traces/run-ledger.log` absent — run a Code session to populate it)"
    with open(_LEDGER, encoding="utf-8") as fh:
        n = sum(1 for ln in fh if ln.strip())
    return f"{n} tool-use event(s) recorded by the PreToolUse hook (Code-only)"


def _scorecard(spec, results):
    rows = [r for r in results if r["prompt"] == spec["id"]]
    npass = sum(1 for r in rows if r["passed"])
    return rows, npass, len(rows)


def build(results=None):
    if results is None:
        results = run_all()
    today = datetime.date.today().isoformat()
    total_pass = sum(1 for r in results if r["passed"])
    total = len(results)

    L = [
        "# Observability — per-prompt scorecards",
        "",
        f"_Generated {today} by `evals/observability.py` from the live `centerline_mcp` logic + the run-trace ledger._",
        "",
        "**Performance is not one number.** It decomposes into **compliance (T2) + step-correctness (T3) "
        "+ computation accuracy (T1) + generative quality (T4)**. T1/T2 are graded deterministically below; "
        "T3 is the expected-trace each prompt should exercise; T4 (emails/memos) is rubric + HITL edit-rate, "
        "reported with Track B — never a fabricated single %.",
        "",
        f"**Overall T1/T2: {total_pass}/{total} cases passed.** " f"Run-trace ledger: {_ledger_summary()}.",
        "",
        "## At a glance",
        "",
        "| Prompt | Skills | MCP tools | T1/T2 cases | Reliability |",
        "|---|---|---|---|---|",
    ]
    for spec in _PROMPT_SPECS:
        _, npass, n = _scorecard(spec, results)
        cell = f"{npass}/{n} ✅" if (n and npass == n) else (f"{npass}/{n} ❌" if n else "—")
        L.append(
            f"| **{spec['id']}** {spec['title']} | {', '.join(spec['skills'])} | "
            f"{len(spec['tools'])} | {cell} | {spec['reliability']} |"
        )

    L += ["", "## Per-prompt detail", ""]
    for spec in _PROMPT_SPECS:
        rows, npass, n = _scorecard(spec, results)
        L += [
            f"### {spec['id']} — {spec['title']}",
            "",
            f"- **Expected skills (T3):** {', '.join(spec['skills'])}",
            f"- **Expected MCP tools (T3):** {', '.join(spec['tools'])}",
            f"- **Guards that must fire:** {', '.join(spec['guards'])}",
            f"- **Expected reliability footer:** {spec['reliability']}",
            f"- **Eval (T1/T2): {npass}/{n} passed**",
            "",
            "| Case | Tier | Result | Grounded in | Detail |",
            "|---|---|---|---|---|",
        ]
        for r in rows:
            mark = "✅" if r["passed"] else "❌"
            L.append(f"| `{r['id']}` | {r['tier']} | {mark} | {r['source']} | {r['detail']} |")
        L.append("")

    L += [
        "## Honest limits",
        "",
        "- **Skill selection is probabilistic.** Mitigated because the critical math/compliance lives in "
        "deterministic MCP tools (enforced + testable), not in model choice; the T3 expected-trace above is "
        "the check, and the eval cases pin the tool outputs.",
        "- **The run-trace ledger is coarse today.** The PreToolUse hook records that a tool was used "
        "(Code-only), not which *skill* selected it. Full per-step attribution (a `log_step` MCP tool + a "
        "per-run `traces/run-<id>.jsonl`) is the production path; in prod the same hooks emit OpenTelemetry "
        "→ Datadog as the §4.1 monitoring evidence.",
        "- **The golden set is small and self-authored.** Mitigated by source-grounded expected answers and "
        "negative/adversarial cases (a clean borrower must not flag; a normal doc must not be refused); "
        "production path is a larger labeled set + real RM accept/edit/dismiss feedback.",
        "",
    ]
    os.makedirs(_REPORTS_DIR, exist_ok=True)
    path = os.path.join(_REPORTS_DIR, "observability.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    return path, total_pass, total


if __name__ == "__main__":
    path, npass, n = build()
    print(f"{npass}/{n} T1/T2 cases passed — wrote {os.path.relpath(path, _REPO)}")
