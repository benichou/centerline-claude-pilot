# Deliverable B — the recipe (exact prompts + agent design)

> The brief asks for **"exact prompts / agent design"** — verbatim, not paraphrased — and **real
> outputs**. This is that artifact for Track B (Relationship Review & Renewal Prep + the
> document-intelligence cluster). It is a **living log**: each demo beat's prompt is recorded here
> **verbatim, as it is actually run in Cowork**, with what it exercised and the captured output.
>
> **Status:** B2 (Meridian package intake → missing-docs email) is **built + Cowork-verified** and recorded
> below. B1 (Crestwood retention), B3 (Arcadia reconciliation + draw letter), B4 (Summit memo) are pending
> — their verbatim prompts + outputs get appended here when they're run, not invented ahead of time.

---

## How it runs (agent design, in one picture)

Like Track A, Track B is a library of **composable skills** the model auto-selects, each backed by a
**deterministic** or **schema-forced** MCP tool. For doc-intelligence the split is explicit: **the model
reads the PDFs; deterministic code decides** (recompute, cross-validate, completeness, quality), and
**every figure is provenance-tagged** because this RM (Sarah) was burned by an unreliable AI pilot.

```
  RM types a prompt (Cowork or Code)
        │
        ▼
  list_documents(dir) ──► enumerate the package host-side (no guessing, no sandbox grant)
        │
        ▼
  classify_document(path) per file ──► §2.1 guarantor PFS refused on intake (never sent to a model)
        │                              ACORD insurance cert → `other` (skipped)
        ▼
  extract_document_fields(path, type) ──► schema-forced structured fields (temp 0)
        │
        ▼
  cross_validate_covenant(cert, financials) ──► certified vs recomputed-GAAP vs bank loan_performance
        │                                        + the EBITDA add-back bridge; every figure sourced
  review_package(items) ──► completeness + quality + §2.1 refusals; emits low_confidence_inputs
        │
        ▼
  screen_and_finalize(text, cross_source_mismatches=…, low_confidence_inputs=…)
        │      └─► §4.2 block + HONEST reliability footer (Partial when ratios diverge / docs missing)
        ▼
  render_pdf(finalized_text) ──► credit-file-grade PDF (banner + footer preserved), reports/pdf/<name>_<UTC>.pdf
        │
        ▼
  markdown inline + PDF artifact ──► RM reviews (§4.3); hand off to drafting-rm-communications for the email
```

**Load it:** same as Track A — Code via `--mcp-config .mcp.json --plugin-dir ./centerline-plugin`; Cowork
via the `claude_desktop_config.json` MCP bridge + the uploaded `centerline-plugin.zip`. The doc-intel
tools read `ANTHROPIC_API_KEY` from a gitignored repo-root `.env`.

**Creative identity (vs the brief's "avoid" list):** the brief says Deliverable B must NOT headline memo
drafting / covenant-package tracking / overdue emails. Track B's *creative* claim is the **non-obvious
find** — close-the-loop + reconciliation + retention (B1/B3). The doc-intel package review (B2) and the
memo (B4) are positioned as the **compliant cleanup of Tom's remaining shadow workflows + persona
coverage** — and as the **provenance/compliance showcase** — not the creativity claim.

---

## B2 (Sarah) — Meridian Q1 covenant-package intake → missing-docs email  ✅ Cowork-verified 2026-06-13

### B2a — "what's in it, what's missing, do the ratios reconcile?"

> **Prompt (verbatim):**
> ```
> Sarah's Meridian Q1 covenant package just arrived in data/synthetic/meridian-package/. Review it —
> what's in it, what's missing, and do the ratios reconcile?
> ```

- **Skill:** `reviewing-covenant-package`
- **MCP tools (in order):** `list_documents` → `classify_document` (×6) → `extract_document_fields` (×4) →
  `cross_validate_covenant` → `review_package` → `screen_and_finalize` → `render_pdf`
- **Guards:** §2.1 guarantor refusal on intake (deterministic pre-screen, never sent to a model); §4.2
  output screen; reliability footer; §4.3 RM-review tag
- **Returns (captured):**
  - **Inventory (6 docs):** covenant certificate (signed, D. Kwan CFO 2025-04-18), financial statement
    (TTM 3/31/25), A/R aging ($9,800k), management representation letter — all `extracted`; ACORD
    Certificate of *Insurance* → **`other`, skipped**; guarantor personal financial statement →
    **refused on intake (§2.1), never read**.
  - **Reconciliation (the headline) — No:** certified **DSCR 1.23 / leverage 3.76** (both pass) vs
    recomputed **1.03 / 4.50** (both breach), the gap entirely a **$2,000k EBITDA add-back bridge**
    (Adjusted 12,100 vs GAAP 10,100); the bank's own `loan_performance` (2025-05) shows **1.03 / 4.50**,
    matching the recompute. **Every figure cited to its document + field + tool** (e.g. *"DSCR 1.03 = GAAP
    EBITDA 10,100 ÷ debt service 9,800 [financial_statement: ebitda_gaap / total_debt_service]"*).
  - **Missing / outstanding:** aerospace purchase order, updated 12-month projections, A/R customer names
    (60–90 day balances withheld). **Quality:** rep letter **unsigned**; A/R names withheld.
  - **Reliability footer: `Partial`** — with the certified-vs-recomputed mismatches + missing/unsigned
    inputs as the stated reasons (NOT a false "Grounded · 0").
- **Output artifacts:** markdown readout rendered inline **+** PDF `reports/pdf/meridian-q1-intake-readout_<UTC>.pdf`
  (DRAFT/§4.3 banner + Partial footer + the covenant table preserved).
- **The point:** the model reads, **deterministic code decides**; **nothing is asserted without a source**
  (Sarah's trust scar); the §2.1 refusal is **enforced, not a disclaimer**; the footer is **honest about
  its own reliability**.

### B2b — "draft the missing-documents email"

> **Prompt (verbatim):**
> ```
> Draft the missing-documents email to Meridian.
> ```

- **Skill:** `drafting-rm-communications` [wf3]
- **MCP tools:** `screen_and_finalize` → `render_pdf`
- **Returns (captured):** a **DRAFT** email to **David Kwan, CFO**, requesting the four outstanding items
  (signed representation letter, A/R customer detail for the 60–90 day balances, aerospace purchase order,
  cash-flow projections), **< 200 words**, facts-and-requests only — **no breach/credit-status
  characterization**, no add-back/recompute reference, **no mention of the guarantor doc** (a neutral line
  notes the guarantor personal financials can't be accepted through this channel). Tagged **Requires RM
  review (§4.3)**.
- **Output artifacts:** inline draft **+** PDF `reports/pdf/meridian-q1-missing-docs-email_<UTC>.pdf`.
- **Reliability footer: `Grounded · 0 issues`** — and that's *correct*: the email asserts nothing
  reliability-dependent (it requests documents). The contrast with B2a's **Partial** shows the footer is
  calibrated, not rubber-stamped.
- **The point:** the package review **tells the letter what to ask for**; the compliant rebuild of Tom's
  wf3 (facts + requests, RM delivers any bad news, human gate before sending).

---

## B1 (Tom) — Crestwood prep + retention  ⏳ pending — record verbatim prompt + output when run
## B3 (Tom) — Arcadia reconciliation + close-the-loop + draw-response letter  ⏳ pending
## B4 (Marcus) — Summit annual relationship-review memo (decomposed §4.2)  ⏳ pending

---

## The foundation guards every prompt routes through

Same cross-surface chokepoint as Deliverable A (see
[`../deliverable-a/recipe.md`](../deliverable-a/recipe.md)): §2.1 strip + §5 gate + guarantor refusal in
the MCP server; §4.2 output screen + reliability footer + §4.3 tag via `screen_and_finalize`. For Track B
the **§2.1 guarantor refusal is a deterministic filename pre-screen *before* any API call**, and
`screen_and_finalize` is fed `cross_source_mismatches` + `low_confidence_inputs` so the footer is honest.

## Production mapping (what we'd wire differently for the bank)

- **Doc source:** local `data/synthetic/` PDFs → a hosted, authenticated document store / imaging system
  (read-only scope). Real covenant packages are §2.3-residency-sensitive → on-prem / self-hosted model.
- **Doc-intel model:** Sonnet 4.6 default (cost lever) → tune per accuracy; the §2.1 pre-screen + the
  deterministic recompute/cross-validate stay regardless of model.
- **Sub-agent:** `covenant-package-review` (fan-out over many docs) — narrated as the production packaging;
  the demo runs the pipeline as a skill composition in the main thread.

## Proof it works

- **Deterministic correctness (no API):** `PYTHONPATH=mcp uv run python mcp/tests/test_docintel.py` →
  **45/45** (prescreen, classify/extract dispatch, provenance, footer tie-in, confidence band,
  list_documents, render_pdf incl. timestamp + title de-dupe). Compliance suite **50/50**.
- **Live, captured:** the B2 run above (Cowork) — readout + email + the two PDFs in `reports/pdf/`.
