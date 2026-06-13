# Evaluation & observability — how we prove the system is correct

This doc explains the eval/observability layer in plain terms: what the **golden set** is, **how grading
works** (and why there's no LLM in it), how to **run it** — including **in-console on either surface** — and
the **honest limits**. Methodology rationale lives in [`../evals/GOLDEN.md`](../evals/GOLDEN.md).

## The questions this answers
1. *Are the numbers actually right — and will I notice if a code change breaks them?* → the **golden set + runner** (Layer 1).
2. *Can I see, at a glance, what each demo prompt does and how trustworthy it is?* → the **observability report** (Layer 2).
3. *Does the **model** make the right decisions — pick the right tool, narrate faithfully, and not emit credit-adjacent language?* → the **agent-behavior eval** (Layer 3).

> **Be precise about what each layer is.** Layer 1 is a **deterministic unit/integration test of the tool
> code** — it calls the Python functions directly; the LLM is never invoked. That's the *floor* ("the engine
> is correct"), not "the LLM-driven system is correct." Layer 3 is the one that actually runs the **model**
> and grades its decisions. Don't let a green Layer 1 be mistaken for a graded agent.

## The golden set (the "answer key")
Plain-text cases, one per line, in [`../evals/cases/`](../evals/cases/):
- **`track-a.jsonl`** — early-warning ground truth across all five borrowers (covenant, trends, engagement, watchlist).
- **`foundation.jsonl`** — compliance assertions (§2.1 strip, §5 halt, guarantor refusal, §4.2 block/allow) + reliability.

Each case names a tool, its args, and the **expected answer grounded in a real source row** (the `source`
field is the receipt). Example:

```json
{"id": "A2-meridian-dscr", "tier": "T1", "tool": "check_covenant_compliance",
 "args": {"borrower_name": "Meridian"}, "source": "loan_performance_monthly.csv (Meridian, 2025-05)",
 "expect": {"dscr.value": 1.03, "dscr.min": 1.2, "dscr.breach": true}}
```

**Tiers:** `T1` objective ground truth · `T1-neg` negative ground truth (a clean borrower must NOT flag) ·
`T2` binary compliance · `T2-neg` negative compliance (a normal doc must NOT be refused). Negatives matter
as much as positives — they catch the system **over-firing**.

**Current size: 81 cases.** It grows with built capability — Track B (doc-intelligence, close-the-loop,
reconciliation, retention, memo) will add its own cases and carry the set past 100. We deliberately do **not**
pad to a round number with cases for unbuilt features (that would be fabrication) or near-duplicates (that
would be inflation).

## How grading works — deterministic, no LLM
`evals/runner.py` is an **automatic grader with zero AI in it.** For each case it:
1. **calls the real tool function** — `core.check_covenant_compliance("Meridian")`, the *same code the demo
   uses*, not a mock;
2. pulls the value out by a dotted path (`dscr.value`) and compares it to the expected answer with ordinary
   Python (`==`, `startswith`, `len`, …);
3. records PASS/FAIL.

Why no LLM? Because these answers are objective — there's one correct number, so `==` is more reliable,
faster, and cheaper than asking a model "is 1.03 right?". (An LLM-as-judge only fits fuzzy outputs like email
quality — the "T4" tier — and even there it's a hint, not the verdict.) A green run is therefore real proof.

## The observability report (the "report card")
`evals/observability.py` writes [`../reports/observability.md`](../reports/observability.md). It:
1. **re-runs the grader** (the report can never be stale),
2. merges in an authored **expected-trace** spec — which skills/tools/guards each demo prompt *should* fire,
3. reads the run-trace ledger (`traces/run-ledger.log`), and
4. writes per-prompt scorecards + an at-a-glance table + an explicit **honest-limits** section.

## How to run it

| Goal | Command |
|---|---|
| Grade the golden set | `PYTHONPATH=mcp python3 evals/runner.py` |
| Regenerate the report card | `PYTHONPATH=mcp python3 evals/observability.py` |
| Deterministic guard/core tests | `PYTHONPATH=mcp python3 mcp/tests/test_compliance.py` |
| Agent-behavior eval (real model, Layer 3) | `PYTHONPATH=mcp python3 evals/agent_eval.py --runs 1` (or `--selftest`) |

### In-console (Claude Code **and** Cowork) — the `run_evals` MCP tool
Because the grader is exposed as the **`centerline` MCP tool `run_evals`**, anyone can trigger it from the
chat on either surface — no terminal. Just ask:

> *"Run the evals"* · *"Are the numbers right?"* · *"Show me the scorecard"*

Claude calls `run_evals`, which grades the live tools, **regenerates `reports/observability.md`**, and returns
a structured summary (`passed`/`total`, `all_passed`, `by_prompt`, `by_tier`, and any `failures`). The
**`running-the-eval-suite`** plugin skill tells Claude how to present it honestly. This makes "prove it's
correct" a live demo moment rather than an engineer-only terminal step.

> Surface note: in **Code** you can also just let Claude run the scripts via its shell. In **Cowork** the shell
> is sandboxed and project hooks don't fire, so the **MCP tool is the reliable cross-surface path** — which is
> exactly why `run_evals` lives in the server.

## Layer 3 — agent-behavior eval (grading the model's decisions)
`evals/agent_eval.py` is the piece that actually **evaluates the LLM-driven system** (Layer 1 only tests the
tool code). It runs the three Track-A demo prompts through **Claude Code headless** (`claude -p`), captures
the **tool trace** and the **final reply**, and grades — *with deterministic code, no LLM judge* — three things:

1. **Tool selection** — did the agent call the right `mcp__centerline__*` tool, with the right borrower arg?
2. **§4.2 on the agent's own narration** — does the reply contain credit-adjacent language? (Run through the
   same `guards.scan_credit_language` the server uses. **This closes the gap the unit tests can't see**: the
   risk of the model emitting credit characterization directly in chat.)
3. **Fact faithfulness** — does the reply carry the correct figures (DSCR 1.03, the 78-day gap) in the right order?

**Why code, not an LLM judge:** all three are objective, so code is more reliable than a model opinion. An
LLM-as-judge is reserved for the genuinely subjective generative-quality layer (Track-B emails/memos) — and
even there it's a *signal, not ground truth* (§4.2). **Self-evaluation by the same agent is deliberately
avoided** — an evaluator must be independent of what it grades.

Run it (you run this — it invokes Claude Code headless on **your** account; uses scoped `--allowedTools`, not a
permission bypass):
```bash
PYTHONPATH=mcp python3 evals/agent_eval.py --runs 1                       # real model runs -> reports/agent_eval/
PYTHONPATH=mcp python3 evals/agent_eval.py --runs 3                       # 3x per prompt -> read the pass-rate
PYTHONPATH=mcp python3 evals/agent_eval.py --model claude-sonnet-4-6      # cheaper model (cost lever)
PYTHONPATH=mcp python3 evals/agent_eval.py --selftest                     # prove the GRADER works, no model call
```
Because the model is non-deterministic, read the **pass-rate** across runs, not a single boolean. Each run's
narration is saved (collapsible in the report; full transcript in `traces/agent_eval/<stamp>/`).

**History & "which is latest":** each run writes a timestamped `reports/agent_eval/agent_eval-<UTC>.md`
(filenames sort chronologically) **and** overwrites `reports/agent_eval/latest.md` — so a skill/reader just
opens `latest.md` for the newest, or lists the folder for history. The nightly CI **commits these back to
main** (below), so the history persists in the repo and the `viewing-eval-results` skill can show it on any
surface.

**Flags:** `--model <id>` (override; default = CLI default, which is the demo model), `--mcp-config <path>`
(default repo `.mcp.json`; CI uses `evals/ci.mcp.json`), `--min-pass-rate <0..1>` (exit 0 if the overall
pass-rate clears the bar — default 1.0 strict; CI relaxes it for non-determinism).

### Scheduled CI (nightly regression) — `.github/workflows/agent-eval.yml`
A GitHub Actions workflow runs this nightly (+ a manual button) on **Sonnet 4.6** (`--model claude-sonnet-4-6`)
to keep cost low, with `--min-pass-rate 0.67` so one varied run out of three doesn't flake the build, and
commits the timestamped report to `reports/agent_eval/` on main (history) **and** uploads it as a run
artifact. Setup + honest caveats:
- **Secret:** add `ANTHROPIC_API_KEY` (Settings → Secrets → Actions). CI auth = an **API key → pay-per-token**,
  not the Pro/Max subscription. Triggers are `schedule` + `workflow_dispatch` only (never `pull_request`), so
  the key never reaches a PR-triggered run.
- **Model caveat:** nightly-on-Sonnet is a cheap **smoke/regression** signal; the live demo runs on Opus, so
  re-run with `--model claude-opus-4-8` (or no `--model`) before the panel to test the *demo* model.
- **Data residency:** fine here because the data is **synthetic**. For **real** borrower data (§2.3) you would
  NOT run this in cloud CI — use a self-hosted/on-prem runner or run locally. The workflow header says so.
- **Portable config:** `evals/ci.mcp.json` has no absolute Mac paths (uv from PATH, `--project .`); the
  workflow supplies `PYTHONPATH`/`CENTERLINE_DATA_DIR` as absolute via `${{ github.workspace }}`.
- **Commit-back (history):** the job needs `permissions: contents: write` and pushes a nightly
  `chore(eval): … [skip ci]` commit to main with the timestamped report (the `[skip ci]` + GITHUB_TOKEN push
  don't re-trigger it). Don't want a nightly bot commit? Delete the "Commit the timestamped report" step and
  set `permissions: contents: read` — history then lives only as run artifacts (downloadable from Actions,
  but not visible to the folder-reading skill).

## Layer 4 — the improvement loop (AI flags, human decides)
`evals/improve.py` (run by the **`eval-improve`** workflow) closes the loop *safely*: it reads the agent-eval
report **history** (latest in full + summaries of prior runs, so it can tell a one-off from a **recurring/flaky**
pattern), and writes a **timestamped advisory report** to `reports/improvements/` proposing changes to the
**prompt/skill library**. The report separates **Must-fix** (tied to a failed/flaky/recurring run) from a
**severity-gated Proactive** section (concrete hardening only — allowed to be empty), each with root cause, the
concrete skill edit, the §-rationale, and a "why this doesn't weaken a guard" note. On a fully-clean history it
says **"no action needed"** rather than manufacturing churn. A human (often compliance) reads it via the
**`viewing-proposed-improvements`** skill (works in Cowork) and applies anything approved **by hand** (through
the normal pre-commit + eval-validation gate).

**Why report-only, not auto-PR or auto-merge:** the analyst has **no write access** to code, guards, or the
eval answer key — it runs with read-only tools and the workflow commits **only `reports/improvements/`**. So
it structurally **cannot** weaken a guardrail or the answer key to make the eval pass (the reward-hacking risk
that makes autonomous self-modification dangerous for a compliance system). It can only *advise*; a human
decides and edits. This mirrors the product's own §4.3 principle.

- **Triggers:** after each `agent-eval` run (`workflow_run`) + a manual button (`workflow_dispatch`). The
  manual trigger is what a **personal-GitHub connector** lets a compliance reviewer fire from Cowork (the
  `centerline` MCP is unchanged — GitHub is a *separate* connector, authenticated to the personal account).
- Run locally: `python3 evals/improve.py --model claude-sonnet-4-6` (or `--dry-run` for a no-model plumbing check).

**Always-latest, cross-surface:** the `centerline` MCP tool **`get_latest_report`** (kind = `improvements` /
`agent_eval` / `observability`) runs a read-only `git pull --rebase` host-side and returns the report
**content** — so the `viewing-*` skills show the newest report even in Cowork (whose file view can lag),
without anyone running git by hand. It never commits/pushes and never calls the GitHub API.

## What "performance" means here (no single %)
> performance = compliance (T2) + step-correctness (T3 expected-trace) + computation accuracy (T1) + generative quality (T4: rubric + edit-rate)

We report a clean pass-rate only for the deterministic T1/T2 cases. We never show a fabricated single
"accuracy %" for generative output.

## Honest limits (stated, not hidden)
- **Skill selection is probabilistic** — mitigated because the critical math/compliance lives in deterministic
  MCP tools (enforced + tested), not in model choice; the T3 expected-trace is the check.
- **The run-trace ledger is coarse today** — the PreToolUse hook records that a tool was used (Code-only), not
  which *skill* chose it. Full per-step attribution (a `log_step` tool + per-run `traces/run-<id>.jsonl`) and
  hook→OpenTelemetry→Datadog are the production path (the §4.1 monitoring evidence).
- **The golden set is small and self-authored** — mitigated by source-grounded expected answers and negative
  cases; production path is a larger labeled set + real RM accept/edit/dismiss feedback.

## Files
```
evals/GOLDEN.md              methodology
evals/cases/*.jsonl          the golden set (81 cases)
evals/runner.py              Layer 1: deterministic tool-logic grader -> evals/results/latest.md
evals/observability.py       Layer 2: report-card generator           -> reports/observability.md
evals/agent_eval.py          Layer 3: agent-behavior eval (real model) -> reports/agent_eval/{<UTC>.md, latest.md}
evals/ci.mcp.json            portable MCP config for CI (no absolute paths)
evals/improve.py             Layer 4: improvement analyst (advisory) -> reports/improvements/{<UTC>.md, latest.md}
.github/workflows/agent-eval.yml  nightly Layer-3 run on Sonnet 4.6 (schedule + manual)
.github/workflows/eval-improve.yml  Layer-4 advisory report after agent-eval + manual (Sonnet 4.6)
mcp/centerline_mcp/core.py   run_evals() (the tool logic)
mcp/centerline_mcp/server.py exposes the run_evals MCP tool
centerline-plugin/skills/running-the-eval-suite/   the in-console skill
```
