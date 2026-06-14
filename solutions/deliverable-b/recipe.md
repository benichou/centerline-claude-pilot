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

## B1 (Tom) — Crestwood prep + retention  ✅ Cowork-verified 2026-06-13

*The retention gem — the inverse of early-warning: the healthy borrower a competitor is courting is the
one you LOSE, and distress monitoring is blind to it. Real data.*

> **Prompt (verbatim):**
> ```
> Prep me for my Crestwood meeting — pull the relationship picture, the renewal/maturity clock, and the
> competitive situation; flag anything I should act on before they shop us.
> ```

- **Skills:** `flagging-renewal-and-retention` (+ `building-client-360` for the dossier; optionally
  `get_relationship_timeline` for how the renewal unfolded)
- **MCP tool:** `flag_renewal_and_retention` (deterministic — reuses `check_covenant_compliance` +
  `detect_deterioration_signals` for the health read, computes the maturity clock, scans the record for
  renewal/competitive signals)
- **Expected (grounded in real Crestwood data):** **`retention_attention: true`** — Growth-tier, pristine &
  improving (DSCR 2.45→2.61, leverage 0.82→0.73, 0% revolver, AUM $2.1B→$2.31B; **0 deterioration
  signals**); matures **2026-08-31** (**457 days** out); a **First Midwest 4.90% term sheet** vs Centerline's
  5.25% on record since Feb-2025; renewal stalled (vague reply → missed 3/18 call → proposal only 4/15 →
  pricing exception pending 5/12); the 5/31 note flags **attrition risk**. The radar surfaces these as
  **facts** and flags **"engage / prioritize the renewal"** — and **never recommends a rate** (the pricing
  committee owns that; the RM already submitted a 4.90% exception). Footer Partial; §4.3.
- **The point:** **inverts the lens** — catches the healthy client Track A is structurally blind to (serves
  the RM's retention/cross-sell mandate). The **"flag ≠ action"** honest-eval lands here: Tom's wf5 flagged
  the gap and he *still* nearly lost a $2.31B-AUM relationship to inaction.
- **Captured (2026-06-13 Cowork run):** ran end-to-end — retention radar → dossier + relationship timeline
  → screened meeting-prep brief rendered to `crestwood-meeting-prep.md` + a PDF. *(Quick eyeball before the
  panel: confirm the brief recommends "engage / prioritize the renewal" but makes NO rate recommendation —
  pricing stays with the committee, §4.2.)*

## B3 (Tom) — Arcadia reconciliation + close-the-loop → draw-response letter  ✅ Cowork-verified 2026-06-13 (B3a + B3b)

*Deliverable B's headline creative gem — runs on REAL data (no synthetic docs).*

> **Captured (B3a, 2026-06-13 Cowork run):** all catches landed — the **Apr-09 mis-dating** ("~13 days
> before… makes the file look 13 days fresher than it is"); **Chen's 2025-04-25 ruling quoted verbatim +
> attributed** with a propose-only CRM entry offered (scribe-not-author); the **open** items (Friday docs
> undelivered, names withheld, the call unverifiable, **71% < 75%** via `detect_deterioration_signals`);
> the completion-date contradiction; footer **`Partial · 4 low-confidence · 5 cross-source mismatches`**,
> §4.3-tagged. **Bonus (unscripted, source-grounded):** the model also caught that the CRM **skips Draw #12
> + a Feb-2025 draw** — both present in `loan_performance` (2024-12 "Draw #12 funded", 2025-02 "Draw
> funded") but absent from the activity log → a real record gap it found by cross-referencing, not designed
> for. **Note:** this run was on plugin v0.5.0 where the readout PDF was *optional* (the agent correctly
> offered it); v0.6.0 makes the reconciliation readout **auto-render** to PDF (consistent with B2).

### B3a — "reconcile Arcadia's emails vs the log"

> **Prompt (verbatim):**
> ```
> Reconcile Arcadia's email thread against the CRM log — what actually happened, what's mis-dated, what
> decision isn't in the file, and what's still open?
> ```

- **Skills:** `detecting-cross-source-discrepancies` + `verifying-commitment-fulfillment` (close-the-loop)
- **MCP tools:** `get_relationship_timeline` (the deterministic anchor — merges the CRM log + the email
  messages into one chronological, source-tagged list, §2.1-redacted) + `get_emails` + `get_activity_log`
  + `detect_deterioration_signals` (construction: pre-leasing vs the 75% perm-conversion threshold)
- **Expected (grounded in the real Arcadia record):**
  - **Mis-dated / conflated entry:** the single CRM entry dated **2025-04-09** ("Draw #13 submitted, 91%,
    pre-leasing 71%, escalated to Marcus Chen") sits **~2 weeks before** the actual Draw #13 thread
    (**2025-04-22 → 25**) and collapses a four-message exchange into one back-dated row — visible on the
    merged timeline (the Apr-09 log row sorts before the Apr-22 submission email).
  - **Email-only credit decision (scribe-not-author):** Marcus Chen's **2025-04-25** ruling — *"fund the
    draw; don't waive the 75% threshold; the LOIs need to be executed and we need tenant names for our
    file; … if the long-term picture is 71-73%, that's a different underwriting story than what we
    approved"* — is **entirely in email, not the log** (which only says "escalated to Chen"). Surfaced
    **verbatim + attributed**, with a proposed CRM entry for the RM to approve.
  - **Open commitments (close-the-loop):** Liang's "items 1, 2, 3 by Friday" (Q1 inspector report, GC
    revised schedule, executed MEP lien waivers) — no record of receipt → **open**; Chen's "don't waive
    75% + tenant names in file" → **open/live** (pre-leasing **71% < 75%** via `detect_deterioration_signals`;
    2 of 3 LOIs name-withheld); Chen's "get a call with Liang this week" → **unverifiable** (no log);
    Liang's "75% within 60 days" → tracked expectation.
  - **Figure/date contradiction:** completion **"end of July"** (Apr-22 email) vs **"Q4 2025"** (2024-12-04
    log) vs the original Q3 2025 target.
  - **Footer:** `Partial` (cross-source mismatches + unverifiable items passed to `screen_and_finalize`).
- **The point:** the system connects sources **no one reconciles** and surfaces **the bank's own dropped
  follow-through** + the most consequential credit decision that never reached the file — as **facts**,
  with the human's words quoted, not the AI's. Construction-lifecycle-aware (operating covenants N/A; the
  signal is pre-leasing vs 75%).

### B3b — "draft the draw-response letter"

> **Prompt (verbatim):**
> ```
> Draft the draw-response letter for Arcadia.
> ```

- **Skill:** `drafting-rm-communications` [wf1] → `screen_and_finalize` → `render_pdf`
- **Expected:** a **DRAFT** to Robert Liang requesting the outstanding items the reconciliation surfaced
  (Q1 inspector report, GC revised schedule, executed MEP lien waivers, and the executed leases / LOIs
  **with tenant names** for the pre-lease summary), stating the 75% perm-conversion documentation
  requirement as a **fact** — no credit characterization, no waiver/commitment the RM hasn't authorized;
  tagged **Requires RM review (§4.3)**.
- **The point:** the reconciliation **tells the letter what to ask for** (per Chen's condition: executed
  leases + tenant names, not verbal LOIs).
- **Captured (2026-06-13 Cowork run):** to Liang, the four outstanding items (3 numbered + the pre-lease
  documentation paragraph); states the 75% perm-conversion documentation requirement (executed leases /
  LOIs with tenant name + sq ft + rent psf; verbal/name-withheld LOIs don't count) as a **fact**; **keeps
  Chen's internal "different underwriting story" reasoning OUT of the client letter**; no waiver / rate /
  approval / timeline commitment (softened "we'll move quickly" → "we'll process the conversion review");
  DRAFT/§4.3, footer **Partial · 2 low-confidence inputs**, PDF rendered. *(Demo wording: "Draft the
  draw-response letter for Arcadia."; this run was triggered by accepting the skill's follow-up offer.)*

## B4 (Marcus) — Summit annual relationship-review memo (decomposed §4.2)  ✅ Cowork-verified 2026-06-13

*The skeptic's wedge — the compliant rebuild of Tom's wf2 (single-prompt memo). AI assembles ~80%; the RM
owns the ~20% that is the credit call.*

> **Prompt (verbatim):**
> ```
> Build my Summit annual relationship-review memo.
> ```

- **Skill:** `drafting-relationship-review-memos` (composes `building-client-360` + `get_loan_performance` +
  `check_covenant_compliance` / `detect_deterioration_signals` + `get_activity_log`)
- **Expected flow:** (1) **ASSEMBLE** the factual sections — relationship overview, 17-month performance
  trend, covenant status, engagement summary, open items — every line cited, no credit characterization;
  (2) **⏸ STOP** and ask Marcus for his assessment *in his own words* (the AI does **not** generate it —
  the §4.2 line); (3) **DRAFT** the narrative around his verbatim, attributed assessment; (4)
  `screen_and_finalize` + `render_pdf` + §4.3.
- **The point:** §4.2 origination made concrete — the AI removes the assembly burden (~71 memos/yr for
  Marcus) **without authoring the judgment**; the assessment section must be **RM-authored and non-empty**.
- **Honest note:** Summit is **thin** (sparse logs, no prior memo) so the assembled sections are lighter
  than a well-documented borrower, and in the demo the RM assessment is **simulated** to show the pause.
- **Captured (2026-06-13 Cowork run) — the strongest §4.2 moment:** the skill assembled the factual
  sections (17-mo performance trend, covenant test, deterioration signals, contact history — all cited),
  then **STOPPED and rendered an interactive form** asking for the RM's own read: *"In your own words —
  what's your assessment of this relationship and the credit? … this goes into the memo as your
  assessment, attributed to you. I won't write or paraphrase it,"* plus an **outlook** chip
  (Positive / Stable / Watch-monitor / Other) and a next-steps box. It explicitly held: *"the memo isn't
  complete without your read, so I'll hold here until you submit."* That is §4.2 origination made literal —
  the AI does the assembly; the human authors the credit judgment. **Demo line:** *"notice the AI made me
  write the assessment — it never characterizes the credit itself."*
- **Sample RM assessment used for the demo (Marcus's voice — simulated; a genuine credit judgment the AI
  must NOT make):** *"Coverage has thinned to 1.12x, just above the 1.10x floor, but I read this as seasonal
  softness in the retail book plus known margin pressure at the two weaker locations — not a structural
  decline. The business still covers its debt service and leverage at 3.6x leaves real cushion. My real
  concern is commercial, not credit: the Location 3 lease renewal at an 18% bump could put that unit
  underwater, and Castillo has sounded more stressed than usual on the last couple of calls. I want eyes on
  the Q2 package and the Location 3 outcome before I move my view. Net: still performing, but watch
  closely."* · outlook = **Watch / monitor** · next steps = *"resolve the Location 3 lease (model the
  downside at +18%); covenant check-in before the July package; in-person visit with Castillo this
  quarter."* The drafted memo places this **verbatim + attributed**, facts organized around it.

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
