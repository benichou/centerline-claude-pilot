# Deliverable A — the recipe (exact prompts + agent design)

> The brief asks for **"exact prompts / agent design"** — verbatim, not paraphrased. This is that
> artifact for Track A (the compliant rebuild of Tom's wf5). It pairs with
> [`what-changed-vs-wf5.md`](./what-changed-vs-wf5.md) (the *why*) and the eval/observability infra in
> [`../../evals/`](../../evals/) + [`../../reports/observability.md`](../../reports/observability.md)
> (the *proof*).

---

## How it runs (agent design, in one picture)

Track A is **not one monolithic agent.** It's a small library of **composable skills** that the model
auto-selects by their description, each backed by a **deterministic MCP tool** that does the actual
computation. The model orchestrates and narrates; it never does the math or makes the credit call.

```
  RM types a prompt (Cowork or Code)
        │
        ▼
  Claude selects skill(s) by description ──► skill calls the matching mcp__centerline__* tool
        │                                          │
        │                                          ▼
        │                              centerline MCP server (local stdio)
        │                                   • §2.1 strip · §5 gate · guarantor refusal  (server-side)
        │                                   • deterministic compute (covenant/trend/engagement/rank)
        │                                          │
        ▼                                          ▼
  narrate the returned FACTS ──► screen_and_finalize (§4.2 block + reliability footer + §4.3 tag)
        │
        ▼
  RM-private artifact (file in folder) ──► RM reviews / dismisses / annotates  (§4.3; §4.1 CCO for automation)
```

**Load it (Claude Code):**
```bash
claude --strict-mcp-config --mcp-config .mcp.json \
       --plugin-dir ./centerline-plugin --setting-sources project
```
**Cowork:** MCP bridged via `claude_desktop_config.json`; skills via the uploaded `centerline-plugin.zip`
(see [`docs/mcp_local_cowork.md`](../../docs/mcp_local_cowork.md)).

**The design rule (the architecture judgment from the brief):** decompose **only where compliance or
accuracy demands it.** Track A decomposes because (a) the aggregation is the §-risk, (b) "who needs
attention" is a credit judgment that must be deterministic (§4.2), and (c) trend/ranking over a CSV is
unreliable in an LLM. Tom's *drafting* workflows stay single-prompt — we don't over-engineer.

---

## The three prompts

Each prompt below is **verbatim** (what the RM types), then: the skill(s) it triggers, the MCP tool(s)
that do the work, the guards that fire, what comes back, and the golden cases that prove it.

### A1 — "Who needs attention this week?"

> **Prompt (verbatim):**
> ```
> Who in my portfolio needs attention this week? Rank them and show me the facts behind each — don't
> characterize their credit, just the numbers and the gaps.
> ```

- **Skill:** `assembling-watchlist-triage`
- **MCP tool:** `assemble_watchlist` (which internally composes `check_covenant_compliance` +
  `detect_deterioration_signals` + `measure_engagement_coverage` for every borrower)
- **Guards:** §2.1 strip + §5 gate (server-side, on every borrower read); output routed through
  `screen_and_finalize` (§4.2 + reliability footer + §4.3 tag)
- **Returns:** a list ranked by **covenant breach → deterioration-signal count → days since substantive
  contact** (a *facts-derived* order, explicitly **not** a credit rating). Meridian #1 → Crestwood last.
- **The point:** it **ranks, it doesn't judge** (§4.2); every line is cited; it blends financial distress
  *and* relationship neglect — and it surfaces that Crestwood sinks to the bottom precisely because
  distress monitoring is blind to a healthy borrower (the bridge to Deliverable B).
- **Backing golden cases:** `A1-meridian-first`, `A1-crestwood-last`, `A1-crestwood-zero-signals` (negative).

### A2 — "Is Meridian covenant-compliant — cushion and trend?"

> **Prompt (verbatim):**
> ```
> Is Meridian covenant-compliant as of the latest month? Show DSCR and leverage against their covenant
> thresholds with the cushion, the revolver level, and whether the reported status matches the trend.
> ```

- **Skill:** `checking-covenant-compliance` (+ `detecting-deterioration-signals` for the trend/mislabel)
- **MCP tools:** `check_covenant_compliance` (latest-month test, cushion, reported-vs-computed) +
  `detect_deterioration_signals` (full-series DSCR/revolver trend, ≥75% revolver alert, status-vs-trend
  mislabel count)
- **Guards:** §2.1/§5 server-side; `screen_and_finalize` on the narration
- **Returns:** DSCR 1.03 vs 1.20 min (**cushion −0.17, BREACH**), leverage 4.5 vs 4.0 (BREACH),
  revolver 85% (a **non-covenant** metric flagged at the 75% alert level), DSCR trend 1.45→1.03 over 17
  months, and the fact that `covenant_status` read "Compliant" through months of decline (the label
  lagged the trajectory).
- **The point:** the **math is deterministic, computed in code — not the LLM**; the status *label* hides
  the slide; the AI shows facts, the RM owns the credit conclusion.
- **Backing golden cases:** `A2-meridian-dscr`, `A2-meridian-cushion`, `A2-meridian-status`,
  `A2-meridian-mislabel`, `A2-arcadia-na` (construction → operating covenants N/A).

### A3 ★ — "Which distressed borrowers have I gone quiet on?"

> **Prompt (verbatim):**
> ```
> Which of my distressed borrowers have I actually gone quiet on? Count days since the last real two-way
> contact — a one-way notice or a missed call doesn't count.
> ```

- **Skill:** `measuring-engagement-coverage` (the creative gem for Deliverable A)
- **MCP tool:** `measure_engagement_coverage`
- **Guards:** §2.1/§5 server-side; `screen_and_finalize` on the narration
- **Returns:** Meridian **78 days** since the last substantive contact (3/14) — vs a naive **33** days
  since the last *any* log entry, because the 4/28 entry was a **one-way overdue notice, not a contact**.
  A 45-day undercount that a "days since last touch" field would hide.
- **The point:** a risk **no single field flags** (distress and engagement diverge); and it's
  **RM-private and dismissible** — which is the direct answer to Sarah's fear of contact-frequency
  surveillance. Labeled an **enhancement** Tom's wf5 couldn't see.
- **Backing golden cases:** `A3-meridian-gap-78`, `A3-meridian-naive-33`, `A3-meridian-asof`,
  `A3-meridian-onewaynotice`, `A3-crestwood-substantive` (the `sent`-in-`presented` regression).

---

## The foundation guards every prompt routes through

| Guard | Where it lives | What it enforces |
|---|---|---|
| **§2.1 restricted-input strip** | MCP server (`guards.strip_record` / `redact_text`) | `credit_grade` removed; watchlist/Special-Assets language redacted in free text — on *every* read, *every* surface |
| **§5 prohibited-borrower gate** | MCP server (`guards.assert_processable`) | Special-Assets/litigation borrower → hard halt |
| **guarantor-document refusal** | MCP server (`guards.refuse_if_guarantor_doc`) | guarantor personal-financial doc → refused |
| **§4.2 output screen** | `screen_and_finalize` MCP tool | blocks credit-characterizing/predictive/recommending language; attaches a qualitative reliability footer (never a %); tags for RM review (§4.3) |

These are the **cross-surface chokepoint** — they run identically in Code and Cowork because they're in
the server, not in (Code-only) hooks.

---

## Production mapping (what we'd wire differently for the bank)

- **Retrieval:** local stdio MCP over `data/` → a **hosted, authenticated remote connector** to the
  bank's loan/CRM systems (read-only scope = a deployment-grade §4.2 guard).
- **Automation:** the on-demand watchlist → a nightly **scheduled pre-compute** that *prepares* the
  Monday list (prepare-only, never auto-act) — gated on **CCO §4.1 approval** before it runs unattended.
- **Observability:** the local `traces/` ledger + `reports/observability.md` → hook-emitted
  **OpenTelemetry → Datadog** (an approved connector) as the §4.1 monitoring evidence.
- **Sub-agent:** `portfolio-early-warning-sweep` (fan-out over borrowers) — narrated as the production
  packaging of `assemble_watchlist`; the demo runs it as a skill composition in the main thread.

---

## Proof it works

- **Deterministic correctness:** `PYTHONPATH=mcp python3 mcp/tests/test_compliance.py` → **46/46**.
- **Golden eval:** `PYTHONPATH=mcp python3 evals/runner.py` → grades **81 source-grounded cases** (all 5
  borrowers + compliance + negatives) against the real tool logic; results in `evals/results/latest.md`.
- **Per-prompt scorecard:** `PYTHONPATH=mcp python3 evals/observability.py` → `reports/observability.md`.
- **In-console (Code *or* Cowork):** ask *"run the evals"* — the **`run_evals` MCP tool** grades the live
  tools, refreshes the scorecard, and returns the pass/fail summary in chat (no terminal). See
  [`../../docs/evals_and_observability.md`](../../docs/evals_and_observability.md).
- **Captured live outputs:** in [`what-changed-vs-wf5.md` §5](./what-changed-vs-wf5.md) (Code + Cowork).
