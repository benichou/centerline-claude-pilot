---
name: running-the-eval-suite
description: Use when asked to run the evals, check accuracy, prove the numbers are right, or show the per-prompt scorecard. Runs the golden-set evaluation against the live tools and reports the results in-console (works in Claude Code and Cowork).
---

# Running the eval suite

When the user wants to **verify the system is correct** ("run the evals", "are the numbers right?",
"show me the scorecard", "prove it"), call the **`centerline` MCP tool `run_evals`** and present what it
returns. This works on both surfaces because the grader runs server-side in the MCP.

## What it does
- Grades the **golden set** — source-grounded ground-truth cases (T1, e.g. Meridian DSCR 1.03 / breach, the
  78-day engagement gap) and binary compliance assertions (T2: §2.1 credit-grade strip, §5 halt, guarantor
  refusal, §4.2 block) — plus **negative cases** (a healthy borrower must NOT flag).
- The grader is **deterministic Python — no LLM** — calling the same code the demo uses, so a green result
  is real proof, not a model opinion.
- Regenerates `reports/observability.md` (the per-prompt scorecards) so the report stays in sync.

## How to present the result
- Lead with the headline: **`passed`/`total`** and whether `all_passed` is true.
- Show the **`by_prompt`** breakdown (A1 / A2 / A3 / foundation) and **`by_tier`** (T1 ground-truth vs T2
  compliance), so it's clear *what* was verified.
- If `failures` is non-empty, list each `{id, detail}` plainly — do not paper over a failure.
- Point to the refreshed `observability_report` path for the full per-prompt detail.

## Honesty rules
- "Accuracy" is a clean number **only** for these deterministic T1/T2 cases. Do **not** present a single
  blended "accuracy %" for generative output (emails/memos) — that's rubric + edit-rate, reported separately.
- State the known limit when relevant: the golden set is small and self-authored (mitigated by
  source-grounded answers + negative cases); the production path is a larger labeled set + real RM feedback.
