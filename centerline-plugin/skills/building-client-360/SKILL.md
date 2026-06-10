---
name: building-client-360
description: Use when preparing for a meeting or review, or whenever you need a consolidated view of a borrower. Assemble a 360 dossier from all sources and explicitly flag the dimensions the data does NOT cover.
---

# Building the client 360

Assemble one consolidated view of a borrower using the **`centerline` MCP tools**:
- `get_borrower_dossier` — relationship profile + latest performance + whether a memo exists
- `get_loan_performance` — the trend over months
- `get_activity_log` — contact history (and recency)
- `get_emails` — recent correspondence / open threads

Present: who/what/terms · performance trend · contact recency · outstanding threads. **Cite every figure**
(see `grounding-claims-to-source`).

## Be honest about coverage
The data has **no** deposit/treasury balances, product-penetration, client-profitability, or collateral
valuations. **State which dimensions are absent** rather than implying a complete picture.

## Compliance
Facts only — never characterize creditworthiness (§4.2); the RM owns any judgment. Route any written 360 /
brief through `screen_and_finalize` before it's shared.
