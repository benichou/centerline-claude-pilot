---
name: drafting-relationship-review-memos
description: Use to build an annual / periodic relationship-review memo (e.g. "build my Summit annual review memo"). The AI assembles the factual sections and drafts the narrative AROUND the RM's own credit assessment — it never writes the assessment itself. This is the compliant, decomposed rebuild of the single-prompt memo (Tom's wf2) that trips §4.2.
---

# Drafting relationship-review memos (decomposed for §4.2)

A relationship-review memo wraps a **credit judgment**. The single-prompt "paste everything → memo" version
(Tom's wf2) is non-compliant precisely because the **AI ends up authoring the creditworthiness
assessment** — which §4.2 forbids. The fix isn't a disclaimer; it's **decomposition**: the AI does the
~80% of assembly + formatting, and the **RM owns the ~20% that is the credit call.** This wins the skeptic
(Marcus) because it removes the memo-writing burden **without changing how he thinks.**

## Steps — do them in this order; do NOT skip step 2

1. **ASSEMBLE the factual sections (cite everything).** Compose `building-client-360` with the data tools —
   `get_loan_performance` (the multi-month trend), `check_covenant_compliance` + `detect_deterioration_signals`
   (the factual covenant/trend read), `get_activity_log` (contact history), and
   `verifying-commitment-fulfillment` if there are open items/commitments. Produce: relationship overview, performance trend,
   covenant status, engagement summary, open items — **every line cited** (`grounding-claims-to-source`),
   **no credit characterization**.

2. **⏸ STOP — ask the RM for the assessment, in their words.** Explicitly pause and request the RM's own
   credit read ("In your words: what's your assessment of this relationship / the credit?"). **Do NOT
   generate, infer, suggest, or "draft for approval" the assessment** — that is the §4.2 line. If no
   RM-authored assessment is provided, the memo is **not complete** — say so; do not fill the gap.

3. **DRAFT the narrative around the RM's assessment.** Place the RM's words as the assessment section
   **verbatim and attributed**, and write the surrounding narrative to *organize and present* the facts and
   the RM's judgment — never to add a creditworthiness conclusion of your own.

4. **SCREEN + render.** Route the memo through **`screen_and_finalize`** (it blocks any credit-adjacent
   language that slipped in, attaches the reliability footer, tags §4.3). Then `render_pdf` for a fileable
   copy; keep the markdown inline. The memo goes to the credit file only after RM review (§4.3).

## Keep the line crisp (§4.2)
- AI MAY: assemble data, summarize the trend as facts, format, and draft narrative **around** the RM's
  assessment.
- AI MAY NOT: write the assessment, characterize creditworthiness ("strong/weak credit", "improving risk
  profile"), or recommend a risk-rating / waiver / action.
- The assessment section must be **RM-authored and non-empty** — that's what makes the memo compliant.

## Honest note (say it)
Demoed on Summit, which is **thin** (sparse logs, no prior memo) — so the assembled sections are lighter
than a well-documented borrower, and in the demo the RM assessment is **simulated** to show the pause. The
value is real for the highest-leverage adopter (Marcus, ~71 memos/yr): the AI removes the assembly burden;
he keeps the judgment.
