---
name: viewing-proposed-improvements
description: Use when asked to show the latest proposed improvements to our skills and automations — the improvements Claude suggested from the eval loop, what should change in the skill library, or to review the latest/all advisory improvement reports. Display-only.
---

# Viewing proposed improvements (to our skills and automations)

The CI "improvement analyst" (`evals/improve.py`, run by the `eval-improve` workflow) reads the agent-eval
history and writes **advisory** reports — the improvements **Claude suggested** for the **skill library**
(proposed prompt/skill changes) plus **automation / eval-loop observations flagged for human attention**. This
skill **displays** those reports so a human (often compliance) can decide what to apply. It only reads files —
it works on any surface, including Cowork.

**Triggers:** "show me the latest proposed improvements to our skills and automations" · "what did Claude
suggest we change?" · "review the latest improvement report."

## How to get the latest (always pull first)
**Call the `centerline` MCP tool `get_latest_report` with `kind="improvements"`.** It runs a read-only
`git pull --rebase` host-side and returns the report **content** directly — so you get the newest report even
in Cowork (whose file view can lag), without doing any git yourself. Present the `content` it returns; mention
the `pulled` status if the sync reported anything notable. If `exists` is false, say there's no report yet
(the eval/improve workflow hasn't produced one).

For the **history** (recurring themes across runs), after pulling, list `reports/improvements/` —
`improvements-<UTC stamp>.md` is one timestamped report per run (filenames sort chronologically) — and
summarize across them.

## How to present (for a compliance reviewer)
- Lead with the summary table (finding · type · real issue vs eval artifact · recurring? · proposed file).
- Separate **Must-fix** (tied to a failed/flaky/**recurring** run) from **Proactive (optional)** hardening; a
  clean history may simply say **"no action needed"** — report that honestly, don't invent items.
- For each item, give the plain-English root cause + the proposed skill change + which § it relates to.
- Call out anything the analyst **flagged for human attention** rather than auto-proposing — i.e. items it
  won't change itself because they touch a guard / the eval answer key, **or are about the automations / the
  eval loop** (e.g. eval coverage, run count, thresholds, cadence). Those flags are the most important to
  surface, since the analyst only *proposes* edits to the skill library, not to the automations.

## Be honest about what this is (and isn't)
- **Advisory only.** Nothing here has been applied. Approving a change means a **human edits the skill library
  by hand**, which then goes through the normal pre-commit (black/flake8) + eval re-validation gate.
- This analyst has **no write access** to code, guards (`guards.py`/`core.py`), or the eval cases — by design,
  so it cannot weaken a guardrail or the answer key to make the eval pass. If a report seems to propose that,
  treat it as a bug and say so.
- If `reports/improvements/` is empty or the latest is stale-dated, say that rather than implying a fresh run.
