---
marp: true
theme: centerline
paginate: true
size: 16:9
html: true
title: Centerline Bank — Claude Pilot
author: Franck Benichou
footer: '<a href="https://github.com/benichou/centerline-claude-pilot">github.com/benichou/centerline-claude-pilot</a>'
---

<!-- _class: cover -->
<!-- _paginate: false -->

<div class="topbar"></div>

<div class="logo-strip">
  <span class="lockup">
    <img class="logo-caylent" src="images/logos/caylent-icon.png" alt="Caylent">
    <span class="wm-caylent">Caylent</span>
  </span>
  <span class="logo-x">×</span>
  <span class="lockup">
    <img class="logo-centerline" src="images/logos/centerline-dark.svg" alt="">
    <span class="wm-centerline">Centerline&nbsp;Bank</span>
  </span>
</div>

<div class="stamp">Fictional case · synthetic data</div>

<div class="eyebrow">Centerline Bank · Claude Pilot</div>

# AI the RMs actually use,<br/>and the CCO trusts
### Built, not described · Measured, not promised · Compliant by design

<div class="meta">
Technical-challenge presentation · <strong>Commercial Banking</strong><br/>
<strong>Senior Forward Deployed Engineer</strong> candidate · <strong><a href="https://www.linkedin.com/in/franckbenichoudata">Franck Benichou</a></strong><br/>
June 2026
</div>

<!--
NOTES (~15s): "Centerline's Commercial Banking Claude pilot — what I built, run live, with
compliance baked in. Two honesty notes: Centerline's fictional and the data synthetic; and every
number is as-of the 2025-05-31 data close, verifiable against the source."
-->

---

<!-- _class: agenda -->

# Agenda

<div class="lede">Roughly 45 minutes, then questions. Two solutions — run live, not described.</div>

<div class="ag">
  <div class="ag-item"><span class="ag-num">1</span><div><div class="t">Who I am</div><div class="s">A 60-second intro</div></div></div>
  <div class="ag-item"><span class="ag-num">2</span><div><div class="t">The situation</div><div class="s">3 RMs · $350M · a shadow-IT catalyst · §4 compliance · the data</div></div></div>
  <div class="ag-item"><span class="ag-num">3</span><div><div class="t">How we built it</div><div class="s">Composable skills + MCP + server-side guardrails, in one architecture</div></div></div>
  <div class="ag-item"><span class="ag-num">4</span><div><div class="t">Track A — Early-Warning <span class="d">(Deliverable A)</span></div><div class="s">Rebuild Tom's shadow workflow — run live</div></div></div>
  <div class="ag-item"><span class="ag-num">5</span><div><div class="t">Track B — Relationship &amp; Renewal <span class="d">(Deliverable B)</span></div><div class="s">Our creative find — run live</div></div></div>
  <div class="ag-item"><span class="ag-num">6</span><div><div class="t">Trust, eval &amp; adoption</div><div class="s">The honest 80/20, and the path to production</div></div></div>
</div>

<!--
NOTES (~15s): "The hour: a quick intro, the context, the architecture, then two live demos —
Track A rebuilds Tom's flagged workflow, Track B is what I found myself — and we close on honest
eval and adoption. About 45 minutes, lots of room for questions. I'd love it to be a conversation."
-->

---

<!-- _class: about -->

# About me

<div class="two-col">

<div class="card navy">
<div class="ct">Snapshot</div>
<div class="who">
<img class="avatar" src="images/franck-photo.jpg" alt="Franck Benichou">
<div>
<div class="name">Franck Benichou</div>
<div class="role">Senior AI Engineer · Carta (LPPA) · Toronto</div>
</div>
</div>
<ul>
<li><strong>AI Engineering — Document Intelligence</strong></li>
<li><strong>Data Science + Consulting / start-up</strong> — Intact · EY · Deloitte · Carta</li>
<li>Technical reviewer · <a href="https://www.packtpub.com/en-us/product/deepseek-in-practice-9781806020843">DeepSeek in Practice</a> (Packt, 2025)</li>
<li>Founder · <strong>HEC Forecast</strong> student data-science conference (2018 → present)</li>
<li>Français · English · Español</li>
</ul>
</div>

<div>
<div class="ct">Why Caylent's Senior FDE — and why me</div>
<ul class="why">
<li><span class="n">1</span><b>It's the work I already do.</b> AWS + Anthropic is my daily stack — the Anthropic APIs and Claude Code at Carta, in document intelligence.</li>
<li><span class="n">2</span><b>Why I'm excited.</b> I'm an AI builder who wants direct commercial impact on the front lines — prototyping and taking things into production.</li>
<li><span class="n">3</span><b>Why I'm a fit.</b> Beyond building, my unconventional, hybrid background brings judgement and client-facing strength — not just code.</li>
</ul>
</div>

</div>

<!--
NOTES (~20s): "Senior AI Engineer at Carta in Toronto — but a hybrid background: data science and
consulting across Intact, EY, Deloitte. Day to day I build on AWS and Anthropic — the APIs and
Claude Code — in document intelligence, the same shape of problem Centerline has. Why this role:
I'm a builder who wants front-line commercial impact, and my edge is judgement and client-facing
skill on top of the engineering. Best proof is the next hour — I built it."
-->


---

<!-- _class: situation -->

# The situation

<div class="lede">Centerline's Commercial Banking division bought Claude for Work — and deployed nothing <strong>yet</strong>.</div>

<div class="stats">
  <div class="stat"><div class="big">$350M</div><div class="lbl">portfolio managed by <strong>3 relationship managers</strong></div></div>
  <div class="stat"><div class="big">30–40%</div><div class="lbl">of RM time on <strong>documentation, covenant tracking & call prep</strong></div></div>
  <div class="stat"><div class="big">0</div><div class="lbl">workflows in production — <strong>licenses bought, not used</strong></div></div>
</div>

<div class="callout">The CCO, <strong>Rachel Torres</strong>, has one stated priority: <strong>early-warning</strong> on contact gaps and financial deterioration — RM-private, compliance-gated. <em>My 90-day mandate.</em></div>

<!--
NOTES (~20s): "Three RMs, a $350M book, a third of their week lost to docs and covenant tracking —
not clients. Claude bought, nothing deployed. The CCO's one ask: early-warning on contact gaps and
deterioration, RM-private. That's my 90-day mandate — everything I show maps back to it."
-->

---

<!-- _class: personas -->

# Meet the three RMs

<div class="lede">Three RMs, three very different relationships with AI. Adoption is the real risk — so we design for each, not for the org chart.</div>

<div class="three-col">

<div class="card">
<div class="hd">Sarah Okonkwo</div>
<div class="ptag">The linchpin · natural teacher</div>
<p><strong>Book:</strong> Meridian · BlueLine — both in covenant breach</p>
<p>Diligent logger. Burned once by an AI that gave <strong>wrong covenant info</strong> — so trust is existential.</p>
<p class="hook">If she adopts, she trains the team.</p>
</div>

<div class="card">
<div class="hd">Tom DeLuca</div>
<div class="ptag">The builder · power-user</div>
<p><strong>Book:</strong> Crestwood (A-rated) · Arcadia (construction)</p>
<p>Built 5 AI workflows on personal ChatGPT. Wants to <strong>co-design</strong>, not be policed.</p>
<p class="hook">Already proved AI helps — by breaking policy.</p>
</div>

<div class="card">
<div class="hd">Marcus Webb</div>
<div class="ptag">The skeptic · 22-yr veteran</div>
<p><strong>Book:</strong> Summit — DSCR drifting toward the floor</p>
<p>Mentors 4 juniors. <strong>~71 annual memos/yr</strong>. Logs sparsely; trusts his own memory.</p>
<p class="hook">Win him and the rollout tips.</p>
</div>

</div>

<div class="rmdef"><strong>RM = Relationship Manager</strong> — a commercial bank's primary owner of a business-borrower relationship: monitors covenants and financial health, prepares periodic reviews and renewals, and is the client's main point of contact.</div>

<!--
NOTES (~25s): "Three RMs — and the risk is whether they'll use it. Sarah, the linchpin, was burned
by a bad AI pilot, so trust is everything; she trains the floor. Tom, the builder behind the shadow
ChatGPT, wants to co-design. Marcus, the skeptic — 71 memos a year, logs sparsely; win him and it
tips. You'll meet all three in the demos."
-->

---

<!-- _class: catalyst -->

# The catalyst — one RM didn't wait

<div class="two-col">

<div class="card flag">
<span class="tag red">IT audit finding</span>
<div class="hd" style="margin-top:10px">Tom built 5 AI workflows on personal ChatGPT</div>
<p>Client financials and names in a personal account — <strong>two compliance violations.</strong> Five workflows: draw letters · memos · client emails · call-prep · weekly summary.</p>
</div>

<div>
<div class="ct">The reframe</div>
<ul class="why">
<li><span class="n">→</span><b>Right instinct, wrong tools.</b> Tom proved AI helps here — by breaking policy to do it.</li>
<li><span class="n">→</span><b>Starting point, not blueprint.</b> We keep the instinct, fix the violations, and turn one person's hack into a governed, shareable library.</li>
</ul>
</div>

</div>

<!--
NOTES (~20s): "Tom didn't wait — five AI workflows on personal ChatGPT with client data. Two
violations. The honest read: right instinct, wrong tools. His workflows are the starting point,
not the blueprint. So the question is what the right tools, done compliantly, look like."
-->

---

<!-- _class: compliance -->

# Compliance isn't a wrapper — it's the architecture

<div class="lede">Section 4 is trickier than it looks. Five constraints decided every design choice that follows.</div>

<div class="policy">
  <div class="pol"><div class="sec">Section 4.2</div><div class="d">No creditworthiness language — even implicitly. A disclaimer does <strong>not</strong> count.</div></div>
  <div class="pol"><div class="sec">Section 2.1</div><div class="d">Credit grade / watchlist can't even be <strong>inputs</strong> to the AI.</div></div>
  <div class="pol"><div class="sec">Section 5</div><div class="d">No AI on <strong>Special-Assets</strong> or litigation credits.</div></div>
  <div class="pol"><div class="sec">Section 4.1</div><div class="d">Automated monitoring needs <strong>CCO approval</strong> to launch.</div></div>
  <div class="pol"><div class="sec">Section 4.3</div><div class="d"><strong>Human review</strong> before anything is client-facing or filed.</div></div>
</div>

<div class="callout">The credit <strong>judgment must originate with the RM.</strong> Claude organizes facts and flags gaps — it never characterizes credit. And we enforce that <strong>in code, not in a prompt.</strong></div>

<!--
NOTES (~22s): "Section 4 is trickier than it looks. No creditworthiness language, even implicitly —
disclaimers don't count. Credit grade and watchlist can't even be inputs. No AI on Special-Assets.
Monitoring needs CCO sign-off. Human review before anything ships. The throughline: judgment
originates with the RM, and we enforce it in code — in the tools — not a prompt."
-->

---

<!-- _class: data -->

# The signal's already there — the record can't be trusted

<div class="lede">Eight files, current through <strong>2025-05-31</strong>. The hard part isn't finding data — the system of record is wrong three ways: <strong>mis-dated logs · decisions that live only in email · status labels that lag the trend.</strong></div>

<div class="three-col">
  <div class="card"><div class="hd">Meridian</div><p>A careful action plan in the memo — that the data shows was <strong>never executed</strong>.</p></div>
  <div class="card"><div class="hd">Crestwood</div><p><strong>Attrition risk on a pristine, healthy borrower</strong> — invisible to every distress metric.</p></div>
  <div class="card"><div class="hd">Across the book</div><p>Engagement <strong>diverges from distress</strong> — RMs go quiet on the credits that are sliding.</p></div>
</div>

<div class="callout">So the job isn't to find hidden data. It's to <strong>organize scattered facts and make the record trustworthy</strong> — and leave the judgment with the RM. <em>That's the spine of both demos.</em></div>

<!--
NOTES (~22s): "Eight files, through end of May. The signal's already there — the problem is the
record can't be trusted: mis-dated logs, decisions only in email, status labels lagging the trend.
Three finds — Meridian's plan never executed; Crestwood an attrition risk while healthy; engagement
diverging from distress. The job: organize the facts, make the record trustworthy, leave the
judgment with the RM. That's the spine of both demos."
-->

---

<!-- _class: approach -->

# How I built it

<div class="lede">Five decisions — and an honest answer to the brief's "is a single prompt the right architecture?"</div>

<div class="grid2">
  <div class="card lead"><div class="hd">LLM-driven workflows, simplest-first <span class="sub">(Anthropic guidance)</span></div></div>
  <div class="card"><div class="hd">Composable skill library</div><p>Small, single-purpose skills Claude selects and composes — not one mega-prompt.</p></div>
  <div class="card"><div class="hd">MCP tool-use over copy-paste</div><p>Retrieval and computation are tools — which is also what makes Tom's workflow compliant.</p></div>
  <div class="card"><div class="hd">Guardrails server-side</div><p>§2.1 / §4.2 enforced in the tools — they hold no matter what the model says, on any surface.</p></div>
  <div class="card"><div class="hd">Build in Code → demo in Cowork</div><p>Cowork is the RM's no-terminal surface — the UI is the product, with no UI to build.</p></div>
</div>

<div class="callout"><strong>Single prompt or multi-step?</strong> The RM still types <strong>one prompt</strong> — but it now fires a multi-tool pipeline. Only the <strong>memo (§4.2)</strong> and <strong>monitoring (§4.1)</strong> need a genuine extra human / governance step.</div>

<!--
NOTES (~28s): "Five decisions. First the philosophy: LLM-driven workflows Claude orchestrates,
starting with the simplest approach that works — Anthropic's guidance — adding structure only where
compliance demands. Then: a composable skill library, MCP tool-use not paste, server-side guardrails,
Code-to-Cowork. The brief's question — is single-prompt right? The RM types one prompt, but it fires a
multi-tool pipeline. 'Single prompt' was never the problem; a single call with pasted-in confidential
data was. Only the memo (§4.2) and monitoring (§4.1) need an extra human or governance step."
-->

---

<!-- _class: archslide -->

# Architecture in one picture

<div class="lede">The AI organizes the facts; <strong>people keep the judgment</strong> — and every output passes through one compliance chokepoint.</div>

<div class="exflow">
  <div class="exstage s-in">
    <div class="et">Inputs</div>
    <div class="es">Claude Code &amp; Cowork surfaces · the bank's records &amp; documents</div>
  </div>
  <div class="exarrow">→</div>
  <div class="exstage s-skill">
    <div class="et">Claude skill library</div>
    <div class="es">selects &amp; orchestrates the workflow</div>
  </div>
  <div class="exarrow">→</div>
  <div class="exstage s-mcp">
    <div class="mcp-title">centerline MCP server — the compliance chokepoint</div>
    <div class="mcp-steps">
      <div class="mstep"><div class="mt">Strip restricted data</div><div class="ms">ratings · watchlist · guarantor never reach the model</div></div>
      <div class="mstep"><div class="mt">Compute in code</div><div class="ms">the math runs deterministically, not in the LLM</div></div>
      <div class="mstep"><div class="mt">Screen every output</div><div class="ms">no credit-adjacent language · reliability footer</div></div>
    </div>
  </div>
  <div class="exarrow">→</div>
  <div class="exstage s-human">
    <div class="et">Human in the loop <span style="font-weight:700">(HITL)</span></div>
    <div class="es">credit-file-ready draft → RM reviews · CCO governs</div>
  </div>
</div>

<div class="portribbon"><strong>Packaged as one plugin</strong> — the same compliant workflows run in <strong>Claude Code</strong> and <strong>Claude Cowork</strong>, the RM's no-terminal surface.</div>

<div class="evalribbon"><strong>Continuously evaluated</strong> — golden tests · live agent-eval · CI gate · reported to the CCO</div>

<!--
NOTES (~22s): "The whole system — I'll point back to it on every demo. Claude picks a skill; the skill
calls deterministic MCP tools that do the math and enforce §2.1 and §4.2 — the model never does the
arithmetic or the credit call. Everything routes through one screen step to a human. One plugin, both
surfaces. And the eval loop measures the skills and reports to the CCO."
-->

---

<!-- _class: trackA -->

<div class="kicker">Track A · Deliverable A</div>

# Fix Tom's flagged workflow

<div class="lede">Tom's five shadow workflows — what's compliant as-is, and what genuinely needs re-architecting (the brief's "is one prompt right?").</div>

| Tom's workflow | Right architecture? | The compliance issue |
|---|---|---|
| Draw-response letter · client email · call-prep | ✅ **Keep as one prompt** (retrieve, not paste) | §4.3 review · no credit bad-news |
| **Relationship memo** | ❌ **Break up** — RM writes the assessment | **§4.2** — the AI may not author the credit judgment |
| **Weekly portfolio summary** *(→ Track A)* | ❌ **Break up** — code computes the flags | **§4.1** — monitoring needs CCO sign-off |
| *all five* | — | **§1 / §2 / §5** — confidential data on a personal ChatGPT |

<div class="callout"><strong>Deliverable A rebuilds the weekly summary</strong> as the early-warning: <strong>retrieve · deterministic flags · screen</strong> — RM-private, §4.1-gated. The aggregation <em>was</em> the problem; moving the math into code is the fix.</div>

<!--
NOTES (~30s): "Tom's five workflows are really single prompts with data pasted in. Three — the letter,
the email, the call-prep — single prompt is the right call; just swap paste for retrieval and add §4.3
review. Two need re-architecting, for compliance: the memo decomposes so the RM authors the assessment
(§4.2); the weekly summary becomes a pipeline with deterministic flags and a CCO gate (§4.1). All five
share the real violation — confidential data on personal ChatGPT. Deliverable A rebuilds that weekly
summary: the aggregation was the problem; moving the math into code is the fix."
-->

---

<!-- _class: demo -->

<div class="demohdr"><span class="kicker">Track A · A1 — watchlist</span><span class="persona">For: <b>the CCO</b> · portfolio early-warning</span></div>

# "Who needs attention this week?"

<div class="promptbar"><span class="lab">Prompt</span>Who in my portfolio needs attention this week? Rank them and show me the facts behind each — don't characterize their credit, just the numbers and the gaps.</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li>Ranked by <strong>risk × neglect</strong> — Meridian #1, Crestwood last</li>
<li>Every line <strong>cited</strong> — it ranks, it doesn't judge</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>loan_performance · activity_log · portfolio_ref — all borrowers, §2.1-stripped</div>
<div class="chain"><span class="sk">assembling-watchlist-triage</span><span class="ar">→</span><span>assemble_watchlist</span><span class="ar">→</span><span>covenant · deterioration · engagement</span><span class="ar">→</span><span>screen_and_finalize</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span></div>
<div class="io out"><span class="iolab out">Output</span>ranked watchlist (cited) + Centerline PDF</div>
</div>
</div>

<div class="point"><strong>The point:</strong> it ranks and cites — never characterizes credit (§4.2), RM-private. Crestwood sinks to the bottom: distress monitoring is blind to a <em>healthy</em> borrower — which sets up Track B.</div>

<!--
NOTES (~28s): "First prompt — 'who needs attention this week?' Watch Claude pick the watchlist skill —
it composes covenant, deterioration, and engagement over the book, then screens. Meridian #1 — breach,
signals, 78 days since contact — Crestwood dead last, zero signals. Every line cites its source. It
ranks and cites — never characterizes credit (§4.2), RM-private. Crestwood at the bottom is the tool
honestly blind to a healthy borrower who's leaving — exactly what Track B catches."
-->

---

<!-- _class: demo -->

<div class="demohdr"><span class="kicker">Track A · A2 — covenant compliance</span><span class="persona">For: <b>Sarah</b> · her borrower Meridian</span></div>

# "Is Meridian compliant — cushion *and* trend?"

<div class="promptbar"><span class="lab">Prompt</span>Is Meridian covenant-compliant as of the latest month? Show DSCR and leverage against their covenant thresholds with the cushion, the revolver level, and whether the reported status matches the trend.</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li>DSCR <strong>1.03 vs 1.20</strong> (breach) · leverage 4.5 · revolver <strong>85% vs the 75% cap</strong></li>
<li>The status field read <strong>"Compliant"</strong> while DSCR slid 1.45 → 1.03</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>loan_performance — Meridian's 17-month series + covenant thresholds</div>
<div class="chain"><span class="sk">checking-covenant-compliance</span><span class="ar">→</span><span>check_covenant_compliance</span><span class="ar">+</span><span>detect_deterioration_signals</span><span class="ar">→</span><span>screen + render_pdf</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span></div>
<div class="io out"><span class="iolab out">Output</span>compliance readout + DSCR-vs-floor trend chart (PDF)</div>
</div>
</div>

<div class="point"><strong>The point:</strong> the math runs <strong>in code, not the LLM</strong>. The field said "fine"; the trend said "sliding." The AI shows both as facts — the RM owns the call.</div>

<!--
NOTES (~22s): "Meridian — cushion and trend. DSCR 1.03 against a 1.20 floor, a breach; revolver 85%
past Sarah's 75% cap. The tell: the status field read 'Compliant' for months while DSCR slid 1.45 to
1.03. The math runs in code, not the model — the field said fine, the trend said sliding; the RM owns
the call. The PDF carries the trend chart."
-->

---

<!-- _class: demo -->

<div class="demohdr"><span class="kicker">Track A · A3 ★ — engagement coverage</span><span class="persona">For: <b>Sarah</b> · Meridian (answers her fear)</span></div>

# "Who have I gone quiet on?"

<div class="promptbar"><span class="lab">Prompt</span>Which of my distressed borrowers have I actually gone quiet on? Count days since the last real two-way contact — a one-way notice or a missed call doesn't count.</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li>Meridian: <strong>78 days</strong> of substantive silence (as of 2025-05-31)</li>
<li>Naive log reads 33 — a one-way notice isn't contact → <strong>undercounts by 45 days</strong></li>
<li>A risk <strong>no single field flags</strong> — RM-private &amp; dismissible</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>activity_log + emails — Meridian (two-way contact only)</div>
<div class="chain"><span class="sk">measuring-engagement-coverage</span><span class="ar">→</span><span>measure_engagement_coverage</span><span class="ar">→</span><span>screen + render_pdf</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span></div>
<div class="io out"><span class="iolab out">Output</span>engagement-gap readout + chart (PDF)</div>
</div>
</div>

<div class="point bridge"><strong>Flag ≠ action.</strong> Tom's own weekly summary flagged the Crestwood gap — and he still lost momentum. Detection isn't enough → that's why <strong>Track B</strong> is about the relationship and the record.</div>

<!--
NOTES (~28s): "Our Deliverable-A find — 'who have I gone quiet on?' Days since substantive two-way contact. Meridian:
78 days as of May 31 — the naive log says 33 because the 4/28 entry was a one-way notice, a 45-day
undercount. RM-private and dismissible — the answer to Sarah's surveillance fear. Then the bridge: flag
isn't action — Tom flagged Crestwood and still lost it. That's why Track B is about the relationship
and the record."
-->

---

<!-- _class: trackB -->

<div class="kicker">Track B · Deliverable B</div>

# Our own find — Relationship & Renewal

<div class="lede">The use case I found by reading the data — not on Tom's list, and not the obvious pain point.</div>

<div class="two-col">
<div class="card claim">
<div class="hd">The creative claim</div>
<ul>
<li><strong>Close-the-loop</strong> — verify the bank kept <em>its own</em> commitments</li>
<li><strong>Cross-source reconciliation</strong> — emails ↔ CRM ↔ structured data</li>
<li><strong>Proactive retention</strong> — catch the healthy client before they shop</li>
</ul>
<p>Combines sources no one reconciles — a risk Tom didn't see.</p>
</div>
<div class="card">
<div class="hd">Compliant cleanup of Tom's other workflows</div>
<ul>
<li>Relationship memo · covenant-package intake · overdue-docs email</li>
<li>The brief's "avoid" list — rebuilt compliant</li>
<li><strong>Explicitly not</strong> the creative claim</li>
</ul>
</div>
</div>

<div class="callout">Said out loud: the brief says don't headline the memo, covenant-tracking, or overdue emails — so those are the <strong>compliant cleanup</strong>. The find is <strong>close-the-loop + reconciliation + retention</strong>, demoed across all three RMs.</div>

<!--
NOTES (~22s): "Track B is what I found in the data. The brief warns the obvious picks — memo, covenant
tracking, overdue emails — and I built those, but they're the compliant cleanup, not the claim. The
find is close-the-loop — did the bank keep its own commitments — plus reconciliation and retention. It
combines sources no one reconciles. Four prompts, one per RM."
-->

---

<!-- _class: demo fill -->

<div class="demohdr"><span class="kicker">Track B · B1 — retention radar</span><span class="persona">For: <b>Tom</b> · Crestwood</span></div>

# "Prep me for my Crestwood meeting"

<div class="promptbar"><span class="lab">Prompt</span>Prep me for my Crestwood meeting — pull the relationship picture, the renewal/maturity clock, and the competitive situation; flag anything I should act on before they shop us.</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li>The <strong>inversion</strong>: the one you lose by being <em>slow</em>, not by credit risk — pristine metrics</li>
<li>Matures 2026-08-31 (<strong>457 days</strong>) · First Midwest <strong>4.90%</strong> vs your 5.05% · pricing-exception deadline passed · no renewal memo</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>portfolio_ref · loan_performance · activity_log · emails — Crestwood</div>
<div class="chain"><span class="sk">flagging-renewal-and-retention</span><span class="ar">→</span><span>flag_renewal_and_retention</span><span class="ar">→</span><span>get_relationship_timeline</span><span class="ar">→</span><span>screen + render_pdf</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span></div>
<div class="io out"><span class="iolab out">Output</span>meeting-prep brief (PDF)</div>
</div>
</div>

<div class="point"><strong>The point:</strong> facts and "engage" — <strong>never a rate</strong> (§4.2; pricing is the committee's call). The <em>healthy</em> borrower A1 is structurally blind to.</div>

<!--
NOTES (~24s): "B1 inverts the watchlist. Crestwood — pristine metrics, so it never shows on early-
warning. The retention skill surfaces: matures August 2026, 457 days out; First Midwest dangling 4.90%
versus 5.05%; the pricing deadline already passed; no renewal memo. The §4.2 line: it says 'engage' —
it never names a rate; that's the committee's call. The healthy borrower A1 is blind to."
-->

---

<!-- _class: demo -->

<div class="demohdr"><span class="kicker">Track B · B2 ★ — document intelligence</span><span class="persona">For: <b>Sarah</b> · Meridian package</span></div>

# "What's in the package — and do the ratios reconcile?"

<div class="promptbar"><span class="lab">Prompt</span>Sarah's Meridian Q1 covenant package just arrived in data/synthetic/meridian-package/. Review it — what's in it, what's missing, and do the ratios reconcile?</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li>§2.1 <strong>guarantor financials refused on intake</strong> · ACORD insurance cert → <code>other</code>, skipped</li>
<li>Certified <strong>1.23 / 3.76</strong> vs recomputed <strong>1.03 / 4.50</strong> — gap = <strong>$2.0M EBITDA add-backs</strong>; the bank's own data agrees with the recompute</li>
<li>Footer reads <strong>Partial</strong>, each reason tagged <code>[tool · source]</code>. <strong>Then:</strong> "Draft the missing-docs email" (wf3)</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>6 covenant-package PDFs (synthetic) + loan_performance</div>
<div class="chain"><span class="sk">reviewing-covenant-package</span><span class="ar">→</span><span>list_documents</span><span class="ar">→</span><span>classify_document</span><span class="ar">→</span><span>§2.1 prescreen</span><span class="ar">→</span><span>extract_document_fields</span><span class="ar">→</span><span>cross_validate_covenant</span><span class="ar">→</span><span>review_package</span><span class="ar">→</span><span>screen + render_pdf</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span></div>
<div class="io out"><span class="iolab out">Output</span>provenance-tagged intake readout (PDF) + missing-docs email</div>
</div>
</div>

<div class="point"><strong>Sarah's scar:</strong> every figure cites its document + field + tool; the §2.1 refusal is <strong>enforced, not a disclaimer</strong>; whether the §1.01 add-backs are adequately supported is <strong>the RM's call, not mine</strong> (§4.2).</div>

<!--
NOTES (~32s): "The doc-intel centerpiece — Sarah's, and trust is everything to her. List, classify —
the guarantor personal financials are refused on intake, never sent to a model (§2.1, in code). The
catch: the certificate says compliant at 1.23 / 3.76; the GAAP financials recompute to a breach at
1.03 / 4.50; the bank's own data agrees with the recompute. The gap is $2M of EBITDA add-backs. Every
figure cites its document, field, and tool — Sarah's scar answered. The footer reads Partial, honestly.
Then a second prompt drafts the missing-docs email — factual asks only. Whether the add-backs are
supported is the RM's call, not mine."
-->

---

<!-- _class: demo -->

<div class="demohdr"><span class="kicker">Track B · B3 ★ — reconciliation</span><span class="persona">For: <b>Tom</b> · Arcadia</span></div>

# "Reconcile the emails vs the CRM log"

<div class="promptbar"><span class="lab">Prompt</span>Reconcile Arcadia's email thread against the CRM log — what actually happened, what's mis-dated, what decision isn't in the file, and what's still open?</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li>The Apr-09 CRM row sits <strong>~2 weeks before</strong> the real Apr-22→25 thread — it poisons contact-recency</li>
<li>Marcus Chen's <strong>"don't waive the 75%"</strong> ruling lives only in email → surfaced <strong>verbatim + attributed</strong>, with a <strong>propose-only</strong> CRM entry</li>
<li>Open: 71% &lt; 75%, Friday docs, names withheld. <strong>Then:</strong> "Draft the draw-response letter" (wf1)</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>emails + activity_log + loan_performance — Arcadia</div>
<div class="chain"><span class="sk">detecting-cross-source-discrepancies</span><span class="ar">+</span><span class="sk">verifying-commitment-fulfillment</span><span class="ar">→</span><span>get_relationship_timeline</span><span class="ar">→</span><span>get_emails</span><span class="ar">→</span><span>detect_deterioration_signals</span><span class="ar">→</span><span>screen + render_pdf</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span></div>
<div class="io out"><span class="iolab out">Output</span>reconciliation readout (PDF) + draw-response letter</div>
</div>
</div>

<div class="point"><strong>The §4.2 moment:</strong> the AI <strong>transcribes the credit officer's decision into the file — it never makes one</strong>. It combines sources no one reconciles, and surfaces the bank's own dropped follow-through.</div>

<!--
NOTES (~30s): "B3 is Deliverable B's creative find, on real data — reconciling email, CRM, and the data via the
relationship timeline. The April-9 CRM row sits two weeks before the real draw thread, so the file
looks fresher than it is. Marcus Chen's 'don't waive the 75%' ruling lives only in email — surfaced
verbatim and attributed, with a propose-only CRM entry. The 71% is still under 75%. The standout §4.2
line: the AI transcribes the credit officer's decision into the file — it never makes one. Then the
draw letter requests the missing items; Chen's internal disposition stays internal."
-->

---

<!-- _class: demo -->

<div class="demohdr"><span class="kicker">Track B · B4 — annual memo</span><span class="persona">For: <b>Marcus</b> · Summit</span></div>

# "Build my Summit annual relationship-review memo"

<div class="promptbar"><span class="lab">Prompt</span>Build my Summit annual relationship-review memo.</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li>AI <strong>assembles + cites</strong> every factual section (17-mo DSCR arc, covenant table, engagement, open items)…</li>
<li>…then <strong>⏸ STOPS</strong> and asks Marcus for his assessment <strong>in his own words</strong> — the AI never writes the judgment</li>
<li>Drafts the narrative <strong>around his verbatim words</strong>. Removes ~71 memos/yr without changing how he thinks</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>loan_performance · activity_log · emails · portfolio_ref — Summit</div>
<div class="chain"><span class="sk">drafting-relationship-review-memos</span><span class="ar">→</span><span>assemble + cite (client-360)</span><span class="ar">→</span><span class="hu">⏸ RM writes the assessment</span><span class="ar">→</span><span>draft → screen + render_pdf</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span><span><span class="sw hu"></span>human step</span></div>
<div class="io out"><span class="iolab out">Output</span>annual memo (markdown + PDF)</div>
</div>
</div>

<div class="rmwrites"><span class="rwl">⏸ The human step — what Marcus fills in (verbatim, attributed)</span><em>"Coverage thinned to 1.12x, just over the 1.10x floor — but I read it as seasonal softness, not a structural decline; leverage at 3.6x leaves cushion. My real concern is commercial, not credit: the Location-3 renewal at an 18% bump, and Castillo's sounded more stressed lately. Eyes on the Q2 package before I move my view."</em><span class="rwmeta">Outlook <b>Watch / monitor</b> · Next steps <b>follow up on the Location-3 lease; request updated Q2 projections</b> · Filed under <b>Marcus Webb (RM of record)</b></span></div>

<div class="point"><strong>§4.2, made literal:</strong> the AI assembles the 80%; Marcus owns the credit judgment it never writes. The skeptic's wedge.</div>

<!--
NOTES (~28s): "The skeptic's wedge — Marcus, 71 memos a year. The compliant rebuild of the memo,
decomposed for §4.2. It assembles and cites every factual section, then STOPS and asks Marcus for his
assessment in his own words — the AI never writes the judgment; his words go in verbatim, attributed.
That's §4.2 made literal — it hands him the pen. The yellow box is exactly what Marcus types at the pause —
a genuine credit judgment the AI must never author. Removes the burden without changing how he thinks."
-->

---

<!-- _class: trust -->

<div class="kicker">Trust · eval &amp; governance</div>

# How the CCO can trust it — with closed-loop learning

<div class="lede">Reliability is a <strong>reported number across both tracks</strong> — not a vibe. Four eval layers, plus a CI prod-gate.</div>

<div class="grid2">
<div class="card"><span class="lyr">Layer 1</span><div class="hd">Deterministic golden set</div><p><strong>95/95</strong> source-grounded cases across A1–A3 + B1–B4. Tests the <strong>tool code</strong> — the LLM is never invoked.</p></div>
<div class="card"><span class="lyr">Layer 2</span><div class="hd">Observability</div><p>Per-prompt scorecards — expected-vs-actual steps, guard hits, reliability footer, latency — across every demo prompt.</p></div>
<div class="card"><span class="lyr">Layer 3</span><div class="hd">Live agent-eval</div><p>Runs the prompts through Claude headless and grades the <strong>model's own decisions</strong> — tool choice, §4.2 on its narration, fact faithfulness.</p></div>
<div class="card"><span class="lyr">Layer 4</span><div class="hd">Improvement loop</div><p><strong>Advisory only</strong> — proposes skill edits, can't touch guards / core / eval keys. A human applies them.</p></div>
</div>

<div class="callout"><strong>AI proposes, a human disposes (§4.3).</strong> The loop caught a real §4.2 footer issue — left unapplied as a live governance artifact. A <strong>CI prod-merge gate</strong> (black · flake8 · deterministic suites) blocks any failing merge. <em>Layer 1 tests the tools; Layer 3 tests the model — don't conflate them.</em></div>

<!--
NOTES (~30s): "The CCO can't approve what she can't measure. Four layers. Layer 1, a deterministic
golden set, 95 of 95 — it tests the tool code; the model isn't called. Layer 2, observability —
per-prompt scorecards. Layer 3, live agent-eval — grades the model's own decisions, including §4.2 on
its narration. Layer 4, an advisory improvement loop. Plus a CI gate blocking failing merges.
Governance: AI proposes, a human disposes (§4.3) — the loop caught a real §4.2 issue and we left it
unapplied. Layer 1 tests the tools; Layer 3 tests the model — don't conflate them."
-->

---

<!-- _class: demo -->

<div class="demohdr"><span class="kicker">Trust · governance — live</span><span class="persona">For: <b>the CCO</b> + Compliance</span></div>

# "How is it doing — and what should we change?"

<div class="promptbar"><span class="lab">Run live</span>"Show me the latest agent eval."<br/>"Show me the latest proposed improvements to our skills and automations."</div>

<div class="demo-grid">
<div class="seeit">
<div class="lbl">What you'll see</div>
<ul>
<li><strong>Eval scorecard</strong> — golden 95/95 + the live agent-eval, across both tracks</li>
<li><strong>Improvement proposals</strong> — incl. the §4.2 footer finding the loop caught, <strong>left unapplied</strong> for a human to approve</li>
</ul>
</div>
<div class="under">
<div class="lbl">Under the hood</div>
<div class="io in"><span class="iolab in">Input</span>committed eval + improvement reports (pulled fresh, cross-surface)</div>
<div class="chain"><span class="sk">viewing-eval-results</span><span class="ar">+</span><span class="sk">viewing-proposed-improvements</span><span class="ar">→</span><span>get_latest_report</span></div>
<div class="chain-legend"><span><span class="sw sk"></span>skill</span><span><span class="sw tl"></span>MCP tool</span></div>
<div class="io out"><span class="iolab out">Output</span>the scorecard + the proposals, shown in Cowork</div>
</div>
</div>

<div class="point"><strong>The loop drives the work:</strong> it independently caught the §4.2 issue and proposed the exact fix — we left it unapplied. <strong>AI proposes, a human disposes (§4.3)</strong> — the CCO's audit trail.</div>

<!--
NOTES (~24s): "The trust story, concrete — two prompts, live. 'Show me the latest agent eval' — the
scorecard, golden 95/95 plus the live eval, both tracks. 'Show me the proposed improvements' — the
loop's suggestions, including the §4.2 issue it caught, left unapplied. The skills only read — they
never write. AI proposes, a human in Compliance disposes; the audit trail is committed reports."
-->

---

<!-- _class: eval80 -->

<div class="kicker">Honest evaluation</div>

# What it does well — and the hard 20%

<div class="two-col">
<div class="card claim">
<div class="hd">✓ What works</div>
<ul>
<li>Grounded &amp; <strong>cited</strong>; compliant <strong>by construction</strong></li>
<li>The math is <strong>deterministic</strong>, not the LLM</li>
<li>Reusable across the book; both creative use cases run on <strong>real data</strong></li>
</ul>
</div>
<div class="card flag">
<div class="hd">The hard 20%</div>
<ul>
<li><strong>Flag ≠ action</strong> — Tom flagged Crestwood and still lost momentum</li>
<li>Value is <strong>gated by logging discipline</strong> (Marcus logs sparsely)</li>
<li>Track A is <strong>blind</strong> to healthy &amp; construction borrowers — by design</li>
<li>Doc-intel runs on <strong>synthetic</strong> documents (clearly labeled)</li>
</ul>
</div>
</div>

<div class="callout">This is the honest 80/20 — what works, and where it falls short. And <strong>none of the creative claim rests on fabricated data</strong>: both creative use cases run on the real files.</div>

<!--
NOTES (~26s): "Honest eval. Works: grounded, cited, compliant by construction, deterministic math, both
creative use cases on real data. The hard 20%: flag isn't action — Tom flagged Crestwood and still lost it; value is
gated by logging discipline — Marcus logs sparsely; Track A is blind to healthy and construction by
design — which is why Track B exists; and doc-intel runs on synthetic, labeled docs. But none of the
creative claim rests on fabricated data."
-->

---

<!-- _class: adoption -->

<div class="kicker">Adoption — the real risk</div>

# No single tool wins all three RMs — a portfolio does

<div class="three-col">
<div class="card">
<div class="hd">Sarah</div>
<div class="ptag">Start here · she trains the team</div>
<p>Her trust scar → grounding; her surveillance fear → RM-private design. The "10-minute Monday."</p>
<div class="lever">Wins on: A1–A3 + B2</div>
</div>
<div class="card">
<div class="hd">Tom</div>
<div class="ptag">The co-builder</div>
<p>Shadow workflow → sanctioned &amp; shareable (§6 amnesty). Make him the partner, not the cautionary tale.</p>
<div class="lever">Wins on: B1 + B3</div>
</div>
<div class="card">
<div class="hd">Marcus</div>
<div class="ptag">The skeptic · make-or-break</div>
<p>The memo removes ~71/yr <strong>without changing how he thinks</strong> — §4.2 hands him the pen.</p>
<div class="lever">Wins on: B4</div>
</div>
</div>

<div class="callout">Adoption is the CCO's stated #3 risk. <strong>Start with Sarah</strong> (she trains the floor), <strong>Marcus</strong> is the proof point, <strong>Tom</strong> co-authors — a portfolio, not one tool.</div>

<!--
NOTES (~24s): "Adoption is the real risk — the CCO's own goal three — and no single tool wins all three.
Sarah: trust answered by grounding, fear by the RM-private design; start with her, she trains the floor.
Tom: co-builder, his shadow workflow becomes the sanctioned one. Marcus: the memo removes 71 a year
without changing how he thinks. A portfolio — Sarah to teach, Marcus to prove, Tom to co-author."
-->

---

<!-- _class: production -->

<div class="kicker">Production</div>

# From pilot to production

<div class="grid2 g3">
<div class="card"><div class="hd">Cowork = the RM surface</div><p>One plugin, no terminal, no UI to build — the same compliant workflows the RMs already saw.</p></div>
<div class="card"><div class="hd">Monitoring · §4.1</div><p>Presented as designed, RM-private, <strong>pending CCO sign-off</strong> — fast-trackable.</p></div>
<div class="card"><div class="hd">Residency · §2.3</div><p>Local scheduled jobs &gt; cloud routines — the bank's data stays put.</p></div>
<div class="card"><div class="hd">Scheduled jobs</div><p>A Sunday-night pre-compute → Sarah's watchlist + open items waiting Monday. Prepare-only, never auto-act.</p></div>
<div class="card"><div class="hd">Query observability &amp; cost</div><p>Every query + response logged and <strong>scanned for non-compliant (§4.2) language</strong> — not just artifacts; per-RM/skill <strong>token &amp; spend budgets</strong> with caps + alerts. OTel → Datadog.</p></div>
<div class="card"><div class="hd">Sandboxing &amp; least-privilege MCP connectors</div><p>The MCP server reaches real data through <strong>least-privilege, read-only connectors</strong>; skills run sandboxed — defense beyond the server chokepoint.</p></div>
</div>

<div class="awspath"><span class="awslab">Production path on AWS</span> Our local MCP + guards map 1:1 onto <strong>Bedrock AgentCore Gateway</strong> (managed MCP · least-privilege) · <strong>Runtime</strong> (microVM isolation) · <strong>Observability</strong> (token · OTel → CloudWatch / Datadog) · <strong>Bedrock Guardrails</strong> — defense-in-depth on our deterministic guards.</div>

<div class="callout"><strong>What 90 days delivers:</strong> pilot both tracks with the three RMs → CCO sign-off on monitoring → a governed data store + funded API tier for rollout.</div>

<!--
NOTES (~26s): "From pilot to production. Cowork is the RM surface — one plugin, no UI to build.
Monitoring is §4.1 — designed, pending CCO sign-off, fast-trackable. For §2.3 residency, local
scheduled jobs beat cloud. A Sunday pre-compute so Sarah's Monday is ready — prepare-only, never
auto-act. And the hardening: query observability — every query and response logged and scanned for
non-compliant language, not just the artifacts; token and spend budgets per RM and per skill; and
sandboxed, least-privilege execution. And the AWS path — and this is Caylent's stack — our local MCP and
guards map one-to-one onto AgentCore Gateway, Runtime, Observability, and Bedrock Guardrails; Guardrails
is defense-in-depth, our deterministic guards stay the chokepoint. Ninety days: pilot both tracks, CCO
sign-off, a governed store and a funded API tier."
-->

---

<!-- _class: close -->

<div class="topbar"></div>

<div class="logo-strip">
  <span class="lockup">
    <img class="logo-caylent" src="images/logos/caylent-icon.png" alt="Caylent">
    <span class="wm-caylent">Caylent</span>
  </span>
  <span class="logo-x">×</span>
  <span class="lockup">
    <img class="logo-centerline" src="images/logos/centerline-dark.svg" alt="">
    <span class="wm-centerline">Centerline&nbsp;Bank</span>
  </span>
</div>

# Built. Trustworthy. Adopted.

<div class="tagline">Two solutions, run live — compliant by construction, geared for production.</div>

<div class="braid">
<b>A</b> — kept Tom's instinct; fixed the violations.<br/>
<b>B</b> — the AI organizes the facts; the RM keeps the judgment.<br/>
<b>C</b> — adoption is the real risk; a portfolio, each tool earning its RM.
</div>

<div class="qa">Questions?</div>

<div class="sig">Franck Benichou · <a href="https://www.linkedin.com/in/franckbenichoudata">linkedin.com/in/franckbenichoudata</a> · <a href="https://github.com/benichou/centerline-claude-pilot">github.com/benichou/centerline-claude-pilot</a></div>

<!--
NOTES (~18s): "The whole story in three words. Built — I ran it live. Trustworthy — compliant by
construction, measured, traceable. Adopted — designed per RM. A, kept the instinct; B, the RM keeps
the judgment; C, a portfolio. Happy to take questions — on the demos, the compliance, the eval, or
how this scales to the bank's real data."
-->
