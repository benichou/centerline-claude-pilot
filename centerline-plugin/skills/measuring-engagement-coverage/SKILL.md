---
name: measuring-engagement-coverage
description: Use to answer "which borrowers have I gone quiet on?" — especially distressed ones. Measures days since the last SUBSTANTIVE two-way contact, not just the last log entry.
---

# Measuring engagement coverage ★

Call the **`centerline` MCP tool `measure_engagement_coverage(borrower_name)`** (deterministic, server-side).
It computes the gap to the last **substantive two-way contact** — a phone/video/in-person conversation or a
reviewed package — and **excludes** one-way notices, emails-sent-with-no-response, missed calls, and internal
prep. It also reports the **naive** "days since any logged entry" so the undercount is visible.

This surfaces a risk **no single data field flags**: *engagement thinning while a credit deteriorates.*
Example (Meridian, as-of 2025-05-31): last substantive contact **2025-03-14**; **78 days** of silence — while
in covenant breach — vs a naive **33 days** (because the only entry since was a 0-min overdue notice).

## Rules
- Present the gap as a **fact** (§4.2) — "78 days since the last two-way contact," not "the RM is negligent"
  or any risk characterization.
- **RM-private and advisory** — the RM can annotate ("saw them at a conference") or dismiss; never auto-escalate.
- Pair with `detecting-deterioration-signals`: a long gap *during distress* is the signal that matters.
