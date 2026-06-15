# Panel prep & Q&A: Centerline Claude Pilot

> Your cockpit card for the hour. Per slide: **Land** (the one thing to say) + **Q&A / gotchas** (likely
> probes with crisp answers). Pairs with the deck's speaker notes and `panel-talking-points.md`.
> Golden rules: **pair from minute one · narrate the why · be honest about the 20% · let it be a conversation.**

---

## Opening posture (before slide 1)
- Set the frame in one breath: *"I built this, two solutions, run live, compliance baked in. I'll narrate
  as I go, and please jump in."*
- Two honesty flags up front (cover): **Centerline is fictional, the data synthetic**; every number is
  **as-of the 2025-05-31 data close**, verifiable against the source.
- Timebox out loud: *"~45 minutes, lots of room for questions."*

## Cross-cutting gotchas (keep these loaded, they can come at any point)
- **"You used Claude Code / Cowork, not Claude for Work, does that count?"** → The brief explicitly
  sanctions any agentic tool. Cowork *is* the no-terminal RM surface, and it runs the same plugin + MCP;
  in production it's an admin-provisioned plugin + a hosted connector. Surface isn't the point; the
  architecture ports 1:1.
- **"Does the model ever make a credit decision / do the math?"** → Never. The math is deterministic MCP
  tools; the credit judgment is either a human's words transcribed (B3/B4) or absent. §4.2 holds *because
  the enforcement is in code*, regardless of what the model says.
- **"How do the guardrails survive someone reading a raw CSV in Cowork?"** → §2.1/§5/guarantor live in the
  MCP server + core, the cross-surface chokepoint; the *access path* is the tool. The production answer is
  a governed data store, not loose files. (Honest: in the pilot, a raw file read would bypass the strip,
  that's why prod = governed store.)
- **"Isn't this a lot for 90 days?"** → 90 days delivers the *pilot* (two tracks, three RMs) + CCO sign-off
  on monitoring + the path to a governed store and funded API tier, not a finished bank-wide rollout.
- **"What breaks at scale (50 borrowers, not 5)?"** → Nothing in the compute (deterministic, per-borrower).
  The real work is connector auth, the governed data store, and alert-fatigue tuning so "flag ≠ action"
  doesn't become "flag → ignored."
- **"What would you do differently in production?"** → Hosted connector over local files; a larger labeled
  eval set with real RM edit-rates; OTel→Datadog for §4.1 monitoring evidence; lifecycle/industry-aware
  signal sets (construction vs operating).
- **"Can anything scan the model's free-form chat for compliance?"** → Honest: no tool scans free chat on
  *any* surface, hooks/tools only see tool I/O. So §4.2 = model behavior + **artifact screening** (which
  *is* enforced via `screen_and_finalize`) + the agent-eval §4.2 scanner on its narration + human review.

---

## Per-slide

### 1 · Cover
- **Land:** built, run live, compliant; fictional bank + synthetic data; numbers as-of 2025-05-31.
- **Q&A:** *"Why June 2026 on the cover but 2025 data?"* → The cover is today; the scenario is pinned to the
  data's as-of date so every figure is verifiable.

### 2 · Agenda
- **Land:** the hour's shape; two live demos; conversation welcome.
- *(no real gotchas)*

### 3 · About me
- **Land:** Senior AI Engineer at Carta; hybrid DS/consulting; builds GenAI + doc-intelligence daily; the
  FDE role is the job I already do, plus judgement + client-facing skill.
- **Q&A:** *"Why Caylent / why leave what you do?"* → I want front-line commercial impact as an embedded
  engineer, discovery to production, which is exactly the FDE role. *"Conflict with Carta?"* → This is a
  personal build on synthetic data, my own time.

### 4 · The situation
- **Land:** 3 RMs, $350M, 30–40% time on docs; nothing deployed; the CCO's early-warning priority is my mandate.
- **Q&A:** *"Are these numbers real?"* → From the assignment brief/data. *"Why is nothing deployed?"* →
  Licenses bought, no compliant path yet, that's the gap I'm closing.

### 5 · Meet the three RMs
- **Land:** adoption is the real risk; three different relationships with AI; design for each.
- **Q&A:** *"Did you invent the personas?"* → No, straight from `rm_personas` in the data (Sarah's trust
  scar, Tom's shadow build, Marcus's 71 memos are all in the file).

### 6 · The catalyst (Tom)
- **Land:** right instinct, wrong tools; starting point, not blueprint.
- **Q&A:** *"What exactly are the two violations?"* → Confidential client data on a personal (unapproved)
  account, §1/§2, plus the memo brushes §4.2 and the portfolio summary brushes §4.1. *"Is Tom in
  trouble?"* → Frame it as §6 amnesty, make him the co-builder, not the cautionary tale.

### 7 · Compliance is the architecture
- **Land:** §4 decided the design; judgment originates with the RM; enforced in code.
- **Q&A:** *"Isn't §4.2 impossible if the tool is useful?"* → No, the AI organizes/cites **facts**; the RM
  owns the **judgment**. You'll see that line drawn live in A3, B3, B4. *"'Enforced in code', how?"* →
  §2.1 strip + guarantor refusal are MCP tools; §4.2 output-screening is `screen_and_finalize`; both are
  deterministic and run server-side on every call.

### 8 · The signal's already there
- **Land:** the record can't be trusted (mis-dated logs · email-only decisions · lagging status); job =
  organize facts, make the record trustworthy, RM judges.
- **Q&A:** *"If the signal's there, why didn't the RMs act?"* → It's buried in free-text and split across
  systems, and Tom's own summary flagged Crestwood and he still lost momentum. Surfacing ≠ acting.

### 9 · How I built it
- **Land:** simplest-first (Anthropic guidance) + composable skills + MCP + server-side guards + Code→Cowork;
  one prompt, multi-tool pipeline.
- **Q&A:** *"Why skills, not one big agent/prompt?"* → Composability and clean selection; small, testable
  capabilities. *"What's the rule for when to add a step?"* → Only where a **human judgment** belongs (the
  memo, §4.2) or a **governance gate** belongs (monitoring, §4.1), not for cleverness.

### 10 · Architecture in one picture
- **Land:** AI organizes; people keep the judgment; one compliance chokepoint; one plugin, both surfaces;
  continuously evaluated.
- **Q&A:** *"Where's the data residency story?"* → Local MCP / governed store; cloud routines run a clone, so
  for §2.3 we prefer local. *"Is the MCP server the only chokepoint?"* → It's the cross-surface one; hooks
  are a Code-only belt; prod adds the governed store.

### 11 · Fix Tom's flagged workflow (the table)
- **Land:** single-prompt is right for the 3 drafting tasks; the memo and monitoring need re-architecting,
  for compliance, not cleverness. Deliverable A rebuilds the weekly summary.
- **Q&A:** *"Why is one prompt fine for the letter but not the memo?"* → The letter is content-drafting; the
  memo embeds a **credit assessment** the AI may not author (§4.2). *"§1/§2/§5?"* → approved-tools / data-
  handling / prohibited-use, the personal-ChatGPT violation common to all five.

### 12 · A1, watchlist (CCO)
- **Land:** ranks by risk×neglect, every line cited; ranks, doesn't judge (§4.2); RM-private.
- **Q&A:** *"Is the ranking a credit rating?"* → No, a facts-derived order (breach → signal count → days
  since contact), explicitly not a rating. *"How's risk×neglect computed?"* → Deterministic composition of
  the covenant/deterioration/engagement tools. *"Could it miss someone?"* → It only surfaces what the data
  shows; and a flag isn't an action, deployment must make the next step frictionless.

### 13 · A2, covenant compliance (Sarah)
- **Land:** DSCR 1.03 vs 1.20 breach, revolver past cap; status field lagged the slide; math in code.
- **Q&A:** *"Why trust your recompute over the bank's status field?"* → The recompute is deterministic from
  the financials and agrees with the bank's own loan-performance; the status field is self-reported and
  lagging. *"What if the model mis-reads a number?"* → It doesn't compute, the tool does, in code.

### 14 · A3 ★, engagement coverage (Sarah)
- **Land:** 78-day substantive-silence gap; naive log undercounts by 45; a risk no field flags; RM-private.
- **Q&A:** *"How do you define 'substantive'?"* → Two-way contact; a one-way notice, a missed call, or an
  internal note don't count. *"Isn't this surveilling RMs?"* → It's RM-private and dismissible, Sarah's
  fear *is* the design; she can annotate or dismiss (e.g., off-system contact). *"Off-system contact?"* →
  Honest caveat: not captured, the log has to be complete.

### 15 · Track B intro
- **Land:** the creative claim = close-the-loop + reconciliation + retention; the memo/intake/email are the
  compliant cleanup, said out loud.
- **Q&A:** *"Isn't covenant-package tracking on the brief's avoid-list?"* → Yes, that's exactly why I call
  it the cleanup, not the claim. The claim is the thing nobody asked for: did the bank keep its own commitments.

### 16 · B1, retention (Tom · Crestwood)
- **Land:** the one you lose by being slow, not by credit risk; facts + "engage," never a rate.
- **Q&A:** *"Why won't it recommend a rate?"* → §4.2, pricing is the committee's call; it surfaces the
  competitor's 4.90% as a fact and says "engage." *"Is the 4.90% real?"* → From the email thread / data.

### 17 · B2 ★, document intelligence (Sarah)
- **Land:** §2.1 guarantor refusal on intake; certified 1.23/3.76 vs recomputed 1.03/4.50; $2M add-back gap;
  every figure cited to doc+field+tool; footer honestly Partial.
- **Q&A:** *"Is the package real?"* → Synthetic and clearly labeled, it encodes real directions (the
  self-reported breach, the add-back gap); the *capability* is real. *"What if extraction is wrong?"* →
  Extraction is the one model step, so we recompute deterministically and cross-check the bank's own data,
  a bad extract shows up as a mismatch, not a silent error. *"Is flagging the $2M add-backs a credit
  judgment?"* → No, it surfaces the gap and its components; whether they're adequately supported is the
  RM's call (§4.2). *"Why refuse the guarantor doc?"* → §2.1, personal financials; refused on intake,
  never sent to a model, enforced in code.

### 18 · B3 ★, reconciliation (Tom · Arcadia)
- **Land:** mis-dated CRM row poisons recency; Chen's "don't waive 75%" ruling surfaced verbatim + attributed;
  propose-only CRM entry. The §4.2 scribe-not-author moment.
- **Q&A:** *"Is the AI making the credit decision?"* → No, it transcribes the credit officer's decision into
  the file, verbatim and attributed; it never makes one. *"How do you know Apr-9 is mis-dated?"* → The email
  timestamps are the reliable clock; the timeline tool merges them and the row sorts before the real thread.
  *"You said it found a missing Draw #12?"* → Yes, unscripted, by cross-referencing loan-performance vs the
  log; an honest real find, not designed.

### 19 · B4, annual memo (Marcus)
- **Land:** assembles + cites, then **stops** and the RM writes the assessment; §4.2 made literal; wins the skeptic.
- **Q&A:** *"Does the AI write the assessment?"* → No, it pauses and the RM types it in their own words,
  attributed; the AI drafts around it. *"What if the RM rubber-stamps?"* → The assessment field must be
  RM-authored and non-empty; the design hands them the pen, adoption is still theirs to own. *"Why does
  this win Marcus?"* → It removes ~71 memos/yr of assembly without changing how he thinks.

### 20 · How the CCO can trust it (eval, closed-loop)
- **Land:** four layers + a CI gate; reliability is a reported number, both tracks; AI proposes, human disposes.
- **Q&A:** *"Layer 1 vs Layer 3?"* → L1 tests the tool **code** (LLM never called); L3 tests the **model's**
  decisions, don't let one stand in for the other. *"95/95, grading your own homework?"* → Honest: a small,
  self-authored set, but source-grounded with negative/adversarial cases and disclosed; production = a
  larger labeled set + real RM edit-rates. *"Is the improvement loop autonomous?"* → No, advisory only; it
  can't touch guards/core/eval keys; a human applies.

### 21 · Governance, live (the 2 display prompts)
- **Land:** show the scorecard + the proposals live; the loop caught a real §4.2 issue, left unapplied.
- **Q&A:** *"Can the loop change the guardrails?"* → No write access, read-only via `get_latest_report`.
  *"Who owns this in production?"* → A named skill-library maintainer + Compliance as the CCO's delegate;
  same propose/dispose split.

### 22 · Honest 80/20
- **Land:** works (grounded, compliant, deterministic, creative use cases on real data); hard 20% (flag≠action, logging-
  gated, A blind to healthy/construction, doc-intel synthetic).
- **Q&A:** *"Biggest weakness?"* → Flag ≠ action + value gated by logging discipline (Marcus). *"Does the
  synthetic doc-intel undercut the claim?"* → No, only doc-intel is synthetic; both creative use cases run on
  the real files.

### 23 · Adoption
- **Land:** no single tool wins all three, a portfolio; start with Sarah.
- **Q&A:** *"Which RM first?"* → Sarah, natural teacher; if she adopts, she trains the floor. *"What if
  Marcus refuses?"* → The memo is the lowest-behavior-change wedge; honestly he's the hardest, and the
  benched memo is his best fit, say it.

### 24 · Production & rollout
- **Land:** Cowork surface · §4.1 fast-track · §2.3 residency · scheduled-jobs · the hardening (query observability,
  token/spend budgets, sandboxing); 90 days → pilot → sign-off → governed store.
- **Hardening (the new card, be ready to expand):**
  - **Query observability:** every query *and* response logged and scanned for non-compliant (§4.2) language, not
    just the artifacts (closes the "nothing scans the free-form chat reply" gap), giving Compliance a queryable
    audit trail of what was asked and answered. OTel → Datadog.
  - **Token/budget monitoring:** per-RM and per-skill token + spend dashboards with budget caps and alerts, cost
    control and an abuse/runaway-loop signal, feeding the §4.1 monitoring evidence.
  - **Sandboxing & least-privilege:** skills/tools run sandboxed; connector scopes read-only by default, defense
    *beyond* the server-side guard chokepoint, so a compromised skill can't reach or write what it shouldn't.
- **Q&A:**
  - *"What breaks at scale (50 borrowers, not 5)?"* → Nothing in the compute (deterministic, per-borrower). The real
    work is connector auth, the governed data store, and **alert-fatigue tuning** so "flag ≠ action" doesn't become
    "flag → ignored."
  - *"What would you do differently in production?"* → Hosted connector over local files; a larger labeled eval set
    with real RM edit-rates; **OTel → Datadog for §4.1 monitoring + query observability**; **token/spend budgets**;
    **sandboxed, least-privilege execution**; lifecycle/industry-aware signal sets (construction vs operating).
  - *"Is Cowork in the bank's approved scope?"* → A rollout-recommendation, not a blocker, confirm with
    IT-Security / §2.3 residency. *"Cost?"* → Funded API tier; nightly eval on Sonnet (cheap), demo on Opus; token
    budgets keep it predictable.
- **AWS production path (Caylent's stack, be ready to go deep; current as of mid-2026):** the pilot is local MCP +
  Claude Code/Cowork; it maps **1:1** onto AWS-managed services, say "maps onto," not "what we built."
  - **Bedrock AgentCore Gateway**, turns our retrieval into a managed MCP server; least-privilege execution roles +
    **Gateway interceptors** (per-tool access control, identity propagation) + **AgentCore Identity OBO** (agent acts
    only in the authenticated user's scope) = the hosted version of our least-privilege-connectors card.
  - **AgentCore Runtime**, serverless, **per-invocation microVM isolation**, 8-hr sessions; **Claude Agent SDK**
    deploys our skills "in 3 lines" = the sandboxing card, concrete.
  - **AgentCore Observability**, OTel-native, CloudWatch dashboards (token usage, latency, errors, sessions) +
    interceptor logs = the query-observability/cost card.
  - **Bedrock Guardrails** (`ApplyGuardrail`), PII/sensitive-info redaction (custom RegEx for §2.1 fields),
    **denied-topics** to block credit-advice language (§4.2), contextual grounding, **cross-account** org-wide
    enforcement w/ audit logs (GA Apr 2026).
  - **Eval pattern**, Anthropic's canonical **Planner→Generator→Evaluator** (Apr 2026); the independent evaluator
    eliminates self-grade inflation = exactly our Layer-1 + independent Layer-3 agent-eval design.
  - **THE honesty point (lead with it if asked):** Bedrock Guardrails is **probabilistic** and **does not scan
    `tool_use` outputs** → our **deterministic, server-side guards remain the primary chokepoint**; Guardrails is
    belt-and-suspenders, not a replacement. Same logic as "enforcement in code, not a disclaimer."
  - **Billing note (if cost comes up):** the **June 15 2026** change moves Agent SDK / `claude -p` / GitHub Actions on
    *subscriptions* to a separate monthly credit, but **API-key production bills per token as before** (what our
    "funded API tier" assumes; our nightly eval cron already runs on the API key).

### 25 · Close
- **Land:** Built. Trustworthy. Adopted., A/B/C. Invite questions.
- *(transition to Q&A)*

---

## The three hardest questions (rehearse these cold)
1. **"What's genuinely novel here vs. what the brief told you to avoid?"** → The avoid-list (memo, covenant
   tracking, overdue emails) is the *compliant cleanup*, I say so out loud. The creative claim is
   **close-the-loop** (did the bank keep its own commitments?) + **cross-source reconciliation** + **retention
   radar**, combining sources no one reconciles, surfacing the bank's own dropped follow-through (B3 found a
   missing draw unprompted).
2. **"How is this actually compliant and not just disclaimered?"** → Enforcement is in **code**, not prompts:
   §2.1 strip + guarantor refusal are MCP tools; §4.2 screening is a deterministic tool every output routes
   through; the credit judgment is transcribed (B3) or RM-authored (B4), never generated. The eval even scans
   the model's own narration for §4.2.
3. **"Is this real or a demo trick?"** → It runs live in Cowork on the assignment data; the math is
   deterministic and cited; 95/95 golden + a live agent-eval; the only synthetic piece is the doc-intel
   package, clearly labeled, and both creative use cases run on the real files.
