---
name: verifying-commitment-fulfillment
description: Use to "close the loop" — extract the commitments, conditions, deadlines, and document requests from the narrative (emails / memo / notes) and verify each against the subsequent data and log. Marks each met / unmet / still-open / unverifiable, with the source. Facts only; the RM owns the judgment.
---

# Verifying commitment fulfillment (close the loop)

The standout creative capability: nothing in the bank connects the **RM's / borrower's stated commitments**
to the **subsequent record** to check whether the plan was actually followed. This skill does — as
**facts (§4.2)**. It elevates monitoring from "metrics moved" to "**commitments not kept**."

## Steps

1. **Gather the narrative + the record.** `get_emails(borrower)`, `get_activity_log(borrower)`, the merged
   `get_relationship_timeline(borrower)`, and the structured data (`get_loan_performance`,
   `detect_deterioration_signals` — for construction borrowers this returns pre-leasing vs the 75%
   perm-conversion threshold, a deterministic anchor).

2. **Extract every commitment / condition / request**, each with its source + date:
   - borrower **commitments** ("I'll send items 1–3 by Friday"; "we'll be at 75% within 60 days"),
   - lender / credit-officer **conditions** ("don't waive the 75% threshold"; "tenant names in our file"),
   - **deadlines** and **document requests**, and **self-imposed limits** (e.g. a revolver cap).

3. **Verify each against the subsequent data/log** and mark its status, with the evidence + source:
   - **met** — fulfilled (cite the later log entry / data),
   - **unmet** — a passed deadline, an unfulfilled condition, an undelivered doc, a breached limit,
   - **open** — a tracked condition still live (e.g. pre-leasing **71% < 75%** per
     `detect_deterioration_signals` → the "don't waive 75%" condition remains in force),
   - **unverifiable** — no record either way (say so; don't assume).
   Register lender conditions as **tracked conditions** and re-check them against the latest data.

4. **Screen + render.** Pass the unmet/open/unverifiable items as `low_confidence_inputs` (and any
   source contradictions as `cross_source_mismatches`) to **`screen_and_finalize`** so the footer reflects
   it. Ground every item (`grounding-claims-to-source`). Tag for RM review (§4.3). The natural next step is
   a client communication (e.g. a draw-response / missing-docs letter) — hand off to
   `drafting-rm-communications`.

## Keep it factual (§4.2)
"3 of the Feb-14 commitments are unmet" and "pre-leasing 71% vs the 75% condition" are **facts**. Whether
that changes the credit is the **RM's** call — never write "high risk" / "likely to breach". A human's
credit condition is surfaced **verbatim + attributed** (scribe, not author).
