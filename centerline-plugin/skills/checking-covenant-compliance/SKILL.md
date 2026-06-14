---
name: checking-covenant-compliance
description: Use to answer "is this borrower covenant-compliant?" with cushion and trend. Reports the deterministic covenant test as facts — never a credit judgment.
---

# Checking covenant compliance

Call the **`centerline` MCP tool `check_covenant_compliance(borrower_name)`** — the math is deterministic
(computed server-side, not by you), so the numbers are auditable.

It returns, for the latest month: DSCR vs the borrower's `covenant_dscr_min` (+ cushion, breach flag),
leverage vs `covenant_leverage_max` (+ headroom, breach flag), revolver utilization, the **reported**
`covenant_status`, the **computed** status, and whether they match. Construction loans return
`applicable: false` (operating covenants aren't in effect yet — use `detecting-deterioration-signals`).

## Answer the "trend" too — don't make it an optional follow-up
When the question asks about the **trend**, the **cushion AND trend**, or whether the **reported status
matches the trajectory**, ALSO call **`detect_deterioration_signals(borrower_name)`** and fold it in — it
returns the DSCR/revolver trend and the **status-vs-trend mislabel** (e.g. the status field read "Compliant"
through months of DSCR decline — the label lagged the slide). Include this in the answer; do **not** offer it
as a follow-up. (Latest-month compliance + the multi-month trend together are the whole answer.)

## Present it as facts (§4.2)
State the numbers and the covenant test result — e.g. *"DSCR 1.03 vs the 1.20 minimum (cushion −0.17),
leverage 4.5 vs the 4.0 maximum; covenant_status: Covenant Breach."* **Do not** add credit characterization
("high risk", "likely to default") — the RM owns that. Cite the data (`grounding-claims-to-source`) and
**route the written output through `screen_and_finalize`** — **do not write your own reliability footer or
compliance disclaimer** (no "Reliability: High/Moderate" scale, no "no creditworthiness…" line; naming credit
vocab even in negation trips §4.2). The tool's deterministic footer is the authoritative signal. Then
**`render_pdf`** the finalized text for an RM-fileable Centerline PDF (keep the inline readout too) — and
**include the DSCR trend as a chart**: pass `charts=[{"title":"DSCR trend (TTM) vs the <min> floor",
"type":"line","labels":<months>,"series":<dscr_ttm from get_loan_performance>,"threshold":<covenant min>}]`
so the slide-vs-floor is visual, not just prose.
