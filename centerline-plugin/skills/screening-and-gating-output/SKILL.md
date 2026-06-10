---
name: screening-and-gating-output
description: Use before any borrower-facing message or credit-file-bound output. Ensure no creditworthiness characterization (§4.2) and route the output through human review (§4.3).
---

# Screening and gating output

The hard compliance line for everything that leaves: **AI states facts and organizes the RM's words; it never
characterizes creditworthiness, recommends waivers/modifications, or produces anything readable as a credit
decision (§4.2). All borrower-facing / credit-file output requires RM review before use (§4.3).**

## How
1. Call the **`centerline` MCP tool `screen_and_finalize`** on the draft (this is the cross-surface guard — it
   runs server-side in both Code and Cowork).
2. If `blocked` (a §4.2 hit), **revise to facts only** — present the numbers and let the RM author any
   judgment — then re-screen. Examples to remove: "elevated credit risk", "likely to default", "I recommend
   waiving", "risk rating". Keep factual status: "DSCR 1.03 vs the 1.20 covenant minimum", "covenant_status:
   Covenant Breach".
3. Tag the finalized output **"Requires RM review"** (§4.3); never send/file without the human gate.
4. When surfacing a *human's* credit decision (e.g. a credit officer's email), quote it **verbatim and
   attributed** — be the scribe, never the author.
