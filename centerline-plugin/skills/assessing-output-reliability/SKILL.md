---
name: assessing-output-reliability
description: Use when finalizing any artifact (brief, digest, email, memo, readout). Attach a deterministic reliability footer (qualitative label + reasons) — never a numeric percentage.
---

# Assessing output reliability

Before presenting an artifact, route it through the **`centerline` MCP tool `screen_and_finalize`**. It runs
deterministically (so it works in both Claude Code and Cowork) and returns a **reliability footer**:

- **label**: `Grounded` / `Partial` / `Unverified` (or `BLOCKED (§4.2)` if it contains credit-adjacent language)
- **reasons**: uncited claims, low-confidence inputs (reconstructed / back-dated / self-reported / stale),
  cross-source mismatches, missing items.

## Rules
- **Never invent a numeric confidence %** — LLM self-confidence is mis-calibrated, and a "%" reads as a
  credit-risk probability (§4.2). The footer is a qualitative label + concrete reasons.
- Surface the footer on the artifact so the RM sees exactly how trustworthy it is and why.
- If the tool returns `BLOCKED`, fix the §4.2 issue (state facts, not credit characterization) and re-run.
- **Use the tool's footer — don't write your own.** Don't append prose like "no creditworthiness claims made
  (§4.2)": naming credit-characterization words *even to deny them* trips the §4.2 screen and is redundant.
  The `screen_and_finalize` footer is the compliance signal; let it speak.
