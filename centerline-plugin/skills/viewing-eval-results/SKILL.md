---
name: viewing-eval-results
description: Use when asked to show the eval results, the scorecard, the agent-behavior eval, or how accurate/trustworthy the system is — especially in Cowork. Reads and presents the latest report files (display-only).
---

# Viewing eval results

When the user wants to **see** how the system scored ("show the scorecard", "what's the agent-eval say?",
"how accurate is it?"), read and summarize the latest report files. This is **display-only** — it works on
any surface (including Cowork) because it just reads files.

## Getting the latest (pull first)
To guarantee you're showing the newest report, call the `centerline` MCP tool **`get_latest_report`** with
`kind="agent_eval"` (or `"observability"`) — it `git pull`s host-side and returns the content, so it's current
even in Cowork. Then read the files below for the full detail / history.

## What to read
- `reports/observability.md` — Layer 1/2: deterministic per-prompt scorecards (tool-logic correctness +
  expected skill/tool/guard trace). Always current; no model needed.
- `reports/agent_eval/latest.md` — Layer 3: the **most recent** agent-behavior eval (real-model runs) —
  tool selection, §4.2 on the agent's own narration, fact faithfulness, with each run's captured analysis.
  **Always read `latest.md` for "the latest"** (it's overwritten each run; its header shows the run's
  UTC timestamp + model).
- `reports/agent_eval/agent_eval-<UTC stamp>.md` — the **history**: one timestamped file per run
  (filenames sort chronologically, so the newest is the max). List this folder if asked for trends/history
  or to compare runs over time.
- `evals/results/latest.md` — the raw golden-case pass/fail table.

## How to present
- Lead with the headlines: the Layer-1 golden pass-rate (e.g. 81/81) and the Layer-3 agent pass-rate per
  prompt (e.g. A1/A2/A3 each n/n across runs).
- Make the **layer distinction explicit**: Layer 1 is a deterministic unit test of the tool *code* (the LLM is
  never invoked); Layer 3 is the eval of the *model's* decisions. Don't let one stand in for the other.
- The Layer-1 scorecard (`reports/observability.md`) now spans **both tracks** — A1/A2/A3 (Track A) **and**
  B1/B2/B3/B4 (Track B) — so present it as a whole-system reliability read for the CCO, not just early-warning.

## Also render a Centerline-styled PDF (every view — for the CCO / the file)
After presenting the report inline, **render it to a Centerline-letterheaded PDF**: pass the report content
(from `get_latest_report` or the file) to the **`render_pdf`** MCP tool → a timestamped PDF in
`reports/pdf/`. Keep showing the markdown inline; the PDF is the fileable copy. (If the report body is
truncated/empty because a CI run failed, say so and render the last complete report instead.)

## Important: display vs run (be honest about the surface)
- **`run_evals`** (the MCP tool / `running-the-eval-suite` skill) re-runs Layers 1/2 live — works in Code **and**
  Cowork.
- **`agent_eval.py` (Layer 3) can only be RUN where the `claude` CLI lives** — Claude Code on the host, or CI.
  **Cowork can display the latest `agent_eval.md` but cannot regenerate it.** If the user asks to *run* the
  agent eval from Cowork, say so plainly and point them to `PYTHONPATH=mcp python3 evals/agent_eval.py` in
  Claude Code (or the scheduled CI run) — then show the resulting report here.
- If a report file is missing or stale-dated, say that rather than implying a fresh run happened.
