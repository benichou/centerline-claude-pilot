---
name: grounding-claims-to-source
description: Use whenever you state a fact, figure, or claim about a borrower. Cite every claim to its source (file:row / doc:page / email line); if a claim cannot be cited, label it UNVERIFIED rather than asserting it.
---

# Grounding claims to source

Every factual claim about a borrower **must carry a source citation**. This answers the bank's audit
requirement (§7) and the RMs' trust requirement (a prior tool gave wrong covenant numbers).

## Rules
- Retrieve borrower data only through the **`centerline` MCP tools** (`get_borrower_dossier`,
  `get_loan_performance`, …). They strip restricted §2.1 fields server-side, so cited data is already safe.
- Attach a citation to each claim — e.g. `DSCR 1.03 (loan_performance, 2025-05)`, `(activity_log: 3/14)`,
  `(meridian-review.md)`.
- If you cannot tie a claim to a retrieved source, write **`UNVERIFIED`** beside it and do **not** present it
  as fact. Prefer omitting an uncitable claim over asserting it.
- Numbers come from the data/tools, never from memory or estimation.

## Hand-off
Finalize any artifact through `assessing-output-reliability` / the `screen_and_finalize` MCP tool, which
records how well-grounded the output is.
