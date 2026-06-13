# Agent-behavior eval (the LLM-driven decisions)

_Generated 2026-06-12 by `evals/agent_eval.py` — 3 run(s) per prompt through Claude Code headless._

Grades the **model's** decisions with deterministic code: tool selection, §4.2 on the agent's own narration, and fact faithfulness. Complements `runner.py` (which unit-tests the tool logic).

| Prompt | Runs passed | Tool selection | §4.2 on output | Facts |
|---|---|---|---|---|
| **A1** | 3/3 | 3/3 | 3/3 | 3/3 |
| **A2** | 3/3 | 3/3 | 3/3 | 3/3 |
| **A3** | 3/3 | 3/3 | 3/3 | 3/3 |

## Per-run detail

### A1
- run 1: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist'] · §4.2 hits=[] · missing facts=[]
- run 2: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist'] · §4.2 hits=[] · missing facts=[]
- run 3: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist'] · §4.2 hits=[] · missing facts=[]

### A2
- run 1: ✅ PASS · tools=['Skill', 'ToolSearch', 'check_covenant_compliance', 'get_loan_performance'] · §4.2 hits=[] · missing facts=[]
- run 2: ✅ PASS · tools=['Skill', 'ToolSearch', 'check_covenant_compliance'] · §4.2 hits=[] · missing facts=[]
- run 3: ✅ PASS · tools=['Skill', 'ToolSearch', 'check_covenant_compliance'] · §4.2 hits=[] · missing facts=[]

### A3
- run 1: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist', 'measure_engagement_coverage'] · §4.2 hits=[] · missing facts=[]
- run 2: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist', 'measure_engagement_coverage'] · §4.2 hits=[] · missing facts=[]
- run 3: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist', 'measure_engagement_coverage'] · §4.2 hits=[] · missing facts=[]

## Honest limits

- **Non-deterministic** — the model can vary run to run; read the pass-rate, run with `--runs N`.
- **§4.2 use-vs-mention** — the scanner flags a blocked phrase even if the agent is *quoting* it to explain a block; rare for A1/A2/A3, noted not fatal.
- **Small prompt set** — the three Track-A prompts; Track-B prompts (emails/memos) will add a generative-quality layer that may warrant an LLM-as-judge (a signal, not ground truth).

