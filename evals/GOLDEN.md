# Golden set & assessment methodology

**There is no pre-existing golden dataset.** The assignment provides raw data (5 borrowers, CSVs, emails,
one memo), not labels or "correct answers." So we **construct a small golden set**, and keep it credible by
**grounding every expected answer in a checkable source row** (`file:row` / `doc:page`) rather than opinion.

Scope: ~3–5 cases per built skill / per demo prompt. Cases live in `evals/<skill>/cases.jsonl`; the runner
(`evals/runner.py`) grades them with-vs-without and checks assertions; results land in `evals/results/`.

## What "performance" means here (no single accuracy %)
> **performance = compliance + step-correctness + extraction/computation accuracy + generative quality**

Viewable **per demo prompt** and **tracked across runs** in `reports/observability.md`. "Accuracy" is a clean
percentage only where ground truth exists (deterministic / extraction); elsewhere it's assertion-based plus
edit-rate — we never display a fabricated single number.

## The four tiers
- **T1 — Objective ground truth** (right answer verifiable from source). Examples:
  - A2 covenant: `DSCR = 1.03 · BREACH · revolver 85% flagged non-covenant · status-vs-trend mismatch`
  - A3 engagement: `gap = 78 days · 4/28 classified as a one-way notice, not a contact`
  - A1 watchlist: `Meridian ranked #1` · **`Crestwood NOT flagged`** (negative case — pristine)
  - close-the-loop: `3 Meridian commitments surfaced as unmet (Feb-14, 75% revolver cap, watchlist)`
  - reconciliation: `Apr-9 entry flagged mis-dated; Chen guidance surfaced; 75% condition unmet`
  - doc-intel: `3 docs missing (PO, AR names, projections) · rep letter unsigned · guarantor refused` (ground truth **by construction** — we authored the synthetic package)
- **T2 — Compliance assertions** (binary, hard): §2.1 field absent · guarantor doc refused · §5 SA borrower halts · no credit-adjacent language · every claim cited · memo has an RM-authored assessment.
- **T3 — Agentic-pattern / expected-trace** (grades the *orchestration*, not the text): each prompt declares its expected skill/tool/guard sequence; we compare it to the actual `traces/run-<id>.jsonl` ledger → catches a wrong skill firing or a skipped step. Critical steps are deterministic, so they're enforced + logged.
- **T4 — Generative quality** (no single right answer — emails, memos, briefs): rubric / property assertions (right items present, §4.3-tagged, no credit language) + the reliability footer + (in production) the **HITL edit-rate**. Optional LLM-as-judge against a rubric, with the §4.2 caveat that it's a signal, not ground truth.

## Negative / adversarial cases (to catch over-firing)
A clean borrower must **not** be flagged; a normal document must **not** be refused; a §2.1 field must be
absent from any model input.

## Honest limits
Small, self-authored, on synthetic/assignment data → risk of "grading our own homework." Mitigations:
source-grounded expected answers, negative/adversarial cases, and explicit disclosure of scale. **Production
path:** a larger labeled set, real RM feedback (accept / edit-distance / dismiss), and A/B — narrated, not
claimed.
