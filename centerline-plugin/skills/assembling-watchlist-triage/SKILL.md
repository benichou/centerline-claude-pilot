---
name: assembling-watchlist-triage
description: Use for "who in my book needs attention this week?" — assemble a portfolio triage list combining covenant status, deterioration signals, and engagement gaps, ranked by risk × neglect.
---

# Assembling the watchlist (triage)

Call the **`centerline` MCP tool `assemble_watchlist()`** (deterministic, server-side). It composes, per
borrower: computed covenant status, deterioration signals, and the substantive-contact gap — then ranks by
**covenant breach → signal count → days-since-substantive-contact** (a facts-derived triage order, **not** a
credit rating).

Typical result (as-of 2025-05-31): **Meridian** on top (breach + 4 signals + 78-day gap), then **BlueLine**
(breach), then **Summit** (thin cushion + drift), **Arcadia** (construction lifecycle), and **Crestwood** at
the bottom — compliant, **0 signals** (distress monitoring is blind to a healthy borrower; its renewal/
retention risk is a *separate* lens).

## Rules
- This is **the rebuild of Tom's wf5** (weekly portfolio summary), done compliantly.
- **Facts only** (§4.2) — each line is a metric + source, never "high risk." The RM owns the judgment.
- **RM-private and advisory**; nothing auto-escalates. As **automated monitoring**, it's presented as
  "designed, pending CCO approval" (§4.1).
- Source-cite every figure (`grounding-claims-to-source`); route any written readout through `screen_and_finalize`.
