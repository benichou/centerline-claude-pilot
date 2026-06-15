# Skills & MCP glossary, panel reference

A grounded reference for the hour: how the **19 skills** cluster by capability, what each skill is and how it
works, and what the **local MCP server** and its **19 tools** are and achieve. Pairs with the three appendix
slides at the end of the deck.

> One sentence to anchor it all: **the skills orchestrate and narrate; the MCP tools do the math and enforce
> compliance.** A skill decides *what* to do; a tool does the deterministic, compliance-bound *work*.

---

## Part 1 · Skills mapped by functional capability

Eight functional clusters. Within a cluster the skills share an **intent** and an **output shape**; across
clusters they differ in what they read and what they produce.

| Cluster | Skills | Shared intent | Output |
|---|---|---|---|
| **1. Compliance & trust foundation** (cross-cutting guards) | grounding-claims-to-source · assessing-output-reliability · redacting-restricted-fields · screening-and-gating-output | Make every artifact safe and trustworthy by construction | Cited claims · qualitative reliability footer · restricted inputs removed · §4.2 screen + §4.3 tag |
| **2. Risk & early-warning** (Track A, deterministic) | checking-covenant-compliance · detecting-deterioration-signals · measuring-engagement-coverage · assembling-watchlist-triage | Surface distress from raw signals, as facts | Compliance/trend readouts · engagement gap · ranked watchlist |
| **3. Relationship, renewal & reconciliation** (Track B, the creative core) | flagging-renewal-and-retention · detecting-cross-source-discrepancies · verifying-commitment-fulfillment | Catch what metrics miss: attrition, an untrustworthy record, dropped follow-through | Retention radar · reconciliation readout · close-the-loop status |
| **4. Document intelligence** (Track B) | reviewing-covenant-package | Read an incoming package, refuse restricted docs, reconcile the ratios | Provenance-tagged intake readout |
| **5. Context & synthesis** | building-client-360 | Consolidate a borrower across all sources, flag what's missing | 360 dossier with coverage gaps |
| **6. Drafting / client output** | drafting-rm-communications · drafting-relationship-review-memos | Turn facts into a client-ready or file-ready document | Letters/emails · the §4.2-decomposed memo |
| **7. CRM enrichment** | updating-the-crm | Capture a contact into the record, propose-only | Proposed CRM note + tasks (RM approves) |
| **8. Eval & governance** | running-the-eval-suite · viewing-eval-results · viewing-proposed-improvements | Measure the system and surface proposed changes for a human | Scorecards · advisory improvement proposals |

### Easily-confused pairs (have the distinction ready)
- **checking-covenant-compliance vs detecting-deterioration-signals:** the first is a **snapshot** (latest month vs the threshold, with cushion); the second is the **trajectory** (the full-history trend, threshold crossings, the status-vs-trend mislabel). "Where you stand" vs "where you're heading."
- **detecting-cross-source-discrepancies vs verifying-commitment-fulfillment:** the first is a **data-integrity / reconciliation** check ("the record is wrong or incomplete: mis-dated, contradictory, email-only"); the second is an **accountability** check ("the plan was not executed: which commitments are met / unmet / open"). One fixes trust in the file; the other audits follow-through.
- **assembling-watchlist-triage vs flagging-renewal-and-retention:** **inverses.** The watchlist surfaces **distress** (and is structurally blind to a healthy borrower who is leaving); the retention radar surfaces the **healthy** borrower at attrition risk that the watchlist misses.
- **grounding-claims-to-source vs assessing-output-reliability vs screening-and-gating-output:** grounding = **cite each claim** (input-side trust); reliability = **summarize how trustworthy the whole artifact is** (the footer); screening = **block credit-adjacent language + tag for review** (output-side §4.2/§4.3). Three different guards on the same artifact.
- **viewing-eval-results vs viewing-proposed-improvements:** "how is it doing?" (the scorecard) vs "what should we change?" (the improvement loop's proposals). Both display-only.
- **drafting-rm-communications vs drafting-relationship-review-memos:** a client-facing **message** (factual, no credit bad-news) vs an internal **memo** that wraps the RM's own credit assessment (the §4.2 human pause).

### Reference vs orchestrating skills
- **Behavioral / reference** (shape how every other skill behaves, may not call a tool directly): grounding-claims-to-source, assessing-output-reliability, redacting-restricted-fields, screening-and-gating-output.
- **Orchestrating** (drive a workflow, compose tools): everything else.

---

## Part 2 · Skills glossary (definition + how it works)

Each entry: **what it achieves** · **how it works** · **compliance posture**.

**Foundation / trust (cross-cutting)**
- **grounding-claims-to-source** — *Achieves:* every fact, figure, or claim points to its source. *How:* cites each claim to `file:row` / `doc:page` / email line; if a claim can't be cited it's labeled UNVERIFIED rather than asserted. *Compliance:* §4.2 traceability + §7 audit; answers Sarah's trust scar.
- **assessing-output-reliability** — *Achieves:* a reader knows how trustworthy an artifact is at a glance. *How:* attaches a deterministic reliability footer, a **qualitative label** (Grounded / Partial / Unverified) plus reasons, **never a numeric %**. *Compliance:* a % reads as a credit-risk score, so it's banned (§4.2).
- **redacting-restricted-fields** — *Achieves:* restricted data never reaches the model. *How:* a reference for what §2.1 prohibits as inputs (internal rating, watchlist/Special-Assets language, guarantor personal financials); enforced server-side in the MCP guards. *Compliance:* §2.1 + §5 + guarantor refusal.
- **screening-and-gating-output** — *Achieves:* nothing credit-adjacent or unreviewed leaves. *How:* routes the drafted artifact through `screen_and_finalize` (scans for §4.2 language, blocks; attaches the footer; tags §4.3 review). *Compliance:* §4.2 output guard + §4.3 human gate.

**Risk & early-warning (Track A, deterministic, facts-only)**
- **checking-covenant-compliance** — *Achieves:* answers "is this borrower compliant, with cushion?" *How:* the `check_covenant_compliance` tool tests latest-month DSCR/leverage vs thresholds, computes the cushion/headroom, flags breach, and compares reported vs computed status. *Compliance:* facts only; the RM owns any credit judgment (§4.2).
- **detecting-deterioration-signals** — *Achieves:* surfaces deterioration over time. *How:* the `detect_deterioration_signals` tool reads the full history for DSCR/revolver trends, threshold crossings, the status-vs-trend mislabel, thin cushion, and construction lifecycle signals (pre-leasing vs 75%). *Compliance:* lifecycle-aware; facts only (§4.2).
- **measuring-engagement-coverage** — *Achieves:* "who have I gone quiet on?" *How:* the `measure_engagement_coverage` tool counts days since the last **substantive two-way** contact (a one-way notice / missed call / internal prep does not count) vs the naive last-entry count. *Compliance:* facts only; RM-private.
- **assembling-watchlist-triage** — *Achieves:* "who needs attention this week?" *How:* the `assemble_watchlist` tool composes the three above across the book and ranks by **risk × neglect** (a facts-derived order, not a rating). *Compliance:* RM-private; automation needs CCO approval (§4.1); facts only (§4.2).

**Relationship, renewal & reconciliation (Track B, the creative core)**
- **flagging-renewal-and-retention** — *Achieves:* "who am I about to lose?" the healthy borrower the watchlist misses. *How:* the `flag_renewal_and_retention` tool fires when a borrower is healthy *and* near renewal / being courted; surfaces the maturity clock, health/trend, the competing offer, and relationship value. *Compliance:* flags "engage," **never a rate** (pricing committee owns price); §4.1 for automation.
- **detecting-cross-source-discrepancies** — *Achieves:* "what actually happened, what's mis-dated, what decision isn't in the file?" *How:* pulls `get_relationship_timeline` (+ emails / activity log / structured data) and surfaces three discrepancy types: mis-dated/conflated CRM entries, email-only decisions, figure/date contradictions. *Compliance:* facts only; a human's credit decision is quoted **verbatim + attributed** (scribe, not author).
- **verifying-commitment-fulfillment** — *Achieves:* "close the loop", did everyone do what they said? *How:* extracts commitments / conditions / deadlines / doc requests from the narrative, then verifies each against the subsequent data and log, marking met / unmet / open / unverifiable, with sources. *Compliance:* facts only; the RM owns the judgment.

**Document intelligence (Track B)**
- **reviewing-covenant-package** — *Achieves:* "what's in the package, what's missing, do the ratios reconcile?" *How:* `list_documents` → `classify_document` (with the §2.1 guarantor pre-screen) → `extract_document_fields` → `cross_validate_covenant` (certified vs recomputed vs the bank's data) → `review_package` (completeness + quality) → `screen_and_finalize` + `render_pdf`. *Compliance:* restricted docs refused on intake; every figure cited; whether add-backs are adequate is the RM's call (§4.2).

**Context & synthesis**
- **building-client-360** — *Achieves:* a consolidated borrower view for a meeting or review. *How:* assembles a dossier from `get_borrower_dossier` + loan performance + activity log + emails (+ memo), and **explicitly flags the dimensions the data does not cover** (no deposits/treasury/collateral). *Compliance:* §3.2 synthesis; rating stripped.

**Drafting / client output**
- **drafting-rm-communications** — *Achieves:* a client-ready message (missing-docs request, draw-response letter, meeting follow-up). *How:* drafts factual, brief copy (no commitments, no credit bad-news) and routes it through `screen_and_finalize` + `render_pdf`. *Compliance:* §4.3 review; rebuild of Tom's wf1/wf3.
- **drafting-relationship-review-memos** — *Achieves:* an annual/periodic relationship-review memo. *How:* assembles + cites the factual sections, then **STOPS and asks the RM for the credit assessment in their own words**, drafts the narrative around the RM's verbatim words, then screens. *Compliance:* the §4.2-decomposed rebuild of Tom's wf2 (the AI never authors the judgment).

**CRM enrichment**
- **updating-the-crm** — *Achieves:* turns a call/email/meeting into a structured CRM note + tasks, or proposes enriching a thin/contradictory log. *How:* drafts the structured entry **propose-only**; nothing is written until the RM approves. *Compliance:* §3.3/§4.2; scribe for any human decision.

**Eval & governance**
- **running-the-eval-suite** — *Achieves:* "run the evals / prove the numbers." *How:* calls `run_evals`, which grades the golden set against the live tools (deterministic, no LLM) and refreshes the observability scorecard; works in Code and Cowork.
- **viewing-eval-results** — *Achieves:* "how is it doing?" *How:* calls `get_latest_report` to display the latest agent-eval / observability scorecard (display-only).
- **viewing-proposed-improvements** — *Achieves:* "what should we change?" *How:* calls `get_latest_report(improvements)` to display the loop's advisory proposals, including the §4.2 finding left unapplied (display-only).

---

## Part 3 · The local MCP server + tool definitions

### What the server is
**`centerline`** is a local, Python **MCP (Model Context Protocol) server**: a small process that exposes the
bank's data and the deterministic analysis/compliance logic as **callable tools**. It is the project's single
**cross-surface compliance chokepoint**: every retrieval strips restricted inputs (§2.1), halts prohibited
borrowers (§5), refuses guarantor documents, and every generated artifact can be routed through the §4.2
output screen, **in code, not in a prompt**, so the guards hold regardless of what the model says.

### How it runs (and why it works on both surfaces)
- The tool logic and the guards live in `core.py` / `guards.py` (**stdlib, SDK-free**), so they're unit-testable and apply even on a direct call.
- The server is launched with `uv run --with mcp` and **spawned on the host Mac**, which is why the *same* server serves both surfaces:
  - **Claude Code** loads it from the repo-root `.mcp.json`.
  - **Claude Cowork** loads it from `~/Library/Application Support/Claude/claude_desktop_config.json`, which Claude Desktop **SDK-bridges** into Cowork's sandboxed VM (it appears as `type: sdk`).
- **Honest boundary:** project/plugin hooks do **not** fire in Cowork, which is exactly why enforcement lives in the server, not in hooks. In Cowork a raw file read could bypass the strip, so the production answer is a **governed data store reached only through the connector** (the AWS AgentCore Gateway mapping).

### Tool definitions (19), by purpose
*Achieves* = what it gives the user · *How* = what it does under the hood.

**Retrieval, read the system of record (all: §2.1 strip · §5 gate · restricted-language redaction)**
- **get_borrower_dossier** — *Achieves:* a borrower's profile + latest performance + memo presence. *How:* reads the bank data; strips the internal rating; keeps `covenant_status` as a fact.
- **get_loan_performance** — *Achieves:* the monthly DSCR/leverage/revolver/status series. *How:* returns the rows as factual data; redacts restricted note language.
- **get_activity_log** — *Achieves:* the CRM contact log. *How:* returns entries with restricted raw-note language redacted.
- **get_emails** — *Achieves:* the borrower's email thread. *How:* returns the thread, restricted language redacted.
- **get_relationship_timeline** — *Achieves:* one chronological, source-tagged view so mis-dated entries and email-only decisions surface. *How:* merges the CRM log + emails into one ordered list (deterministic dates).
- **list_documents** — *Achieves:* enumerate a covenant-package folder without a Cowork folder prompt. *How:* lists the directory **host-side** (the server runs on the host on both surfaces); returns files + PDFs.

**Track-A analysis, deterministic, facts-only (§4.2)**
- **check_covenant_compliance** — *Achieves:* the latest-month covenant test with cushion. *How:* DSCR/leverage vs thresholds, cushion/headroom, breach flags, reported-vs-computed status (construction → N/A).
- **detect_deterioration_signals** — *Achieves:* deterioration over the full history. *How:* trends, threshold crossings, the status-vs-trend mislabel, thin cushion, construction lifecycle (pre-leasing vs 75%).
- **measure_engagement_coverage** — *Achieves:* the substantive-contact gap. *How:* days since the last two-way contact (one-way notices / missed calls excluded) vs the naive count.
- **assemble_watchlist** — *Achieves:* the ranked portfolio triage. *How:* composes the three above across borrowers, ranked by risk × neglect (a facts order, not a rating); §4.1 for automation.
- **flag_renewal_and_retention** — *Achieves:* the inverse radar, the healthy borrower at attrition risk. *How:* fires on healthy + near-renewal + competitive signal; surfaces the maturity clock, health, the offer, relationship value; **never a rate**.

**Document intelligence (the synthetic Meridian package)**
- **classify_document** — *Achieves:* the type of a package PDF. *How:* runs the **§2.1 pre-screen first** (a guarantor PFS is refused before any model call), else calls the Anthropic API (temp 0, Pydantic-forced schema); returns type + confidence + rationale.
- **extract_document_fields** — *Achieves:* the structured fields for a classified doc. *How:* per-type schema extraction; `other` / PO / projections are skipped; guarantor is refused.
- **cross_validate_covenant** — *Achieves:* the certified-vs-recomputed catch. *How:* reconciles the certificate's certified ratios vs recomputed (GAAP) vs the bank's own data, surfaces the EBITDA add-back bridge, provenance-tags every figure, returns `cross_source_mismatches`. Deterministic (no API).
- **review_package** — *Achieves:* the intake summary. *How:* completeness (required vs received → missing docs/items) + quality flags (unsigned letter, withheld names) + §2.1 refusals; returns `low_confidence_inputs`. Deterministic (no API).

**Compliance & output (the guards every artifact routes through)**
- **screen_and_finalize** — *Achieves:* a safe, footer'd, review-tagged artifact. *How:* scans for §4.2 credit-characterizing/predictive/recommending language (blocks), attaches the qualitative reliability footer (pass `cross_source_mismatches` / `low_confidence_inputs` for an honest Partial), tags §4.3 review. The cross-surface OUTPUT guard.
- **render_pdf** — *Achieves:* a credit-file-grade PDF of a screened artifact. *How:* renders the markdown (with the DRAFT banner + footer preserved) on the host, with optional trend charts; Centerline letterhead. Deterministic (no API).

**Eval & governance**
- **run_evals** — *Achieves:* "prove the numbers." *How:* grades the golden set against the live tool logic (deterministic, no LLM) and regenerates the observability scorecard; returns pass/fail totals + breakdowns.
- **get_latest_report** — *Achieves:* always-current eval / improvement / observability reports cross-surface. *How:* a read-only `git pull --rebase` host-side (never commits/pushes), then returns the report content; `kind` = improvements / agent_eval / observability.

---

## Part 4 · Skill → tool quick map (who calls what)

| Skill | Primary MCP tool(s) | Always ends with |
|---|---|---|
| assembling-watchlist-triage | `assemble_watchlist` (composes covenant + deterioration + engagement) | `screen_and_finalize` → `render_pdf` |
| checking-covenant-compliance | `check_covenant_compliance` (+ `detect_deterioration_signals`) | screen → render_pdf |
| detecting-deterioration-signals | `detect_deterioration_signals` | screen |
| measuring-engagement-coverage | `measure_engagement_coverage` | screen → render_pdf |
| flagging-renewal-and-retention | `flag_renewal_and_retention`, `get_relationship_timeline` | screen → render_pdf |
| detecting-cross-source-discrepancies | `get_relationship_timeline`, `get_emails`, `get_activity_log` | screen → render_pdf |
| verifying-commitment-fulfillment | `get_emails`, `get_activity_log`, `detect_deterioration_signals` | screen |
| reviewing-covenant-package | `list_documents` → `classify_document` → `extract_document_fields` → `cross_validate_covenant` → `review_package` | screen → render_pdf |
| building-client-360 | `get_borrower_dossier`, `get_loan_performance`, `get_activity_log`, `get_emails` | (feeds other skills) |
| drafting-rm-communications | (retrieval for context) | screen → render_pdf |
| drafting-relationship-review-memos | client-360 retrieval, then the RM-authored pause | screen → render_pdf |
| updating-the-crm | (none, propose-only output) | RM approves before any write |
| grounding / reliability / redacting / screening | behavioral; lean on the server guards + `screen_and_finalize` | n/a |
| running-the-eval-suite | `run_evals` | n/a |
| viewing-eval-results | `get_latest_report` (agent_eval / observability) | n/a |
| viewing-proposed-improvements | `get_latest_report` (improvements) | n/a |
