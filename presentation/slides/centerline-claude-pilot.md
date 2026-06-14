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
<strong>Senior Forward Deployed Engineer</strong> candidate
</div>

<div class="speaker">
<a href="https://www.linkedin.com/in/franckbenichoudata">Franck Benichou</a> · June 2026
</div>

<!--
NOTES (≈30s): "This is the Claude pilot for Centerline's Commercial Banking division —
what I built, run live, with compliance baked in. I'll narrate every decision as we go.
Two honesty notes up front: Centerline is a fictional bank and the data is synthetic; and
the cover is today, but the scenario is pinned to the data — the 2025-05-31 close — so every
number you'll see is verifiable against the source."
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
<li><span class="n">1</span><b>It's the work I already do.</b> AWS + Anthropic is my current stack — I build with the Anthropic APIs and Claude Code every day at Carta, in the document-intelligence team.</li>
<li><span class="n">2</span><b>Why I'm excited.</b> I'm an AI builder who wants direct commercial impact on the front lines — prototyping and taking things into production.</li>
<li><span class="n">3</span><b>Why I'm a fit.</b> Beyond building, my unconventional, hybrid background brings judgement and client-facing strength — not just code.</li>
</ul>
</div>

</div>

<!--
NOTES (≈45s): "Quickly, who I am — a Senior AI Engineer at Carta in Toronto, but the background is
hybrid: data science and consulting across Intact, EY, Deloitte, now Carta. Day to day I build on
AWS and Anthropic — the Anthropic APIs and Claude Code — in our document-intelligence team, the
same shape of problem Centerline has. Why this role: I'm an AI builder who wants direct commercial
impact on the front lines — prototyping and shipping into production. And my fit isn't only that I
build; it's that the unconventional, hybrid background brings judgement and client-facing skill on
top of the engineering. The best proof is the next hour — I didn't write slides about what I'd
build; I built it. Let's get into it."
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

<div class="callout">The CCO, <strong>Rachel Torres</strong>, has one stated priority: an <strong>early-warning</strong> capability for contact gaps and financial deterioration — RM-private, compliance-gated. <em>That's my mandate for the next 90 days.</em></div>

<!--
NOTES (~50s): "Three RMs, a combined $350M book, and they lose a third of their week to
documentation, covenant tracking, and call prep — not to clients. The bank bought Claude for
Work and deployed nothing. And the CCO, Rachel Torres, has a specific ask: early-warning on
contact gaps and financial deterioration, RM-private and compliance-gated. That's the mandate
I'm here to land — and everything I show maps back to it."
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

<!--
NOTES (~55s): "Three RMs — and the honest risk isn't the tech, it's whether they'll use it.
Sarah's the linchpin: a natural teacher, but she was burned by an AI pilot that gave wrong
covenant info, so trust is everything — if she adopts, she trains the floor. Tom's the builder —
he's the one who stood up the shadow ChatGPT workflows; he wants to co-design, not be policed.
Marcus is the skeptic — 22 years, mentors four juniors, writes about 71 annual memos a year, and
logs sparsely because he trusts his own memory. Win Marcus and the rollout tips. You'll meet all
three again in the demos — every prompt is one of their real workflows."
-->

---

<!-- _class: catalyst -->

# The catalyst — one RM didn't wait

<div class="two-col">

<div class="card flag">
<span class="tag red">IT audit finding</span>
<div class="hd" style="margin-top:10px">Tom built 5 AI workflows on personal ChatGPT</div>
<p>Client financials and names pasted into a personal account — <strong>two compliance violations.</strong> Draw-response letters · relationship memos · client emails · call-prep briefs · a weekly portfolio summary.</p>
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
NOTES (~50s): "One RM — Tom — didn't wait. He built five AI workflows on a personal ChatGPT
account with client financials and names pasted in. The IT audit caught it: two violations.
The honest read isn't 'Tom's the problem' — it's that Tom was right that this helps, and used
the wrong tools. His workflows are our starting point, not our blueprint. So the first question
isn't technical — it's: what do the right tools, done compliantly, look like?"
-->

---

<!-- _class: compliance -->

# Compliance isn't a wrapper — it's the architecture

<div class="lede">Section 4 is trickier than it looks. Five constraints decided every design choice that follows.</div>

<div class="policy">
  <div class="pol"><div class="sec">§4.2</div><div class="d">No creditworthiness language — even implicitly. A disclaimer does <strong>not</strong> count.</div></div>
  <div class="pol"><div class="sec">§2.1</div><div class="d">Credit grade / watchlist can't even be <strong>inputs</strong> to the AI.</div></div>
  <div class="pol"><div class="sec">§5</div><div class="d">No AI on <strong>Special-Assets</strong> or litigation credits.</div></div>
  <div class="pol"><div class="sec">§4.1</div><div class="d">Automated monitoring needs <strong>CCO approval</strong> to launch.</div></div>
  <div class="pol"><div class="sec">§4.3</div><div class="d"><strong>Human review</strong> before anything is client-facing or filed.</div></div>
</div>

<div class="callout">The credit <strong>judgment must originate with the RM.</strong> Claude organizes facts and flags gaps — it never characterizes credit. And we enforce that <strong>in code, not in a prompt.</strong></div>

<!--
NOTES (~55s): "Section 4 is trickier than it looks. §4.2 — no creditworthiness language, even
implicitly, and 'I added a disclaimer' explicitly does not count. §2.1 — credit grade and
watchlist can't even be inputs to the model. §5 — no AI at all on Special-Assets or litigation.
§4.1 — monitoring needs CCO sign-off before launch. §4.3 — human review before anything ships.
The throughline: the credit judgment originates with the RM; the AI organizes facts. And you'll
see this enforced in code — in the tools — not bolted on as a prompt instruction."
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
NOTES (~55s): "Eight files — three CSVs, four email threads, one memo — current through end of
May 2025. The signal is already in the data; the problem is the record can't be trusted: logs
are mis-dated, the most consequential credit decisions live only in email, and the covenant
status field lags the real trend by months. Three finds fall out — Meridian's action plan was
never executed; Crestwood is an attrition risk while looking perfectly healthy; and across the
book, engagement diverges from distress. So our job is to organize scattered facts and make the
record trustworthy — and leave the judgment with the RM. That's the spine running through both
demos."
-->
