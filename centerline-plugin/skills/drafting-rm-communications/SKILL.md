---
name: drafting-rm-communications
description: Use to draft a client-facing message — a missing-documents request, a draw-response letter, or a meeting follow-up. Keep it factual and brief; never make commitments or convey credit-status bad news; route through review.
---

# Drafting RM communications

Draft concise (<200 words) client-facing messages grounded in retrieved facts (e.g., exactly which covenant
package items are still outstanding). Covers Tom's draw-response letters [wf1] and client emails [wf3].

## Rules
- **No commitments** — no rates, approvals, waivers, or timelines the RM hasn't authorized.
- **No credit-status / bad-news characterization** — that's the RM's to deliver, not the AI's.
- State **facts + clear requests** only ("To process Draw #13 we still need: 1) … 2) … 3) …").
- **Route the draft through `screen_and_finalize`** (§4.2 scan) — it tags the output **"Requires RM review"**
  (§4.3). Never send without the RM. **Pass a record-completeness caveat as a structured
  `low_confidence_input`** — `{"reason":"doc receipt unconfirmed — confirm before sending","tool":
  "get_activity_log","source":"rm_activity_log.csv"}` — because a document *request*'s premise ("these are
  still outstanding") depends on the record being complete (which reconciliation showed it may not be). So
  the footer honestly reads **Partial** with that reason + its tool/source shown, consistently across the
  email and the draw-response letter. Do **not** write your own footer — the tool's footer is authoritative.
- **Then call `render_pdf`** on the returned `finalized_text` to emit a PDF copy (DRAFT banner + footer
  preserved) — keep the markdown shown inline too. See `screening-and-gating-output`.
- Ground every referenced fact (see `grounding-claims-to-source`).
