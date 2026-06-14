---
name: detecting-cross-source-discrepancies
description: Use to reconcile the system of record against the emails and structured data — "what actually happened, what's mis-dated, what decision isn't in the file?" Surfaces mis-dated/conflated CRM entries, decisions that live only in email, and figure/date contradictions. Facts only; a human's credit decision is quoted verbatim and attributed (scribe, not author).
---

# Detecting cross-source discrepancies

The bank's record is a thin, lagging, sometimes-inaccurate proxy. This skill reconciles the **three
sources** — the CRM activity log, the email thread, and the structured data — and surfaces where they
disagree, as **facts (§4.2)**. You organize and quote; you never characterize creditworthiness, and you
never paraphrase a human's credit decision into your own risk language.

## Steps

1. **Pull the merged timeline.** Call the `centerline` MCP tool **`get_relationship_timeline(borrower)`** —
   it merges the CRM log + the email messages into one chronological, source-tagged list (deterministic
   dates, so you don't reconstruct them). Also pull `get_emails(borrower)` and `get_activity_log(borrower)`
   for the full text, and `get_loan_performance` / `detect_deterioration_signals` for the structured figures.

2. **Surface three kinds of discrepancy**, each grounded to its source (`grounding-claims-to-source`):
   - **Mis-dated / conflated entries.** A log entry dated *before* the emails it summarizes — or one row
     collapsing a multi-day exchange — is a timeline-integrity signal (it poisons contact-recency math).
     Cite the log date vs the email dates (e.g. *"the log entry is dated 2025-04-09, but the Draw #13
     thread it summarizes runs 2025-04-22 → 25"*).
   - **Email-only decisions (scribe-not-author).** A credit officer's / RM's decision that never reached
     the record. **Quote it verbatim and attribute it** (*"per M. Chen, email 2025-04-25: '…'"*) — surface
     the human's words; do **not** restate them as your own creditworthiness assessment. Propose a
     provenance-tagged CRM entry for the RM to approve (propose-only — see `updating-the-crm`; §3.3/§4.2).
   - **Figure / date contradictions.** The same fact reported differently across sources (e.g. a completion
     date that's "Q4 2025" in one log entry and "end of July" in a later email). State both, with sources.

3. **Screen + render.** Collect the contradictions as `cross_source_mismatches` and anything you couldn't
   independently verify as `low_confidence_inputs`, and pass both to **`screen_and_finalize`** so the
   reliability footer is honest (Partial when the record and the correspondence diverge). Then
   **`render_pdf`** the finalized readout (a fileable PDF copy; DRAFT/§4.3 banner + footer preserved) —
   keep the markdown shown inline too. Tag for RM review (§4.3). If you surfaced an email-only credit
   decision, offer to draft the provenance-tagged CRM entry (propose-only — `updating-the-crm`).

## Honest framing
This is **synthesis**, not arithmetic — its value is the LLM connecting sources no one reconciles. Keep it
trustworthy by **grounding every claim to a source**, **quoting human decisions verbatim**, and letting the
**reliability footer** say where the record is thin. Needs *both* sources present — strong for documented
relationships, near-useless where there's no email trail (say so).
