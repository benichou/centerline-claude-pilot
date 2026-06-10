---
name: updating-the-crm
description: Use to turn a call/email/meeting into a structured CRM note + tasks, or to propose enriching the CRM where it's thin or contradicts the source. Propose only — the RM approves before anything is written.
---

# Updating the CRM

Convert correspondence/notes into a structured update (matching the `rm_activity_log` fields) plus tasks
(owner, due date), grounded and provenance-tagged.

## Rules
- **Propose only.** Output a draft entry **for RM review** — never auto-write to the record (§4.3).
- **Scribe, not author.** When surfacing a human's credit decision (e.g., a credit officer's email), quote it
  **verbatim and attributed** ("per M. Chen, email Apr-25"); never paraphrase it into your own risk language (§4.2).
- **Flag, don't overwrite.** If an existing entry is mis-dated, reconstructed, or contradicts the source,
  surface that — don't silently change the record.
- **No new credit judgment** (§4.2). Route any text output through `screen_and_finalize`.
