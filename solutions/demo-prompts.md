# Panel demo — the run-of-show (single source of truth for the prompts)

> The exact prompts we display in the 1-hour panel, **in order**, with status and what each shows. This is
> the **panel script**; the per-deliverable recipes hold the deeper agent design + captured outputs:
> [`deliverable-a/recipe.md`](./deliverable-a/recipe.md) (Track A) ·
> [`deliverable-b/recipe.md`](./deliverable-b/recipe.md) (Track B).
>
> **Status key:** ✅ **built + run verbatim** (wording is final, recorded in a recipe) · ◐ **planned**
> (working wording; finalized + recorded in the recipe when the beat is built).
> **Build in Claude Code → demo in Claude Cowork** (RM-facing surface). Every output routes through
> `screen_and_finalize` (§4.2 + reliability footer + §4.3 tag) and can be rendered to a PDF (`render_pdf`).

---

## 0–5 min — FRAME  *(narration, no prompt)*
The situation (3 RMs / $350M / 30–40% on docs); Tom's shadow ChatGPT workflow the IT audit flagged; "before I type: credit grade / watchlist / Special-Assets are stripped at retrieval (§2.1, server-side); everything is RM-private; every number traces to a source."

## 5–25 min — DEMO 1 · TRACK A = Deliverable A (Portfolio Risk & Early-Warning)
*Region 1 · rebuild of Tom's wf5 · §4.1, RM-private · all ✅ (verbatim in `deliverable-a/recipe.md`).*

**A1 — "who needs attention?"** ✅
```
Who in my portfolio needs attention this week? Rank them and show me the facts behind each — don't
characterize their credit, just the numbers and the gaps.
```
*Shows:* watchlist ranked by risk × neglect (Meridian #1 → Crestwood last); ranks, doesn't judge (§4.2); every line cited.

**A2 — "Meridian compliant? cushion + trend"** ✅
```
Is Meridian covenant-compliant as of the latest month? Show DSCR and leverage against their covenant
thresholds with the cushion, the revolver level, and whether the reported status matches the trend.
```
*Shows:* DSCR 1.03 vs 1.20 (cushion −0.17, BREACH), leverage 4.5 vs 4.0, revolver 85% (non-covenant), the status label lagging the slide; math is deterministic, not the LLM.

**A3 ★ — "who have I gone quiet on?"** ✅  *(Deliverable A's gem)*
```
Which of my distressed borrowers have I actually gone quiet on? Count days since the last real two-way
contact — a one-way notice or a missed call doesn't count.
```
*Shows:* Meridian 78 days (not the naive 33) — a risk no field flags; RM-private/dismissible (answers Sarah's fear).

→ **Bridge** *(narration):* "flag ≠ action" — Tom's wf5 flagged Crestwood and he still lost it. Motivates Track B.

## 25–50 min — DEMO 2 · TRACK B = Deliverable B (Relationship Review & Renewal + Doc-Intel)
*Region 2 · one beat per RM · order is real-data-first (B2/B3 real; B1/B4 round out persona coverage).*

**B1 (Tom) — Crestwood prep + retention** [wf4] ✅ *Cowork-verified 2026-06-13 (v0.8.0)*
```
Prep me for my Crestwood meeting — pull the relationship picture, the renewal/maturity clock, and the
competitive situation; flag anything I should act on before they shop us.
```
*Shows:* the "healthy-but-leaving" radar — the risk Track A is blind to; surfaces facts (maturity 457d out, First Midwest 4.90% term sheet, attrition noted) + "engage", **never a rate** (§4.2). *Skill: `flagging-renewal-and-retention`; tool: `flag_renewal_and_retention`. Gem: retention.*

**B2 (Sarah) — Meridian Q1 package intake** ✅  *(in `deliverable-b/recipe.md`)*
```
Sarah's Meridian Q1 covenant package just arrived in data/synthetic/meridian-package/. Review it —
what's in it, what's missing, and do the ratios reconcile?
```
*Shows:* §2.1 guarantor refusal on intake; ACORD cert → `other`/skipped; certified 1.23/3.76 vs recomputed 1.03/4.50 via the $2,000k add-back bridge, corroborated by loan_performance; missing PO/projections/A/R-names; unsigned rep letter; **every figure cited**; **Partial** reliability footer; PDF rendered.

**B2 cont. — missing-docs email** [wf3] ✅
```
Draft the missing-documents email to Meridian.
```
*Shows:* DRAFT to David Kwan, 4 items, < 200 words, no breach/credit language, §4.3 review tag; the review tells the letter what to ask for.

**B3 (Tom) — Arcadia reconciliation + close-the-loop** ✅ *Cowork-verified 2026-06-13 · Deliverable B's headline gem*
```
Reconcile Arcadia's email thread against the CRM log — what actually happened, what's mis-dated, what
decision isn't in the file, and what's still open?
```
*Shows:* the Apr-9 mis-dated/conflated entry (visible on the deterministic merged timeline); Chen's credit guidance that's email-only, surfaced verbatim + attributed (scribe-not-author); the 75% condition still open (pre-lease 71%). *Skills: `detecting-cross-source-discrepancies` + `verifying-commitment-fulfillment`; tool: `get_relationship_timeline`. Gem: close-the-loop + reconciliation.*

**B3 cont. — draw-response letter** [wf1] ✅ *Cowork-verified 2026-06-13*
```
Draft the draw-response letter for Arcadia.
```
*Shows:* requests the outstanding items the reconciliation surfaced (incl. executed leases + tenant names per Chen's condition); §4.3 review.

**B4 (Marcus) — Summit annual relationship-review memo** [wf2, decomposed §4.2] ✅ *Cowork-verified 2026-06-13 (v0.8.0)*
```
Build my Summit annual relationship-review memo.
```
*Shows:* AI assembles the 17-month data + contacts + open items (the 80%), **pauses for the RM's own assessment**, drafts narrative around the RM's words (§4.2) — wins the skeptic without changing how he thinks. *Skill: `drafting-relationship-review-memos`.*

## 50–55 min — HONEST EVAL (80/20)  *(narration, no prompt)*
Works = grounded/compliant/reusable; hard 20% = flag≠action, data-quality limits, A blind to Crestwood/Arcadia, doc-intel on synthetic docs.

## 55–60 min — SYSTEM / GOVERNANCE / ADOPTION

**Eval display — "show me the latest agent eval"** ✅
```
Show me the latest agent eval.
```
*Shows:* `viewing-eval-results` → the Layer-3 agent-behavior results (pulls fresh via `get_latest_report`).

**Governance display — "latest proposed improvements"** ✅
```
Show me the latest proposed improvements to our skills and automations.
```
*Shows:* `viewing-proposed-improvements` → the Layer-4 advisory report (incl. the live A1 §4.2 finding we intentionally left unapplied); the human-proposes / human-disposes governance loop.

**Optional in-console proof — "run the evals"** ✅
```
Run the evals.
```
*Shows:* the `run_evals` MCP tool grades the live tools + refreshes the scorecard, in chat, no terminal.

**Narrated, not typed:** the scheduled-jobs adoption beat — Sarah's Monday pre-compute, the CCO early-warning sweep, Tom's wf5 on a cadence (prepare-only / §4.3; monitoring → CCO §4.1; local > cloud for §2.3 residency).

---

## Tally
~11 displayed prompts — **ALL built + Cowork-verified (2026-06-13, plugin v0.8.0):** A1, A2, A3, B1, B2 (×2), B3 (×2), B4, the two eval/governance display prompts (+ optional `run the evals`). Scheduled-jobs is narrated, not typed. *(One eyeball pending: confirm the B1 Crestwood brief makes no rate recommendation.)*
