# Speaker notes — Centerline Claude Pilot (tight spoken script)

> The trimmed, spoken version — matches the `<!-- -->` notes embedded in `slides/centerline-claude-pilot.md`.
> ~15–32s per slide; ~45 min total, leaving room for Q&A. (Per-slide Q&A / gotchas: see `panel-qa-prep.md`.)

---

**1 · Cover (~15s)** — "Centerline's Commercial Banking Claude pilot — what I built, run live, with
compliance baked in. Two honesty notes: Centerline's fictional and the data synthetic; and every number
is as-of the 2025-05-31 data close, verifiable against the source."

**2 · Agenda (~15s)** — "The hour: a quick intro, the context, the architecture, then two live demos —
Track A rebuilds Tom's flagged workflow, Track B is what I found myself — and we close on honest eval and
adoption. About 45 minutes, lots of room for questions. I'd love it to be a conversation."

**3 · About me (~20s)** — "Senior AI Engineer at Carta in Toronto — but a hybrid background: data science
and consulting across Intact, EY, Deloitte. Day to day I build on AWS and Anthropic — the APIs and Claude
Code — in document intelligence, the same shape of problem Centerline has. Why this role: I'm a builder who
wants front-line commercial impact, and my edge is judgement and client-facing skill on top of the
engineering. Best proof is the next hour — I built it."

**4 · The situation (~20s)** — "Three RMs, a $350M book, a third of their week lost to docs and covenant
tracking — not clients. Claude bought, nothing deployed. The CCO's one ask: early-warning on contact gaps
and deterioration, RM-private. That's my 90-day mandate — everything I show maps back to it."

**5 · Meet the three RMs (~25s)** — "Three RMs — and the risk is whether they'll use it. Sarah, the
linchpin, was burned by a bad AI pilot, so trust is everything; she trains the floor. Tom, the builder
behind the shadow ChatGPT, wants to co-design. Marcus, the skeptic — 71 memos a year, logs sparsely; win
him and it tips. You'll meet all three in the demos."

**6 · The catalyst (~20s)** — "Tom didn't wait — five AI workflows on personal ChatGPT with client data.
Two violations. The honest read: right instinct, wrong tools. His workflows are the starting point, not the
blueprint. So the question is what the right tools, done compliantly, look like."

**7 · Compliance is the architecture (~22s)** — "Section 4 is trickier than it looks. No creditworthiness
language, even implicitly — disclaimers don't count. Credit grade and watchlist can't even be inputs. No AI
on Special-Assets. Monitoring needs CCO sign-off. Human review before anything ships. The throughline:
judgment originates with the RM, and we enforce it in code — in the tools — not a prompt."

**8 · The signal's already there (~22s)** — "Eight files, through end of May. The signal's already there —
the problem is the record can't be trusted: mis-dated logs, decisions only in email, status labels lagging
the trend. Three finds — Meridian's plan never executed; Crestwood an attrition risk while healthy;
engagement diverging from distress. The job: organize the facts, make the record trustworthy, leave the
judgment with the RM. That's the spine of both demos."

**9 · How I built it (~28s)** — "Five decisions. First the philosophy: LLM-driven workflows Claude
orchestrates, starting with the simplest approach that works — Anthropic's guidance — adding structure only
where compliance demands. Then: a composable skill library, MCP tool-use not paste, server-side guardrails,
Code-to-Cowork. The brief's question — is single-prompt right? The RM types one prompt, but it fires a
multi-tool pipeline. 'Single prompt' was never the problem; a single call with pasted-in confidential data
was. Only the memo (§4.2) and monitoring (§4.1) need an extra human or governance step."

**10 · Architecture in one picture (~22s)** — "The whole system — I'll point back to it on every demo.
Claude picks a skill; the skill calls deterministic MCP tools that do the math and enforce §2.1 and §4.2 —
the model never does the arithmetic or the credit call. Everything routes through one screen step to a
human. One plugin, both surfaces. And the eval loop measures the skills and reports to the CCO."

**11 · Fix Tom's flagged workflow (~30s)** — "Tom's five workflows are really single prompts with data
pasted in. Three — the letter, the email, the call-prep — single prompt is the right call; just swap paste
for retrieval and add §4.3 review. Two need re-architecting, for compliance: the memo decomposes so the RM
authors the assessment (§4.2); the weekly summary becomes a pipeline with deterministic flags and a CCO
gate (§4.1). All five share the real violation — confidential data on personal ChatGPT. Deliverable A
rebuilds that weekly summary: the aggregation was the problem; moving the math into code is the fix."

**12 · A1 — watchlist (~28s)** — "First prompt — 'who needs attention this week?' Watch Claude pick the
watchlist skill — it composes covenant, deterioration, and engagement over the book, then screens. Meridian
#1 — breach, signals, 78 days since contact — Crestwood dead last, zero signals. Every line cites its
source. It ranks and cites — never characterizes credit (§4.2), RM-private. Crestwood at the bottom is the
tool honestly blind to a healthy borrower who's leaving — exactly what Track B catches."

**13 · A2 — covenant compliance (~22s)** — "Meridian — cushion and trend. DSCR 1.03 against a 1.20 floor, a
breach; revolver 85% past Sarah's 75% cap. The tell: the status field read 'Compliant' for months while
DSCR slid 1.45 to 1.03. The math runs in code, not the model — the field said fine, the trend said sliding;
the RM owns the call. The PDF carries the trend chart."

**14 · A3 ★ — engagement coverage (~28s)** — "Our Deliverable-A find — 'who have I gone quiet on?' Days since substantive
two-way contact. Meridian: 78 days as of May 31 — the naive log says 33 because the 4/28 entry was a one-way
notice, a 45-day undercount. RM-private and dismissible — the answer to Sarah's surveillance fear. Then the
bridge: flag isn't action — Tom flagged Crestwood and still lost it. That's why Track B is about the
relationship and the record."

**15 · Track B intro (~22s)** — "Track B is what I found in the data. The brief warns the obvious picks —
memo, covenant tracking, overdue emails — and I built those, but they're the compliant cleanup, not the
claim. The find is close-the-loop — did the bank keep its own commitments — plus reconciliation and
retention. It combines sources no one reconciles. Four prompts, one per RM."

**16 · B1 — retention (~24s)** — "B1 inverts the watchlist. Crestwood — pristine metrics, so it never shows
on early-warning. The retention skill surfaces: matures August 2026, 457 days out; First Midwest dangling
4.90% versus 5.05%; the pricing deadline already passed; no renewal memo. The §4.2 line: it says 'engage' —
it never names a rate; that's the committee's call. The healthy borrower A1 is blind to."

**17 · B2 ★ — document intelligence (~32s)** — "The doc-intel centerpiece — Sarah's, and trust is everything
to her. List, classify — the guarantor personal financials are refused on intake, never sent to a model
(§2.1, in code). The catch: the certificate says compliant at 1.23 / 3.76; the GAAP financials recompute to
a breach at 1.03 / 4.50; the bank's own data agrees with the recompute. The gap is $2M of EBITDA add-backs.
Every figure cites its document, field, and tool — Sarah's scar answered. The footer reads Partial,
honestly. Then a second prompt drafts the missing-docs email — factual asks only. Whether the add-backs are
supported is the RM's call, not mine."

**18 · B3 ★ — reconciliation (~30s)** — "B3 is Deliverable B's creative find, on real data — reconciling email, CRM,
and the data via the relationship timeline. The April-9 CRM row sits two weeks before the real draw thread,
so the file looks fresher than it is. Marcus Chen's 'don't waive the 75%' ruling lives only in email —
surfaced verbatim and attributed, with a propose-only CRM entry. The 71% is still under 75%. The standout
§4.2 line: the AI transcribes the credit officer's decision into the file — it never makes one. Then the
draw letter requests the missing items; Chen's internal disposition stays internal."

**19 · B4 — annual memo (~28s)** — "The skeptic's wedge — Marcus, 71 memos a year. The compliant rebuild of
the memo, decomposed for §4.2. It assembles and cites every factual section, then STOPS and asks Marcus for
his assessment in his own words — the AI never writes the judgment; his words go in verbatim, attributed.
That's §4.2 made literal — it hands him the pen. The yellow box is exactly what Marcus types at the pause —
a genuine credit judgment the AI must never author. Removes the burden without changing how he thinks."

**20 · How the CCO can trust it (~30s)** — "The CCO can't approve what she can't measure. Four layers. Layer
1, a deterministic golden set, 95 of 95 — it tests the tool code; the model isn't called. Layer 2,
observability — per-prompt scorecards. Layer 3, live agent-eval — grades the model's own decisions,
including §4.2 on its narration. Layer 4, an advisory improvement loop. Plus a CI gate blocking failing
merges. Governance: AI proposes, a human disposes (§4.3) — the loop caught a real §4.2 issue and we left it
unapplied. Layer 1 tests the tools; Layer 3 tests the model — don't conflate them."

**21 · Governance, live (~24s)** — "The trust story, concrete — two prompts, live. 'Show me the latest agent
eval' — the scorecard, golden 95/95 plus the live eval, both tracks. 'Show me the proposed improvements' —
the loop's suggestions, including the §4.2 issue it caught, left unapplied. The skills only read — they
never write. AI proposes, a human in Compliance disposes; the audit trail is committed reports."

**22 · Honest 80/20 (~26s)** — "Honest eval. Works: grounded, cited, compliant by construction, deterministic
math, both creative use cases on real data. The hard 20%: flag isn't action — Tom flagged Crestwood and still lost it;
value is gated by logging discipline — Marcus logs sparsely; Track A is blind to healthy and construction by
design — which is why Track B exists; and doc-intel runs on synthetic, labeled docs. But none of the
creative claim rests on fabricated data."

**23 · Adoption (~24s)** — "Adoption is the real risk — the CCO's own goal three — and no single tool wins
all three. Sarah: trust answered by grounding, fear by the RM-private design; start with her, she trains the
floor. Tom: co-builder, his shadow workflow becomes the sanctioned one. Marcus: the memo removes 71 a year
without changing how he thinks. A portfolio — Sarah to teach, Marcus to prove, Tom to co-author."

**24 · Production & rollout (~26s)** — "From pilot to production. Cowork is the RM surface — one plugin, no UI
to build. Monitoring is §4.1 — designed, pending CCO sign-off, fast-trackable. For §2.3 residency, local
scheduled jobs beat cloud. A Sunday pre-compute so Sarah's Monday is ready — prepare-only, never auto-act.
And the hardening: query observability — every query and response logged and scanned for non-compliant
language, not just the artifacts; token and spend budgets per RM and per skill; and sandboxed,
least-privilege execution. And the AWS path — Caylent's stack — our local MCP and guards map one-to-one onto
AgentCore Gateway, Runtime, Observability, and Bedrock Guardrails (defense-in-depth; our deterministic guards
stay the chokepoint). Ninety days: pilot both tracks, CCO sign-off, a governed store and a funded API tier."

**25 · Close (~18s)** — "The whole story in three words. Built — I ran it live. Trustworthy — compliant by
construction, measured, traceable. Adopted — designed per RM. A, kept the instinct; B, the RM keeps the
judgment; C, a portfolio. Happy to take questions — on the demos, the compliance, the eval, or how this
scales to the bank's real data."
