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

## Present it as facts (§4.2)
State the numbers and the covenant test result — e.g. *"DSCR 1.03 vs the 1.20 minimum (cushion −0.17),
leverage 4.5 vs the 4.0 maximum; covenant_status: Covenant Breach."* **Do not** add credit characterization
("high risk", "likely to default") — the RM owns that. Cite the data (`grounding-claims-to-source`) and route
any written output through `screen_and_finalize`.
