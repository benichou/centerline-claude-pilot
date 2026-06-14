# Speaker Notes — Centerline Claude Pilot panel deck (draft v1)

> Pairs with `deck-outline.md`. Presenter-spine format: slides stay sparse; the narration lives here.
> **Grading reality:** the panel scores narration + ability to hold a conversation, not just the live outputs. So each demo/eval slide carries **why it matters · workflow-fit/gap · the live orchestration (skill→MCP tools→guard→screen→PDF) · the compliance line · the honest caveat · the segue · likely Q&A.**
> Numbers are grounded in the assignment data and our build (cite the source row live when asked). Track-A figures are real; Track-B doc-intel (B2) runs on clearly-labeled **synthetic** docs that encode real *directions*.
> **Two dates, kept distinct.** Cover/presentation date = **June 2026** (delivered to the panel). Engagement scenario = **end of May 2025, as-of 2025-05-31** — the last loan-performance row (emails end Apr–May 2025, policy v1.2 eff. Feb 2025). Pinning the as-of to 2025-05-31 keeps the figures exact: A3's 78-day gap and B1's 457-day maturity clock (2025-05-31 → 2026-08-31) are both measured from it. In-scenario "this week" = the week of the 2025-05-31 close. Only the cover shows June 2026; all in-scenario narration is as-of end-May 2025.

---

## PART I — CONTEXT

### S1 — Cover
**On-slide:** "Centerline Bank — Claude Pilot." · "Technical-challenge presentation · Senior Forward Deployed Engineer (candidate) · Caylent." · Franck Benichou · June 2026.
**Say:** "This is the Claude pilot for Centerline's Commercial Banking division — what I built, run live, with the compliance baked in. I'll narrate every decision as we go."

### S2 — Who I am / my mandate
**Say:** "I'm joining at the end of May 2025 as the Senior FDE on a 90-day engagement, embedded with Rachel Torres, the CCO, to take this pilot from *licenses purchased, nothing deployed* to *workflows three RMs actually use*. The way I work: pair from minute one, show what good looks like, and be honest about the hard parts."
**Point:** sets the frame — I'm not pitching a product; I'm the engineer who already built the thing and is here to land it.
**Likely Q&A:** *"Why you / why an FDE?"* → "Because the risk here isn't the model — it's adoption inside a regulated workflow. That's an embedded-engineering problem, not a software-license problem."

### S3 — The situation
**Say:** "Three RMs manage a combined **$350M** book and spend **30–40%** of their time on documentation, covenant tracking, and call prep — not on clients. The bank has bought Claude for Work licenses and deployed nothing. And the CCO has a specific priority: an early-warning capability for contact gaps and financial deterioration."
**Why it matters:** quantifies the prize (a third of three senior RMs' time) and names the buyer's stated need so everything downstream maps to it.

### S4 — The catalyst (through-line A)
**Say:** "One RM — Tom DeLuca — didn't wait. He built five AI workflows on a personal ChatGPT account, with client financials and names pasted in. The IT audit caught it; **two compliance violations**. The honest read isn't 'Tom's the problem' — it's *Tom was right that this helps, and he used the wrong tools to do it.* His workflows are our starting point, not our blueprint."
**Segue:** "So the first question is: what does 'the right tools' even mean here? That's a compliance question before it's a technical one."

### S5 — The compliance reality
**On-slide:** five chips — §4.2 · §2.1 · §5 · §4.1 · §4.3.
**Say:** "Section 4 is trickier than it looks. **§4.2** — AI output may not characterize creditworthiness, even implicitly, and 'I added a disclaimer' explicitly does *not* count. **§2.1** — internal credit ratings and watchlist designations can't even be *inputs* to the AI without written CCO approval. **§5** — no AI at all on Special-Assets or litigation credits. **§4.1** — automated monitoring needs CCO sign-off before launch. **§4.3** — everything human-reviewed before it's client-facing or in the file."
**Point:** "These aren't a wrapper we add at the end. They decide the architecture — you'll see them enforced in code, not in a prompt."
**Likely Q&A:** *"Isn't §4.2 impossible if the tool is useful?"* → "No — the trick is the AI organizes and cites *facts* and the RM owns the *judgment*. You'll see that line drawn live in A3, B3, and B4."

### S6 — The data & what it revealed (through-line B)
**Say:** "Eight files — three CSVs, four email threads, one relationship memo — current through end of May 2025, so everything I show is *this week's* picture. The signal is *already in the data* — it's just scattered across structured and unstructured sources, and the system of record can't be trusted. Logs are mis-dated, the most consequential credit decisions live only in email, and the covenant *status* field lags the actual trend by months. Three things fell out: Meridian — a careful action plan that **was never executed**; Crestwood — **attrition risk on a perfectly healthy borrower**; and across the book, **engagement diverges from distress** — RMs go quiet on exactly the credits that are sliding."
**Point (the spine):** "So our job isn't to find hidden data. It's to **organize scattered facts and make the record trustworthy** — and leave the judgment with the RM."
**Likely Q&A:** *"If the signal's already there, why didn't the RMs act?"* → "Because it's buried in free-text notes and split across systems. Tom's own weekly summary even flagged Crestwood — and he still lost momentum. Surfacing isn't enough; that's the 'flag ≠ action' point I'll come back to."

---

## PART II — APPROACH

### S7 — How we built it
**Say:** "Four decisions. One — a **composable skill library**, not one mega-prompt: small, single-purpose skills Claude selects and composes. Two — **MCP tool-use** instead of pasting data into context, which is also what makes Tom's workflow compliant. Three — **guardrails live server-side**, in the tools themselves, so they hold no matter what the model says. Four — I build in Claude **Code** and demo in **Cowork**, which is the RM's no-terminal surface — the UI is the product, with no UI to build."
**The brief's question, answered honestly:** "The brief asks: is Tom's single-prompt-with-everything-pasted-in the right architecture? My answer: the RM still types **one prompt** — but it now fires a **multi-tool pipeline** (retrieve → compute → draft → screen → render). 'Single prompt' was never the problem; *single LLM call with confidential data pasted in* was. The only workflows that need a genuine extra step are the ones where a **human judgment** belongs — the memo (§4.2) — or a **governance gate** belongs — monitoring (§4.1)."
**Likely Q&A:** *"So even the simple drafting tasks aren't one call?"* → "Correct — even the missing-docs email retrieves the package state, screens the output, and renders a PDF. The single thing the RM does is ask; the system does the orchestration."

### S8 — Architecture in one picture *(the recurring lens)*
**On-slide:** the flow diagram (DATA+MCP → SKILL → deterministic tools/guards → screen_and_finalize → PDF → human).
**Say:** "This is the whole system, and I'll point back to it on every demo. Claude reads a request and **selects one skill by its description**. The skill is a **recipe** that calls deterministic **MCP tools** — the tools do the arithmetic and enforce §2.1/§4.2; the model never does the math or makes the credit call. The output is routed through one screening tool that attaches the reliability footer and the §4.3 tag, then rendered to a credit-file-grade PDF. The model orchestrates and narrates; the tools do the math and the compliance."
**Point:** "That separation is the entire trust story — and it's why the guardrails hold cross-surface, in Code and in Cowork."

### S9 — Requirements scorecard *(flip-to / Q&A)*
**Say (only if surfaced or as a quick checkpoint):** "Quick map against the brief: two working solutions — built, not described; exact prompts — verbatim in the recipes; real outputs — we'll run them live; honest eval — a whole slide on the hard 20%; multi-step + MCP — the architecture you just saw; compliance designed-in — server-side; and a creative, non-obvious pick — close-the-loop reconciliation and retention."
**Use:** keep in back pocket; pull up if the panel starts checklisting.

---

## PART III — TRACK A (Deliverable A — fix Tom's wf5)

### S10 — Track A intro
**Why it matters / business impact:** this is the CCO's **#1 priority** and the exact workflow IT flagged — so fixing it is both the compliance win and the buyer's stated need.
**Fits / fills gap:** replaces Tom's Monday-morning scramble across three systems (his wf5 was literally "every Monday, ~15 min in personal ChatGPT") with a compliant, RM-private pre-compute.
**What changed (the architecture verdict):** paste-everything-into-ChatGPT → **retrieve via MCP → deterministic flags (not the LLM) → present → §4.1 gate**. The aggregation was the compliance problem; the math moving into code is the fix.
**Segue:** "Three prompts — let me show the watchlist first."

### S11 — A1 "who needs attention this week?"
**Why / impact:** one ranked view of where the $350M is at risk *and* neglected — the triage an RM does manually every Monday.
**Fits / gap:** the weekly portfolio review, minus the manual collation; surfaces *risk × neglect*, which no single field captures.
**Under the hood (show it live):** skill **`assembling-watchlist-triage`** → MCP **`assemble_watchlist`**, which composes **`check_covenant_compliance`** + **`detect_deterioration_signals`** + **`measure_engagement_coverage`** over the book → **`screen_and_finalize`** → **`render_pdf`**. Point at S8: "watch the Progress list — that's the skill ticking off tool calls."
**Result to narrate:** Meridian #1 (DSCR 1.03 vs 1.20 · revolver 85% vs the 75% cap Sarah set · 78 days since substantive contact, as of 2025-05-31 · covenant due) … **Crestwood last** — zero distress signals.
**Compliance line:** "It **ranks; it does not judge**. No 'high risk,' no grade — facts ordered by severity and neglect (§4.2). And it's RM-private."
**Honest caveat:** "Crestwood sinking to the bottom is the tool being *honestly blind* — distress monitoring can't see a healthy borrower who's about to leave. That's a separate lens, and it's exactly Track B."
**Segue:** "Let me prove the math on the one at the top."

### S12 — A2 "is Meridian compliant — cushion *and* trend?"
**Why / impact:** covenant compliance is the core of portfolio management; getting it *wrong* in a credit file is the nightmare. So the math must be deterministic and the trend must be visible.
**Fits / gap:** the covenant-tracking task that eats RM time — and corrects the misleading **status label** (read "Compliant" through months of DSCR sliding 1.45 → 1.03).
**Under the hood:** **`checking-covenant-compliance`** → **`check_covenant_compliance`** (DSCR/leverage vs per-borrower thresholds, cushion, reported-vs-computed) + composes **`detect_deterioration_signals`** for the trend + the revolver-past-cap flag → screen → **PDF with a DSCR-vs-floor trend chart**.
**Result:** DSCR 1.03 (breach, cushion −0.17), leverage 4.5 (breach), revolver 85% = 10 pts over a *non-covenant* cap. "The math runs in code, not the LLM."
**Compliance line:** "The field said 'fine'; the trend said 'sliding.' The AI shows both as **facts**; the RM owns the call."
**Honest caveat:** "Self-reported, batch-arriving data — so the tool flags it as a fact to verify, not a verdict."
**Likely Q&A:** *"Why not let the model compute the ratio?"* → "Because a mis-calibrated arithmetic slip in a covenant test is a §4.2/credit-file risk. Determinism is the point."

### S13 — A3 ★ "who have I gone quiet on?" (the gem)
**Why / impact:** this is the risk **no field flags** — and it's the CCO's stated contact-gap priority. Going quiet on a sliding credit is how a workout becomes a loss.
**Fits / gap:** nothing in the bank's systems measures *substantive two-way contact*; the raw log over-counts (a one-way overdue notice looks like "contact").
**Under the hood:** **`measuring-engagement-coverage`** → **`measure_engagement_coverage`** (uses `get_activity_log` + `get_emails`; excludes one-way notices, missed calls, internal-only) → screen → PDF (engagement bar chart).
**Result:** Meridian **78 days** of substantive silence **as of 2025-05-31** — the naive log reads 33 (the 4/28 "Formal Notice – No Response" is one-way) → **undercounts by 45 days**. (Measured from the data's as-of date, not today's clock.)
**Compliance line / Sarah's fear, answered:** "It's **RM-private, advisory, dismissible** — 'facts for your judgment, annotate or dismiss; maybe you saw them at a conference.' Sarah's objection — *don't flag my contact frequency to management* — became the design."
**Honest caveat (keep it — it builds trust):** "Engagement coverage is only as good as the log; off-system contact won't be captured."
**THE BRIDGE (close Track A):** "Here's the honest limit of all early-warning: **flag ≠ action.** Tom's own weekly summary flagged the Crestwood gap — and he still lost momentum on it. Detection is necessary, not sufficient. So Track B is about the relationship and the record — and the actions that fall through the cracks."

---

## PART IV — TRACK B (Deliverable B — our own find)

### S14 — Track B intro
**Say (read-the-brief moment):** "The brief says Deliverable B must *not* be the obvious ones, and it names them: memo drafting, covenant-package tracking, overdue emails. We built those too — but I'm calling them what they are: the **compliant cleanup of Tom's remaining shadow workflows.** Our actual creative claim is the thing nobody asked for: **close-the-loop** — verifying the bank kept its own commitments — plus **cross-source reconciliation** and **proactive retention.** It combines sources no one reconciles and surfaces the bank's *own* dropped follow-through."
**Why it matters:** elevates early-warning from "metrics are deteriorating" to "**commitments weren't kept**" — and catches healthy clients about to walk.

### S15 — B1 "prep me for Crestwood" (retention — the inversion)
**Why / impact:** retention and cross-sell are the RM's *core* mandate. Losing Crestwood — A-rated, pristine, improving — over 15 bps and a slow renewal is a direct failure of the role's primary measure, not a peripheral risk.
**Fits / gap:** the meeting-prep workflow (Tom's wf4), inverted into a retention radar — the lens A1 is structurally blind to.
**Under the hood:** **`flagging-renewal-and-retention`** → **`flag_renewal_and_retention`** (reuses `check_covenant_compliance` + `detect_deterioration_signals`; healthy + maturity-clock + competitive-signal scan) + **`building-client-360`** + **`get_relationship_timeline`** → screen → PDF.
**Result:** matures 2026-08-31 — **457 days out as of the 2025-05-31 data close** (the clock is measured against the data's as-of date, not today), First Midwest **4.90%** vs our 5.05%, pricing-exception pending with the client's deadline already passed, no renewal memo on file, "risk of attrition high."
**Compliance line:** "It surfaces facts and says *engage / chase this to a yes-or-no* — but it **never names a rate.** That's the pricing committee's call (§4.2)."
**Honest caveat:** "Newest record entry is 2025-05-31 — confirm the live renewal state before you walk in."

### S16 — B2 "what's in Meridian's package?" (doc-intel — the TRUST centerpiece)
**Why / impact:** this is Sarah's workflow and Sarah's scar — she was burned by an AI that gave wrong covenant info. So this demo is the answer to *"why should I trust it this time?"*: every number points to the document and field it came from.
**Fits / gap:** the covenant-package intake she's been chasing — classify, check completeness, reconcile, flag — that today is hours of manual cross-checking.
**Under the hood (the full pipeline — show every step in Progress):** **`reviewing-covenant-package`** → **`list_documents`** → **`classify_document`** → **`prescreen_section_2_1`** (guarantor PFS **refused on intake, never sent to a model**) → **`extract_document_fields`** → **`cross_validate_covenant`** → **`review_package`** → **`grounding-claims-to-source`** → **`screen_and_finalize`** (fed the mismatches + low-confidence inputs) → **`render_pdf`** (DSCR trend chart).
**Result (the wow):** the certificate **certifies compliant (1.23 / 3.76)**; the GAAP financials **recompute to a breach (1.03 / 4.50)**; the **bank's own loan_performance agrees with the recompute.** The entire gap is **$2.0M of EBITDA add-backs** (legal/restructuring 800k, owner-comp 700k, equity 300k, run-rate 200k). The ACORD insurance cert classifies `other` and is skipped (the "certificate" overlap trap). Missing: aerospace PO, projections, A/R names. Rep letter unsigned.
**Provenance / Sarah's scar (the centerpiece line):** "Look at the footer — it reads **Partial**, and *every reason is bulleted and tagged with the tool and the source*: 'DSCR certified 1.23 vs recomputed 1.03 [cross_validate_covenant · certificate vs financial_statement].' Trust isn't a confident tone; it's *here is exactly where this came from.*"
**Compliance line:** "The §2.1 guarantor refusal is **enforced, not a disclaimer** — the document is never read. And whether those §1.01 add-backs are *adequately supported* is the RM's call, not mine."
**Honest caveat:** "This package is synthetic — clearly labeled — but it encodes real directions from the data (self-reported breach, the add-back gap). The capability is real; the PDFs are staged so the system has something to catch."
**Units note:** "Say **$2.0M**, not $2,000 — the package is in thousands."
**Second prompt:** "draft the missing-docs email" → **`drafting-rm-communications`** → David Kwan, four items, no breach/credit language, no guarantor reference, DRAFT/§4.3. "The package review *tells the letter what to ask for.*"
**Likely Q&A:** *"What if the model mis-extracts?"* → "Extraction is the one model step here — so we recompute deterministically and cross-check against the bank's own data; a bad extract shows up as a mismatch, not a silent error."

### S17 — B3 "reconcile Arcadia emails vs the CRM log" (scribe-not-author — THE §4.2 moment)
**Why / impact:** the most consequential credit decisions live only in email and never reach the record — so when the RM leaves, the bank loses the "what did we know and when." This is a governance + audit win, found by triangulating sources no one reconciles.
**Fits / gap:** the CRM-update workflow (Tom's wf-CRM) turned into a reconciliation: emails vs log vs structured data — and it feeds A3's contact-recency math the *correct* dates.
**Under the hood:** **`detecting-cross-source-discrepancies`** + **`verifying-commitment-fulfillment`** + MCP **`get_relationship_timeline`** (merges CRM log + parsed email dates) + **`get_emails`** + **`detect_deterioration_signals`** (the 71% < 75% condition) → screen → PDF.
**Result:** the **04-09 CRM row sits 13 days before the draw was even submitted** and collapses the Apr 22–25 exchange — "it poisons contact-recency math, reads Apr 9 instead of Apr 25." And Chen's Apr-25 ruling — *"don't waive the 75%; 71–73% is a different underwriting story than what we approved"* — lives only in email.
**THE line (scribe-not-author):** "Watch what it does with Chen's decision: it surfaces it **verbatim and attributed** — 'per M. Chen, email Apr-25' — and offers a **propose-only** CRM entry. *The AI transcribes the credit officer's decision into the file; it never makes one.* That's the §4.2 line drawn precisely."
**Honest caveat:** "Friday docs unconfirmed, tenant names pre-lease, completion date unreconciled — it lists what it *can't* close, it doesn't paper over it."
**Second prompt:** "draft the draw-response letter" (wf1) → requests the four items; Chen's internal disposition **stays internal** — the RM delivers it, not the letter; no funding commitment/waiver. DRAFT/§4.3.

### S18 — B4 "build my Summit annual memo" (wins the skeptic)
**Why / impact:** Marcus is the highest producer, the AI-skeptic, mentors four juniors — the make-or-break adopter. He writes **~71 annual memos a year**. Win him without changing how he thinks and the whole rollout tips.
**Fits / gap:** Tom's wf2 (the memo), **decomposed for §4.2** — the one workflow that genuinely needs an extra human step.
**Under the hood:** **`drafting-relationship-review-memos`** → assemble + cite every factual section (17-month DSCR arc 1.13→1.21→1.12, covenant table, engagement, open items) → **⏸ STOP and render a form** eliciting the RM's own *assessment / outlook / next-steps / attribution* → draft the narrative **around the RM's verbatim words** → screen → PDF.
**THE line (§4.2 made literal):** "Here's the part I can't write for you. Per §4.2, the credit assessment must be yours — so the AI **stops and hands you the pen.** Your words go in verbatim, attributed to you. The AI does the 80% assembly; you keep the 20% judgment. That's the policy made *visible*."
**Honest caveat:** "Footer reads Partial — thin cushion, status-lag, sparse CRM notes, no prior memo, no email thread — each reason tagged with its source."
**Likely Q&A (the skeptic's own objection):** *"I don't need AI to tell me what I think about my clients."* → "Exactly — and it doesn't. It never authors the judgment. It gives you back the three hours of assembly so you spend your time on the judgment only you can make."

---

## PART V — TRUST · EVAL · ADOPTION

### S19 — How we keep it trustworthy
**Why / impact:** the CCO can't approve what she can't measure. So reliability is a reported number across both tracks, not a vibe — this is also the §4.1 monitoring-evidence story.
**Under the hood (expose the eval workflow too):** **Layer-1** deterministic golden — `evals/runner.py` over source-grounded cases (**95/95**, spanning A1–A3 + B1–B4) — *tests the tool code, LLM never invoked.* **Layer-3** live agent-behavior eval — `agent_eval.py` runs prompts through Claude **headless** (`claude -p`, scoped tools) and grades the **model's own decisions**, including a §4.2 scan of its narration (closes the "nothing checks the chat reply" gap). **Layer-4** improvement loop — `improve.py`, advisory only. **CI prod-gate** — black/flake8 + deterministic suites on every merge to main.
**The line:** "Layer 1 tests the tools; Layer 3 tests the model. Don't let one stand in for the other."
**Reported to the CCO:** the `viewing-eval-results` skill shows this live in Cowork, both tracks.

### S20 — Governance loop
**Say:** "The improvement loop isn't cosmetic — it **independently caught** a real §4.2 footer issue in A1/A3, diagnosed it, and proposed the exact fix. We left it **unapplied on purpose** as a live governance artifact: **AI proposes skill edits — it has no write access to the guards, the core, or the eval keys — and a human in Compliance disposes (§4.3).** The audit trail is committed, timestamped reports."
**Honesty about its own automation:** "When the report pipeline hit an API limit, the skill *said so* and fell back to the last complete report — it tells you when its own automation failed."
**Likely Q&A:** *"Who owns this in production?"* → "A named skill-library maintainer plus Compliance as the CCO's delegate — same propose/dispose split, on the bank's funded API tier."

### S21 — Honest eval (the 80/20)
**Say:** "What it does well: grounded, cited, compliant by construction, reusable across the book. The hard 20%, owned: **flag ≠ action** — surfacing doesn't fix follow-through, the deployment has to make the next step frictionless; **value is gated by logging discipline** — Marcus logs sparsely, so reconciliation is near-useless for him, the adoption catch-22; **Track A is blind by design** to healthy borrowers and construction loans, which is *why* Track B exists; and **doc-intel runs on synthetic docs** because the bank's package had no raw source documents."
**Point:** "None of the creativity claim rests on fabricated data — the gems run on the real files."

### S22 — Adoption per RM
**Say:** "Adoption is the real risk, and no single tool wins all three RMs — a **portfolio** does. **Sarah:** her trust scar and her fear *are* the design — grounding answers the scar, RM-private answers the fear; her KPI is a '10-minute Monday.' **Tom:** make him the co-builder — his shadow workflow becomes the sanctioned one; that's the §6 amnesty done right. **Marcus:** the memo is the wedge — the one thing that removes real burden without touching his judgment."
**Likely Q&A:** *"Which RM do you start with?"* → "Sarah — she's the natural teacher; if she adopts, she trains the team. Marcus is the proof point; Tom is the co-author."

### S23 — Production & rollout
**Say:** "**Cowork is the RM surface** — no terminal, no UI to build. For monitoring, **§4.1** means we present it as 'designed, RM-private, pending CCO approval — and fast-trackable.' For data, **§2.3 residency** means local scheduled jobs beat cloud routines — the data stays put. And the adoption flourish: a Sunday-night pre-compute so Sarah's watchlist, open items, and reconciliation are waiting Monday — the same 'run on a cadence, prepare for a human, never act' pattern we use for our own evals."
**90 days:** "Pilot the two tracks with the three RMs → CCO sign-off on monitoring → a governed data store and funded API tier for the rollout."

### S24 — Close / the ask
**Say:** "The whole story in one line: **Tom's instinct was right (A) — so we kept it and made it compliant; the signal was already there but the record couldn't be trusted (B) — so the AI organizes the facts and the RM keeps the judgment; and the real risk is adoption (C) — so we built a portfolio, each tool earning a specific RM.** Built, not described. Compliant by construction. Honest about the 20%. Happy to go deeper on any of it."
**Then:** Q&A.

---

## Anticipated cross-cutting Q&A (keep ready)
- **"Why Claude Code/Cowork and not Claude for Work directly?"** → The brief sanctions any agentic tool; Cowork *is* the no-terminal RM surface and runs the same plugin (skills + MCP). In production it's an admin-provisioned plugin + a hosted connector.
- **"How do the guardrails survive someone reading a raw CSV in Cowork?"** → §2.1/§5/guarantor live in the MCP server + core — the cross-surface chokepoint; the access path is the tool, and the production answer is a governed store, not loose files.
- **"Is the model ever making a credit decision?"** → Never. The math is deterministic tools; the credit judgment is either a human's words transcribed (B3/B4) or absent. §4.2 holds regardless of what the model says, because the enforcement is in code.
- **"What breaks first at 50 borrowers instead of 5?"** → Nothing in the compute (it's deterministic and per-borrower); the real scaling work is connector auth, the governed data store, and alert-fatigue tuning so 'flag ≠ action' doesn't become 'flag → ignored.'
- **"What would you do differently in production?"** → Hosted connector over local files; a larger labeled eval set with real RM edit-rates; OTel→Datadog for the §4.1 monitoring evidence; and lifecycle/industry-aware signal sets (construction vs operating).
- **"What date are these day-counts measured from — today?"** → No — every time-based figure (78-day gap, 457-day maturity clock) is computed against the **data's as-of date, 2025-05-31** (the last loan-performance row), not wall-clock time. The tool derives "now" from the data, so the numbers are **deterministic and reproducible** — re-run it next month and the figure only changes when the *data* does. That's exactly what you want for an audit trail and §4.1 monitoring evidence: the result doesn't silently drift with the calendar.
