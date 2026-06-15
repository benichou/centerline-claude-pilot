# Slide-by-slide deep dive — presenter's reader

A thorough companion to `slides/centerline-claude-pilot.md`. For each slide: **what it's doing**
(the subtext a panel reads), **facts to have cold**, **likely questions → crisp answers**, and the
**gotcha** that could trip you. Pairs with the tighter `panel-qa-prep.md` (Land + top Q&A) and the
spoken script in `speaker-notes.md`.

> This is the candidate's prep, not a panel handout. Everything here is grounded in the repo and the
> assignment data — no new claims.

---

## How to use this

- Read it once end-to-end the night before; skim the **"have cold"** lines morning-of.
- The deck carries the argument; *you* carry the evidence. Each slide below tells you the one sentence
  to land and the two facts you must not fumble.
- When unsure on a number, say *"as of the 2025-05-31 data close"* and point to the source — being
  traceable beats being fast.

## The spine you're defending (the A/B/C braid)

Hold all three through-lines at once — they're a braid, not a menu:

- **A (open):** shadow-IT → a governed, shareable **skill library**. *Right instinct, wrong tools.*
- **B (spine):** the record can't be trusted → **the AI organizes the facts; the RM keeps the judgment.**
- **C (close):** the real risk is **adoption**, not the tech → **a portfolio of tools, each earning its RM.**

One-liner if you only get one: *"I built two compliant Claude workflows the RMs will actually use —
the AI organizes the facts and every credit judgment stays with the human, enforced in code."*

## Facts to have cold (cross-cutting cheat-sheet)

- **As-of date = 2025-05-31** (the latest `loan_performance` month). The engine derives "now" from the
  data, not the wall clock (`core._as_of_date()`) — so every "X days" is measured from end-May-2025.
  Presentation is June 2026; the scenario is a fixed historical snapshot.
- **Portfolio:** 5 borrowers, 3 RMs, $350M. Sarah → Meridian + BlueLine (both in breach). Tom →
  Crestwood (A-rated, pristine) + Arcadia (construction). Marcus Webb → Summit (DSCR drifting).
- **Compliance sections:** §2.1 (ratings/watchlist can't be *inputs*) · §4.1 (monitoring needs CCO
  sign-off) · §4.2 (no creditworthiness language, even implicitly; disclaimers don't count; applies to
  *format*, not just content) · §4.3 (human review before client-facing/filed) · §5 (no AI on
  Special-Assets/litigation).
- **Build surface:** built in **Claude Code**, demoed in **Claude Cowork** (the no-terminal RM surface).
  The brief explicitly sanctions "another agentic AI tool."
- **Enforcement lives in code** — the **centerline MCP server + `core.py`** is the cross-surface
  chokepoint (strip §2.1 → compute in code → `screen_and_finalize` §4.2 + reliability footer). Hooks are
  a **Code-only** redundant belt; they do **not** fire in Cowork.
- **Reliability footer = qualitative** (Grounded / Partial / Unverified) — **never a numeric %** (a "%"
  is mis-calibrated and reads as a credit-risk score → §4.2).
- **Eval:** golden **95/95** deterministic (Layer 1, LLM not invoked) · observability scorecards (Layer
  2) · live agent-eval (Layer 3) · advisory improvement loop (Layer 4) · CI prod-gate.

---

## 1 · Cover — "AI the RMs actually use, and the CCO trusts"

**What it's doing.** Sets the dual audience in the title itself (RM adoption + CCO trust) and front-loads
two honesty flags (fictional case / synthetic data; everything as-of the 2025-05-31 close). The
Caylent × Centerline lockup signals you're presenting *to* Caylent *about* a bank engagement.

**Have cold.** You are the *Senior Forward Deployed Engineer candidate*. Subhead = "Built, not described ·
Measured, not promised · Compliant by design" — that's the whole deck in six words.

**Likely questions → answer.**
- *"Why 'the RMs actually use'?"* → Because the CCO's #3 risk is adoption; a compliant tool nobody opens
  is worth nothing. The whole design is per-RM.

**Gotcha.** Don't over-talk the cover. 15 seconds, then move — the proof is later.

## 2 · Agenda

**What it's doing.** Buys you permission to spend 5–7 minutes on context before the demos by showing the
demos are coming. Signals "≈45 min + lots of Q&A — I'd like a conversation," which matches the brief's
"pair from minute one."

**Likely questions → answer.**
- *"Can we jump to the demo?"* → "Absolutely — two minutes of context so the demo lands, then we go live."

**Gotcha.** If they push to start demos early, fold slides 4–8 into 90 seconds and go; don't fight it.

## 3 · About me

**What it's doing.** Establishes the hybrid DS + consulting + AI-engineering background and that
**AWS + Anthropic is your daily stack** — which makes the AWS production story on slide 24 credible, not
borrowed.

**Have cold.** Senior AI Engineer at Carta (document intelligence); prior Intact / EY / Deloitte;
technical reviewer on *DeepSeek in Practice* (Packt, 2025); founder of HEC Forecast.

**Likely questions → answer.**
- *"What have you shipped with Claude?"* → Document-intelligence work at Carta on the Anthropic APIs and
  Claude Code — the same shape of problem as Centerline's covenant-package intake.
- *"Why leave for an FDE role?"* → I'm a builder who wants front-line commercial impact; my edge is
  judgment + client-facing skill on top of the engineering.

**Gotcha.** Keep it to ~20s. The hybrid background is the point — don't recite a CV.

## 4 · The situation

**What it's doing.** Establishes the business pain in three numbers and names the CCO's single stated
priority — your 90-day mandate. Everything downstream maps back to this.

**Have cold.** $350M / 3 RMs · 30–40% of RM time on docs, covenant tracking, call prep · **0** workflows
in production (licenses bought, unused). CCO = **Rachel Torres**; her ask = early-warning on contact gaps
+ financial deterioration, **RM-private, compliance-gated**.

**Likely questions → answer.**
- *"Where does 30–40% come from?"* → The personas / brief; it's the documentation + covenant-tracking +
  call-prep load, which is exactly what Track A and the memo attack.

**Gotcha.** Note "RM-private" early — it pre-empts Sarah's surveillance fear that A3 resolves.

## 5 · Meet the three RMs

**What it's doing.** Adoption is the real risk, so the people are introduced *before* the tech. Each RM is
a different relationship with AI (trust scar / builder / skeptic) and a different adoption lever. The
`RM = Relationship Manager` definition box covers a panelist who isn't a banker.

**Have cold.** Sarah = linchpin, burned by an AI that gave **wrong covenant info** (trust is existential),
trains the floor. Tom = builder, 5 shadow workflows, wants to co-design. Marcus = 22-yr skeptic, **~71
memos/yr**, logs sparsely, mentors 4 juniors.

**Likely questions → answer.**
- *"Who do you start with?"* → Sarah — her trust scar is answered by grounding, her fear by the RM-private
  design, and she trains the team (covered on slide 23).

**Gotcha.** **Marcus Webb (the RM) ≠ Marcus Chen (the credit officer in B3).** Two different people. If you
say "Marcus" in B3, clarify "Chen, the credit officer."

## 6 · The catalyst — one RM didn't wait

**What it's doing.** Frames Tom's violation generously: *right instinct, wrong tools.* Turns "got caught"
into "proved AI helps — by breaking policy," and sets up Deliverable A as keeping the instinct, fixing the
violations.

**Have cold.** 5 workflows (draw letters · memos · client emails · call-prep · weekly summary). **Two
violations = confidential client data on a personal ChatGPT** (the memo + the portfolio aggregation).

**Likely questions → answer.**
- *"Isn't this a disciplinary issue, not an AI one?"* → Both — but the lesson is the demand is real and
  unmet. §6 amnesty + co-design turns the highest-risk user into the pilot's best ally.

**Gotcha.** Don't moralize about Tom. The reframe ("starting point, not blueprint") is the whole point.

## 7 · Compliance isn't a wrapper — it's the architecture

**What it's doing.** Pre-empts the single biggest way these projects fail: bolting a disclaimer on at the
end. Five constraints, and the throughline — **judgment originates with the RM, enforced in code.**

**Have cold.** §4.2 (no credit language, disclaimers insufficient) · §2.1 (rating/watchlist not even
inputs) · §5 (no AI on Special-Assets) · §4.1 (monitoring → CCO) · §4.3 (human review).

**Likely questions → answer.**
- *"How is enforcing-in-code different from a system prompt?"* → A prompt is advisory; the model can drift.
  Our `screen_and_finalize` tool and the §2.1 strip are deterministic code every output routes through —
  they hold regardless of what the model says, on any surface.
- *"§4.2 applies to format too?"* → Yes — the policy says so. That's why the memo (B4) decomposes so the
  *human* authors the assessment; formatting a credit call is still making one.

**Gotcha.** This is the slide a compliance-minded panelist will probe hardest. Know the difference between
§2.1 (input) and §4.2 (output) cold.

## 8 · The signal's already there — the record can't be trusted

**What it's doing.** Re-frames the problem honestly: the signal isn't *hidden*, it's *unactioned and
unreliable* — wrong timestamps, decisions in email, lagging status labels. This is the spine of both demos
and your "worked through the data" proof.

**Have cold.** Three finds: Meridian (action plan never executed) · Crestwood (attrition risk on a healthy
borrower) · across the book (engagement diverges from distress).

**Likely questions → answer.**
- *"So the data isn't hidden — what's the value-add?"* → Exactly — the value is **organizing scattered
  facts and making the record trustworthy**, then leaving judgment to the RM. That's harder and more
  useful than "find the hidden number."

**Gotcha.** Earlier framings said "risk invisible in structured data" — that was corrected. The honest line
is *"in the free-text notes, just unactioned."* Don't claim the signal was invisible.

## 9 · How I built it

**What it's doing.** Five design decisions, and the **direct answer to the brief's "is a single prompt the
right architecture?"** The RM still types one prompt — it just fires a multi-tool pipeline.

**Have cold.** (1) LLM-driven, simplest-first (Anthropic guidance) (2) composable skill library (3) MCP
tool-use over paste (4) guardrails server-side (5) build in Code → demo in Cowork. Only the **memo (§4.2)**
and **monitoring (§4.1)** need a genuine extra human/governance step.

**Likely questions → answer.**
- *"Single prompt or multi-step?"* → "Single prompt" was never the problem; a single call with pasted-in
  confidential data was. The RM types one prompt; under it is retrieval + deterministic compute + screening.
  Two cases genuinely need decomposition — and it's for *compliance*, not cleverness.
- *"Why skills, not one big agent?"* → Small single-purpose skills are reusable across both tracks, testable
  in isolation, and let Claude compose — Anthropic's Agent Skills best practice.

**Gotcha.** Don't overclaim multi-agent sophistication. The honest, brief-aligned answer is "simplest thing
that works; structure only where compliance demands."

## 10 · Architecture in one picture

**What it's doing.** The mental model you'll point back to on every demo: Inputs → Claude skill library →
**centerline MCP server (the compliance chokepoint)** → Human-in-the-loop. Plus two ribbons: one plugin /
both surfaces, and continuously-evaluated.

**Have cold.** The chokepoint does three things: **strip restricted data** (ratings/watchlist/guarantor
never reach the model) · **compute in code** (math is deterministic) · **screen every output** (no
credit-adjacent language + reliability footer).

**Likely questions → answer.**
- *"Why is the MCP server the chokepoint and not hooks?"* → Hooks fire in Code but **not in Cowork**; the
  MCP server/`core.py` runs on both surfaces, so that's where the guards live. Hooks are a Code-only belt.
- *"What if the agent reads a raw CSV directly in Cowork, bypassing the server?"* → Honest answer: it can,
  which is why production uses a **governed data store reached only through the connector** + Bedrock
  Guardrails as a second layer. In the pilot, the MCP path is the sanctioned access route + human review.

**Gotcha.** This is where the hooks-vs-server nuance lives. Don't claim hooks enforce anything in Cowork.

## 11 · Fix Tom's flagged workflow (Track A intro)

**What it's doing.** Triages Tom's five workflows against the brief's question. Three are fine as one prompt
(swap paste → retrieval + §4.3); two need re-architecting — the memo (§4.2) and the weekly summary (§4.1).
Deliverable A rebuilds the weekly summary as the early-warning.

**Have cold.** The table verdicts: drafting trio → keep as one prompt; memo → break up (RM authors
assessment, §4.2); weekly summary → break up (code computes flags, §4.1); all five → the §1/§2/§5 data
violation.

**Likely questions → answer.**
- *"Why rebuild the weekly summary specifically?"* → It's the one whose *aggregation* was the compliance
  problem and the CCO's named priority; moving the math into code is the fix, and it's RM-private + §4.1.

**Gotcha.** Be precise: the violation common to all five is the *personal-ChatGPT data handling*, separate
from the §4.2/§4.1 architecture issues on two of them.

## 12 · A1 — "Who needs attention this week?" (live)

**What it's doing.** First live demo. Shows composition (one skill pulls covenant + deterioration +
engagement), ranking by **risk × neglect**, and that it **cites but never characterizes** (§4.2). Crestwood
sinking to the bottom is the deliberate setup for Track B.

**Have cold.** Meridian #1 (breach, signals, 78 days since contact). Crestwood last (zero distress signals).
Chain: `assembling-watchlist-triage` → `assemble_watchlist` → covenant/deterioration/engagement →
`screen_and_finalize`. §2.1-stripped input.

**Likely questions → answer.**
- *"Isn't 'who needs attention' a credit ranking — §4.2?"* → No — it ranks on factual signals (breach math,
  days since contact) and cites each line; it never says "high risk." The ordering is deterministic, not a
  model opinion.
- *"Why is Crestwood last when you say it's the one you lose?"* → Because distress monitoring is *structurally
  blind* to a healthy borrower who's leaving. That's the honest limitation — and exactly what B1 catches.

**Gotcha.** If it ranks Crestwood low live, that's the *intended* teaching moment, not a bug. Say so.

## 13 · A2 — "Is Meridian compliant — cushion *and* trend?" (live)

**What it's doing.** Proves the math is **deterministic, in code, not the LLM**, and that the *reported
status field lied* (read "Compliant" for months while DSCR slid). Facts both ways; the RM owns the call.

**Have cold.** DSCR **1.03 vs 1.20 floor** (breach) · leverage **4.5** (vs 4.0 max) · revolver **85% vs
Sarah's 75% cap** (a non-covenant cap she set) · DSCR trend **1.45 → 1.03** · status read "Compliant"
Jan–Sep, Watch Oct, Breach Nov+.

**Likely questions → answer.**
- *"Why recompute if there's a status field?"* → Because the field lagged the trend by months. The covenant
  *status* is kept as a fact, but we distrust it and recompute deterministically.
- *"Is 'revolver 85% vs 75%' a covenant breach?"* → No — it's a cap Sarah set, not a loan covenant. We flag
  it as a fact, labeled as non-covenant. That precision matters under §4.2.

**Gotcha.** Don't call the revolver cap a covenant. It's RM-set; the DSCR/leverage are the covenants.

## 14 · A3 ★ — "Who have I gone quiet on?" (live; Deliverable-A find)

**What it's doing.** The Deliverable-A creative find: days since **substantive two-way** contact — a risk
**no single field flags**. Answers Sarah's surveillance fear (RM-private, dismissible) and bridges to Track
B with **"flag ≠ action."**

**Have cold.** Meridian **78 days** of substantive silence (as of 2025-05-31). Naive log = **33** because the
4/28 entry was a **one-way overdue notice**, not contact → **45-day undercount**. Last substantive contact
3/14.

**Likely questions → answer.**
- *"How do you decide what counts as 'substantive'?"* → Deterministic rules in code: one-way notices, missed
  calls, internal-only entries don't count; it requires a real two-way exchange. Auditable, not a model guess.
- *"Isn't flagging contact frequency exactly Sarah's fear?"* → That's why it's **RM-private and dismissible**,
  never auto-escalated to management. The design *is* the answer to her objection.

**Gotcha.** The bridge line is the most important transition in the deck: *Tom's own summary flagged the
Crestwood gap and he still lost momentum.* Detection ≠ action → that's why Track B exists. Deliver it.

## 15 · Track B intro — our own find

**What it's doing.** Proactively handles the brief's "avoid list." States out loud that memo / covenant-
tracking / overdue-emails are the **compliant cleanup**, and the **creative claim is close-the-loop +
reconciliation + retention** — combining sources no one reconciles (a risk Tom didn't see).

**Have cold.** Creative claim = (1) close-the-loop (did the bank keep *its own* commitments) (2) cross-source
reconciliation (emails ↔ CRM ↔ structured) (3) proactive retention. Demoed across all three RMs.

**Likely questions → answer.**
- *"The brief said don't build the memo — but you did."* → Deliberately, and I say so: the memo is compliant
  *cleanup* of Tom's shadow work and Marcus's adoption wedge — explicitly **not** the creative headline. The
  find is close-the-loop. Calling that out is proof I read the brief.

**Gotcha.** Say the avoid-list line *before* a panelist raises it. Pre-empting it reads as judgment; being
caught reads as a miss.

## 16 · B1 — "Prep me for my Crestwood meeting" (live; retention radar)

**What it's doing.** Inverts the watchlist: surfaces the **healthy** borrower you lose by being slow, not by
credit risk — the one A1 is blind to. The §4.2 discipline: facts + "engage," **never a rate**.

**Have cold.** Crestwood: matures **2026-08-31 (457 days out** from the 2025-05-31 close) · First Midwest
competing at **4.90% vs your 5.05%** · pricing-exception deadline already passed · no renewal memo logged.
Chain: `flagging-renewal-and-retention` → `flag_renewal_and_retention` → `get_relationship_timeline` →
screen + render_pdf.

**Likely questions → answer.**
- *"Why 457 days if it's June 2026 now?"* → The scenario is a fixed snapshot as of the 2025-05-31 data close;
  the engine measures from the data, not the wall clock. 2025-05-31 → 2026-08-31 ≈ 457 days.
- *"Isn't 'engage on pricing' a credit/pricing recommendation?"* → It surfaces the maturity clock + the
  competitive fact and says "engage." It **never names a rate** — pricing is the committee's call (§4.2).

**Gotcha.** The deck uses **5.05%** as your rate (an earlier draft said 5.25% — use the deck figure). Don't
quote a specific recommended renewal rate; that's the line you must not cross.

## 17 · B2 ★ — "What's in the package — and do the ratios reconcile?" (live; doc-intel)

**What it's doing.** The trust centerpiece for Sarah. Shows the §2.1 refusal *enforced* (guarantor financials
never sent to a model), a real cross-source catch (certified vs recomputed vs the bank's own data), and
provenance on every figure. The footer reads **Partial**, honestly.

**Have cold.** 6 synthetic PDFs. **Guarantor personal financials → refused on intake** (§2.1, pre-screen
before any API call). **ACORD insurance certificate → classified `other`, skipped.** Certified **1.23 / 3.76**
vs recomputed **1.03 / 4.50**; gap = **$2.0M EBITDA add-backs** (legal/restructuring 0.8 + owner-comp 0.7 +
equity-comp 0.3 + run-rate 0.2); **the bank's own loan_performance agrees with the recompute.** Missing:
aerospace PO, AR customer names, updated projections. Unsigned management rep letter. CFO = David Kwan.

**Likely questions → answer.**
- *"Is the doc-intel real?"* → The *documents* are synthetic and clearly labeled, because the package had no
  raw PDFs. They encode facts already in the real data; the **engine** does the catching. It's the one fully-
  synthetic piece, positioned as a compliance showcase, not the creative headline.
- *"Did the AI decide the add-backs are illegitimate?"* → No. It surfaces that certified and recomputed differ
  by $2M of named add-backs and that the bank's data matches the recompute. **Whether those add-backs are
  adequately supported is the RM's call (§4.2)** — the AI never makes it.
- *"How does the §2.1 refusal actually work?"* → A deterministic filename/type pre-screen refuses the
  guarantor PFS *before* any model call — it's never base64'd into a prompt. Enforced, not a disclaimer.

**Gotcha.** Two numbers must be exact and paired: **certified 1.23 / 3.76**, **recomputed 1.03 / 4.50**,
**gap $2.0M**. If you blur them the whole catch loses force.

## 18 · B3 ★ — "Reconcile the emails vs the CRM log" (live; close-the-loop)

**What it's doing.** Deliverable B's creative gem on real data. Catches a **mis-dated CRM row that poisons
contact-recency**, surfaces a **credit decision that lives only in email** (scribe-not-author), and tracks an
unmet condition. The sharpest §4.2 line in the deck.

**Have cold.** Arcadia: the **Apr-09 CRM row predates the real Apr-22→25 email thread** (~2 weeks off →
poisons recency). **Marcus Chen** (credit officer) ruled **"don't waive the 75%"** — email-only → surfaced
**verbatim + attributed**, with a **propose-only** CRM entry. Pre-leasing **71% < 75%** (condition unmet).
Then drafts the draw-response letter (wf1). Construction loan → operating covenants are N/A by design.

**Likely questions → answer.**
- *"Isn't transcribing a credit decision into the file making a credit judgment?"* → No — that's the
  scribe/author distinction. Surfacing a *human's* decision verbatim and attributed is §4.2-safe; the AI
  generating its own credit characterization is not. The AI **transcribes Chen's decision — it never makes
  one.** And the CRM write is propose-only (§4.3).
- *"Why is the mis-dating a big deal?"* → Every time-based computation (contact-recency, SLA, deadlines) runs
  off it. Wrong dates make the system *confidently wrong*, which is worse than missing. Emails are the
  reliable clock; we prefer them and tag reconstructed entries low-confidence.

**Gotcha.** **Marcus Chen is the credit officer; Marcus Webb is the RM (Summit, B4).** Different people, same
first name — say "Chen" in B3.

## 19 · B4 — "Build my Summit annual relationship-review memo" (live; the skeptic's wedge)

**What it's doing.** §4.2 made *literal*: the AI assembles + cites the 80%, then **STOPS** and makes the RM
author the credit judgment in his own words via an interactive form. The yellow box shows exactly what Marcus
fills in. Wins the make-or-break skeptic without changing how he thinks.

**Have cold.** The form elicits four things: the **assessment** (verbatim), an **outlook** chip (Marcus picks
*Watch / monitor*), **next steps/conditions**, and **whose name to file under** (Marcus Webb, RM of record).
Summit facts in his words: coverage **1.12x vs the 1.10x floor**, leverage **3.6x**, Location-3 lease renewal
at an **18% bump**. ~71 memos/yr removed.

**Likely questions → answer.**
- *"Isn't the demo assessment AI-written?"* → It's a *simulated* RM input to show the pause (Summit is thin —
  sparse logs, no prior memo). In production the RM types it; the AI never authors or paraphrases it — his
  words go in verbatim, attributed.
- *"What stops the RM from just rubber-stamping AI text?"* → There is no AI text to stamp — the assessment
  field is empty and required; the memo isn't complete until the human writes it. That's the §4.2 design.

**Gotcha.** Be upfront that the sample assessment is simulated for the demo. Claiming it's "Marcus's real
words" would be the kind of overclaim the honest-eval slide exists to avoid.

## 20 · How the CCO can trust it — four eval layers + CI gate

**What it's doing.** Reliability as a **reported number, not a vibe.** Four layers, and the crucial
distinction: Layer 1 tests the *tools*, Layer 3 tests the *model* — don't conflate them. Governance = AI
proposes, human disposes (§4.3).

**Have cold.** **L1** deterministic golden **95/95** (`evals/runner.py` + `evals/cases/`, LLM not invoked).
**L2** observability (`reports/observability.md`, generated by `evals/observability.py` from the live tool
logic + `traces/run-ledger.log`). **L3** live agent-eval (`evals/agent_eval.py`, Claude headless, grades tool
choice + §4.2 on the model's own narration + fact faithfulness). **L4** advisory improvement loop
(`evals/improve.py`, read-only, proposes skill edits only). **CI prod-gate** = black + flake8 + deterministic
suites. The loop caught a real §4.2 footer issue — **left unapplied** as a governance artifact.

**Likely questions → answer.**
- *"Where's Layer 2 in the repo?"* → `reports/observability.md`, generated by `evals/observability.py` from
  the live `centerline_mcp` logic + the `traces/run-ledger.log` hook ledger. Real files from real runs.
- *"Isn't testing your own golden set grading your own homework?"* → Partly, yes — it's small and
  self-authored, so I mitigate with **source-grounded expected answers**, **negative/adversarial cases**, and
  disclosure. Production = a larger labeled set + real RM edit-rates.
- *"Layer 1 is 95/95 — does that mean the model is 100% right?"* → No — Layer 1 tests the deterministic
  *tool code* (the model isn't called). The model's behavior is Layer 3. Conflating them is the trap.

**Gotcha.** The run-ledger is **Code-only** (the hook doesn't fire in Cowork) — the report says so. Production
observability = OTel → Datadog / AgentCore Observability (slide 24).

## 21 · Governance, live — "How is it doing, and what should we change?"

**What it's doing.** Makes the trust story concrete with two read-only prompts in Cowork: the eval scorecard,
and the improvement proposals (including the §4.2 finding the loop caught, left unapplied for a human). The
skills only **read** — never write.

**Have cold.** Chain: `viewing-eval-results` + `viewing-proposed-improvements` → `get_latest_report` (does a
read-only host-side `git pull --rebase`, returns content cross-surface). Audit trail = committed timestamped
reports.

**Likely questions → answer.**
- *"Could the improvement loop auto-apply a fix?"* → It's deliberately **advisory only** — it can't touch
  guards, core, or eval keys, and a human in Compliance applies approved edits. AI proposes, human disposes.

**Gotcha.** Prereq for this live beat: the latest plugin zip uploaded + relaunched so `get_latest_report` is
present in Cowork. If not, show the committed reports directly.

## 22 · What it does well — and the hard 20%

**What it's doing.** The required honest self-eval. Volunteering the limits *before* the panel finds them is
the credibility move. The callout: none of the creative claim rests on fabricated data.

**Have cold.** Works: grounded + cited, compliant by construction, deterministic math, both creative use
cases on real data. Hard 20%: **flag ≠ action** (Crestwood) · value **gated by logging discipline** (Marcus
logs sparsely) · Track A **blind to healthy/construction by design** · **doc-intel is synthetic** (labeled).

**Likely questions → answer.**
- *"What's the single biggest weakness?"* → Adoption, not the tech — and the highest-leverage adopter
  (Marcus) is served by the memo, which is the compliant-cleanup piece, not the creative headline. I hold
  that honestly.
- *"Doesn't synthetic doc-intel undercut the claim?"* → Only doc-intel is synthetic, and it's the compliance
  *showcase*, not the creative claim. Both creative finds (close-the-loop, retention) run on the real files.

**Gotcha.** Don't get defensive here — this slide *is* the answer. Name the limits crisply and move to
adoption.

## 23 · Adoption — a portfolio, not one tool

**What it's doing.** The C through-line: no single tool wins all three RMs. Maps each RM to the demos that win
them, and sequences the rollout (Sarah teaches → Marcus proves → Tom co-authors).

**Have cold.** Sarah wins on A1–A3 + B2 (start here). Tom wins on B1 + B3 (co-builder). Marcus wins on B4
(the memo). Adoption = the CCO's stated #3 risk.

**Likely questions → answer.**
- *"How do you measure adoption?"* → Sarah's "10-minute Monday" (setup time), HITL edit-rate on drafts, and
  per-RM active use — real signals, not licenses sold.
- *"What if Marcus still refuses?"* → Then the memo time-saving has to speak for itself; he's mentoring 4
  juniors, so even partial adoption propagates. I'd co-design with him, not mandate.

**Gotcha.** Resist picking "the one solution." The honest, stronger answer is the portfolio.

## 24 · From pilot to production (+ AWS path)

**What it's doing.** The deployment story: Cowork as the RM surface, §4.1 monitoring pending CCO sign-off,
§2.3 residency (local > cloud), scheduled jobs (prepare-only), plus the hardening cards (query observability,
token/spend budgets, sandboxing) and the **AWS-managed mapping** — which lands with Caylent's AWS-partner
panel.

**Have cold.** AWS mapping: local MCP + guards → **Bedrock AgentCore Gateway** (managed MCP, least-privilege
roles, interceptors, Identity OBO) · **AgentCore Runtime** (microVM isolation, Claude Agent SDK) · **AgentCore
Observability** (OTel → CloudWatch, token/latency/errors) · **Bedrock Guardrails** (PII redaction, denied
topics, cross-account, GA Apr 2026). 90 days → pilot both tracks → CCO sign-off → governed store + funded API
tier.

**Likely questions → answer.**
- *"What breaks at scale (50 borrowers, not 5)?"* → Nothing in the compute (deterministic, per-borrower). The
  real work is connector auth, the governed data store, and **alert-fatigue tuning** so "flag ≠ action"
  doesn't become "flag → ignored."
- *"Did you build on Bedrock?"* → No — the pilot is local MCP + Claude Code/Cowork. AWS is the production
  *target* it maps onto 1:1. Saying that honestly is the point.
- *"Bedrock Guardrails — doesn't that replace your guards?"* → No. Guardrails is **probabilistic and doesn't
  scan `tool_use` outputs**, so our **deterministic server-side guards stay the primary chokepoint**;
  Guardrails is belt-and-suspenders.
- *"Cost?"* → Funded API tier; nightly eval on Sonnet (cheap), demo on Opus; token budgets keep it
  predictable. (June-15-2026 billing moved subscription Agent-SDK/`claude -p` to a separate credit, but
  API-key production bills per token as before — which is what we assume.)

**Gotcha.** Don't say you "built on AgentCore/Guardrails." Say "maps onto." The honesty is the credibility.

## 25 · Close — Built. Trustworthy. Adopted.

**What it's doing.** Lands the three-word spine and the A/B/C braid one last time, then opens Q&A. Subhead:
"compliant by construction, geared for production."

**Likely questions → answer.** This is the Q&A launchpad — see the consolidated hardest-questions below.

**Gotcha.** End on the braid, invite questions, stop talking. Don't re-summarize the whole deck.

---

## Named-entity & number landmines (don't trip)

- **Marcus Webb (RM, Summit, B4) vs Marcus Chen (credit officer, B3).** Two different people. Say "Chen" in B3.
- **All "X days" are from the 2025-05-31 data close**, not June 2026. (457 days to Crestwood maturity; 78-day
  Meridian gap; etc.)
- **78 vs 33 days** (A3): 78 = substantive two-way; 33 = naive log; the 4/28 one-way notice is the 45-day gap.
- **Certified 1.23 / 3.76 vs recomputed 1.03 / 4.50, gap $2.0M** (B2): keep the pairs exact.
- **Your Crestwood rate = 5.05%; competitor First Midwest = 4.90%** (B1). Never quote a recommended renewal rate.
- **Revolver 85% vs 75%** (A2) is an RM-set cap, **not** a loan covenant.
- **Only doc-intel (B2) is synthetic.** Everything else runs on the real files. Guarantor refusal is a planted
  trigger for a real policy.
- **§2.1 = inputs (ratings/watchlist stripped); §4.2 = outputs (no credit language).** `covenant_status` is
  kept as a *fact*; `credit_grade` is *stripped*.
- **Hooks are Code-only**; the **MCP server/core** is the cross-surface chokepoint. Don't claim hooks enforce
  in Cowork.
- **Reliability footer is qualitative, never a %.**

## The hardest questions — rehearse cold

1. **"What's genuinely novel vs what the brief told you to avoid?"** → The avoid-list (memo, covenant
   tracking, overdue emails) is the *compliant cleanup* — I say so out loud. The creative claim is
   **close-the-loop** (did the bank keep its own commitments?), **cross-source reconciliation**, and the
   **retention radar** — combining sources no one reconciles and surfacing the bank's *own* dropped
   follow-through. B3 found a missing draw condition unprompted.
2. **"How is this compliant and not just disclaimered?"** → Enforcement is in **code**: §2.1 strip + the
   guarantor pre-screen at retrieval; deterministic math (not the LLM); `screen_and_finalize` on every output;
   the memo's §4.2 pause that makes the human author the judgment. Disclaimers are explicitly insufficient
   under §4.2 and we don't rely on them.
3. **"What's the weakest part?"** → Adoption, not the tech — and the highest-leverage adopter (Marcus) is best
   served by the memo, the compliant-cleanup piece. Doc-intel is synthetic. Track A is blind to healthy and
   construction by design. I'd rather name these than have you find them.
4. **"Single prompt or multi-step — and were you just adding complexity?"** → The RM types one prompt; under it
   is a multi-tool pipeline. Three of Tom's workflows are correctly single-prompt; only the memo (§4.2) and the
   monitor (§4.1) need decomposition — for compliance, not cleverness.
5. **"Why Claude Code, not Claude for Work?"** → The brief sanctions another agentic tool. I built in Code and
   demo in Cowork (the no-terminal RM surface); the same plugin runs on both, and production maps to managed
   Claude for Work + AWS. The surface isn't the point — the compliant, reusable library is.
6. **"Will the live demo work — and what if it doesn't?"** → It's been Cowork-verified end-to-end. If a call
   stalls live, I show the committed artifact (the PDF/report in the repo) and narrate the chain — the outputs
   are real files, not slideware.

## If a demo breaks live (failure playbook)

- **Stay calm, narrate the chain** from slide 10 while it retries.
- **Fall back to the committed artifact** — every demo writes a real file (`reports/`, `reports/pdf/`); open it
  and walk it.
- **Re-run once**, then move on — don't burn 3 minutes. The eval slides prove it works repeatably.
- **Cowork prereqs:** latest plugin zip uploaded + relaunched (skills load); `.env` with `ANTHROPIC_API_KEY`
  present for the live doc-intel call (B2); MCP bridge live for `mcp__centerline__*`.
