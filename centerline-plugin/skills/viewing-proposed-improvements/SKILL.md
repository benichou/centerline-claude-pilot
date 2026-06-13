---
name: viewing-proposed-improvements
description: Use when a reviewer (e.g. compliance) asks what improvements the eval loop has proposed, what should change in the skill library, or to review the latest/all advisory improvement reports. Display-only.
---

# Viewing proposed improvements

The CI "improvement analyst" (`evals/improve.py`, run by the `eval-improve` workflow) reads the latest
agent-eval results and writes **advisory** reports proposing changes to the **prompt/skill library**. This
skill **displays** those reports so a human (often compliance) can decide what to apply. It only reads files —
it works on any surface, including Cowork.

## What to read
- `reports/improvements/latest.md` — the **most recent** advisory report (proposed skill/prompt changes,
  root causes, §-rationale, and an explicit "why this doesn't weaken a guard" note per item).
- `reports/improvements/improvements-<UTC stamp>.md` — the **history**: one timestamped report per run
  (filenames sort chronologically). When asked to "read all reports" / spot recurring themes, list this
  folder and summarize across them.

## How to present (for a compliance reviewer)
- Lead with the summary table (finding · type · real issue vs eval artifact · recurring? · proposed file).
- Separate **Must-fix** (tied to a failed/flaky/**recurring** run) from **Proactive (optional)** hardening; a
  clean history may simply say **"no action needed"** — report that honestly, don't invent items.
- For each item, give the plain-English root cause + the proposed skill change + which § it relates to.
- Call out anything the analyst **flagged for human attention** (i.e. a failure it would NOT fix because it
  would require touching a guard or the eval answer key) — those are the most important to surface.

## Be honest about what this is (and isn't)
- **Advisory only.** Nothing here has been applied. Approving a change means a **human edits the skill library
  by hand**, which then goes through the normal pre-commit (black/flake8) + eval re-validation gate.
- This analyst has **no write access** to code, guards (`guards.py`/`core.py`), or the eval cases — by design,
  so it cannot weaken a guardrail or the answer key to make the eval pass. If a report seems to propose that,
  treat it as a bug and say so.
- If `reports/improvements/` is empty or the latest is stale-dated, say that rather than implying a fresh run.
