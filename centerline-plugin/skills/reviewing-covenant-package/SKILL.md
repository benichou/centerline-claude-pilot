---
name: reviewing-covenant-package
description: Use when an RM hands you an incoming covenant / financial-reporting package (a folder of PDFs) and asks "what's in here / what's missing / does it reconcile?" — e.g. Sarah's Meridian Q1 package just arrived. Classifies each document, refuses restricted ones, extracts the figures, recomputes the covenant ratios, and reports completeness + quality as facts, with every figure cited to its source.
---

# Reviewing an incoming covenant package

The framing: the borrower finally sent the package the RM has been chasing. Your job is the **intake
review** — sort it, pull the numbers, reconcile them, and say what's still outstanding. The **model reads
the PDFs; deterministic `centerline` tools decide** (the arithmetic and the compliance call are never
yours to eyeball). Everything you report is a **fact (§4.2)** — you never characterize creditworthiness;
the RM owns that.

**Provenance is the whole point.** This RM (Sarah) was burned by an earlier AI pilot that gave wrong
covenant information, so trust here means *"here is exactly where this number came from"* — never a
confident tone. **Cite every figure to its document + field + the tool that derived it. Assert nothing
you can't trace.** The tools below return that provenance for you (`sources`, `derivation`,
`confidence_band`); your job is to surface it, not hide it.

Pass **repo-relative paths** (e.g. `data/synthetic/meridian-package/<file>.pdf`) — the MCP server resolves
them against the repo root on the host, so this works identically in Claude Code and Cowork.

## Steps

1. **List the package.** Call the `centerline` MCP tool **`list_documents(directory)`** (for the demo:
   `data/synthetic/meridian-package/`) — it enumerates the real files **host-side**, so don't guess
   filenames and don't try to `ls` the folder yourself (that triggers a Cowork folder-access prompt).
   Classify each entry in the returned `pdfs` list.

2. **Classify each document** — call `classify_document(path)` per file. Each result carries provenance:
   the `document`, the model's `rationale` + `key_signals`, and a qualitative `confidence_band`
   (high/medium/low). **Narrate the band qualitatively — never a numeric %.**
   - A **guarantor personal financial statement is refused on intake** (§2.1) — `refused: true`, the
     document is **never sent to a model**. Report the refusal; do not re-classify or extract it.
   - A misfiled document (e.g. an ACORD **Certificate of *Insurance***) classifies as **`other`** — not
     part of the covenant package, skipped at extraction.

3. **Extract fields** for each extractable doc — `extract_document_fields(path, doc_type)` using the
   `doc_type` from step 2. `other` / purchase orders / projections come back **skipped**; the guarantor
   doc stays **refused**. Keep the returned `extracted` dicts.

4. **Cross-validate the ratios (the headline).** With the covenant **certificate** and **financial
   statement** extractions, call `cross_validate_covenant(certificate, financials, borrower)`. It
   recomputes DSCR/leverage on the **unadjusted (GAAP)** financials, compares to what the certificate
   **certifies**, corroborates against the bank's `loan_performance`, and surfaces the **EBITDA add-back
   bridge**. Each `findings` entry comes with `sources` (document + field + value); each recomputed ratio
   comes with a `derivation`. **Present the finding AND its source** — e.g. *"recomputed DSCR 1.03 = GAAP
   EBITDA 10,100 [financial_statement] ÷ debt service 9,800 [financial_statement]; certified 1.23
   [covenant_compliance_certificate]; bank loan_performance 1.03."* It also returns
   `cross_source_mismatches` — keep it for step 6.

5. **Completeness + quality.** Call `review_package(items, borrower)` with one entry per document
   (`{doc_type, path, extracted, refused, skipped}`). It returns **missing documents**, **outstanding data
   elements**, **quality flags** (unsigned rep letter, withheld A/R names) — each tagged with its `source`
   (document + field + value) — the **§2.1 refusals**, and a `low_confidence_inputs` list. Keep the latter
   for step 6.

6. **Compose + screen.** Write a short intake readout with a **source on every figure** (document + field
   + tool) and a brief **"Sources & basis"** close — invoke `grounding-claims-to-source`. Then route the
   readout through **`screen_and_finalize`**, passing the provenance through so the reliability footer is
   honest:
   - `cross_source_mismatches=` the list from step 4 (the certified-vs-recomputed gaps),
   - `low_confidence_inputs=` the list from step 5 (missing docs, unsigned letter, withheld names).
   With real mismatches/low-confidence inputs the footer will correctly read **Partial** (not "Grounded ·
   0 issues") — that honesty is the point. Then call **`render_pdf(text=finalized_text, title="Meridian
   Fabrication — Q1 2025 Covenant Package — Intake Readout", output_path="reports/pdf/meridian-q1-intake-readout.pdf")`**
   to emit a credit-file-grade PDF (banner + footer preserved; `render_pdf` auto-appends a UTC timestamp so
   each save is a unique file — pass the plain base name) — **keep showing the markdown readout inline
   too**; the PDF is an additional output. The natural next step is a missing-docs email — hand off to
   `drafting-rm-communications`.

## Keep it factual (§4.2)
"Recomputes to 1.03, below the 1.20 minimum" and "rep letter is unsigned" are **facts** — state them with
their source. "High risk", "likely to breach", "they're hiding the AR" are **not** — don't write them. The
catches here (overstated certification, missing items, unsigned letter, §2.1 refusal) are surfaced **with
their provenance** for the RM to judge, not judged for them.

## Note on cost
`classify_document` / `extract_document_fields` make real Anthropic API calls (model set by
`CENTERLINE_DOCINTEL_MODEL`, default Sonnet 4.6) and read `ANTHROPIC_API_KEY` from the server's
environment. `cross_validate_covenant` and `review_package` are deterministic — no API, no cost.
