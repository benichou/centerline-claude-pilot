---
name: detecting-deterioration-signals
description: Use to surface deterioration over time — DSCR/revolver trends, threshold crossings, the status-vs-trend mislabel, thin cushion, and (for construction loans) lifecycle signals. Lifecycle-aware; facts only.
---

# Detecting deterioration signals

Call the **`centerline` MCP tool `detect_deterioration_signals(borrower_name)`** (math is deterministic,
server-side). It looks across the *full* history, not just the binary status, and returns factual signals:

- **DSCR trend** (e.g., "declined 1.45→1.03 over 17 months; below the 1.20 floor"),
- **revolver trend + alert** (e.g., "rose 38%→85%; ≥75% alert — a *non-covenant* metric the status field misses"),
- **status-vs-trend mislabel** (e.g., "covenant_status read 'Compliant' during 9 months of DSCR decline"),
- **thin cushion** (e.g., Summit: "DSCR 1.12 is only 0.02 above the 1.10 floor"),
- **lifecycle / construction** — operating covenants are 0/N-A; surfaces pre-leasing % vs the **75%**
  perm-conversion threshold, schedule, interest-reserve (Arcadia). *This is why monitoring must be
  lifecycle-aware — a DSCR-only view is blind to a construction loan.*

## Rules
- Present signals as **facts** (§4.2) — never "high/elevated risk" or predictions. The RM judges.
- A pristine, improving borrower (e.g., Crestwood) returns **no signals** — say so honestly (the early-warning
  is structurally blind to a healthy borrower; relationship/renewal risk is a *separate* lens).
- Cite the data and **route the written summary through `screen_and_finalize`**. **Do not write your own
  reliability footer or compliance disclaimer** — no "Reliability: High/Moderate" scale, no "no
  creditworthiness…" line (credit vocab even in negation trips §4.2); the tool's deterministic footer is the
  authoritative signal. See `screening-and-gating-output`.
- Then **`render_pdf`** the finalized text for an RM-fileable Centerline PDF (keep the inline readout too),
  **including the trend as a chart** — e.g. `charts=[{"title":"DSCR trend (TTM)","type":"line","labels":
  <months>,"series":<dscr_ttm from get_loan_performance>,"threshold":<floor>}]` (and/or the revolver trend).
