# Deliverable A — What changed & why (rebuild of Tom's wf5)

> **The assignment:** take a workflow Tom DeLuca built in personal ChatGPT (with compliance
> violations), rebuild it Claude-native so it does the same job, **fix the violations**, and show
> *what changed and why* — including the architecture judgment: was his "single prompt with the data
> pasted in" the right design, or should it be broken into steps?
>
> **The workflow:** **wf5 — "Portfolio Summary for Myself (Weekly)."** Tom's own words: *"Every Monday
> morning I do this to get my head straight for the week. Takes me about 15 minutes."* It's the one
> the IT audit flagged (FLAG #2), and it's the workflow that maps directly onto the CCO's stated
> early-warning priority (§7) — so it's the highest-value, highest-scrutiny one to get right.
>
> All sources cited inline. Facts are grounded in `reference/shadow-workflows/wf5-portfolio-summary.md`,
> the compliance policy (`reference/compliance-policy/`), and the **real outputs** captured from the
> built system (§4 below).

---

## 1. BEFORE — Tom's wf5, verbatim

From `reference/shadow-workflows/wf5-portfolio-summary.md`:

```
Here is a summary of my commercial loan portfolio as of [date]:
[paste table with: borrower, DSCR, covenant status, last contact date, next action needed]

Summarize:
1. Which borrowers need attention this week and why
2. Any patterns or trends I should be aware of across the portfolio
3. My top 3 priorities for the week

Be concise. I don't need explanations — just the most important things.
```

**Architecture:** a **single-turn prompt** — Tom hand-assembles a portfolio table across *multiple*
accounts in Excel, pastes it into his **personal ChatGPT Plus account**, and asks the model to tell
him who needs attention, what the trends are, and what his priorities should be.

**Self-reported value (real, and worth honoring):** *"Output quality is honestly impressive. Last
week it flagged that I hadn't contacted Crestwood in over 6 weeks and there was a pending renewal
item. I had completely lost track of it."* — wf5 notes. The need is genuine; the implementation is
the problem.

---

## 2. The violations (what exactly is wrong, and which clause)

| # | Violation | Where it lives in wf5 | Policy clause |
|---|---|---|---|
| **V1** | **Multi-account aggregation in a personal account.** Borrower names + loan balances + DSCR across *multiple* accounts, compiled into one personal-ChatGPT prompt. The audit's FLAG #2 calls this a "higher-risk data handling pattern than single-account queries." | The pasted table; personal ChatGPT Plus (`00-setup.md`) | **§2.x data handling** (`02-data-handling.md`) + **§6** personal-account use of bank data is prohibited (`06-existing-unauthorized-usage.md`) |
| **V2** | **Latent restricted-input exposure.** The table is hand-built, so nothing *stops* an RM from pasting the internal `credit_grade` (B+/BB-/A-) or watchlist/Special-Assets language alongside it. wf5 as written doesn't include the grade, but the manual paste makes §2.1 a matter of RM discipline, not enforcement. | "[paste table…]" — uncontrolled input | **§2.1** prohibited inputs (`02-data-handling.md`) |
| **V3** | **The model is asked to make the credit judgment.** "Which borrowers need attention **and why**" and "my **top 3 priorities**" ask ChatGPT to *characterize* which credits are concerning and *rank* them. That is credit-adjacent output — exactly what §4.2 reserves for the RM. The policy is explicit that this "applies to the **format** of the output, not just its content." | Prompt items 1 & 3 | **§4.2** credit-adjacent outputs (`04-restricted-use-cases.md`) |
| **V4** | **Unapproved automated monitoring.** A weekly tool that scans borrower data and emits attention-flags / deterioration signals is automated monitoring + contact-frequency monitoring — which §4.1 says needs CCO approval *before* launch (it "may constitute credit analysis under Regulation B"). | The whole workflow's purpose | **§4.1** automated monitoring (`04-restricted-use-cases.md`) |
| **V5** | **An LLM is asked to compute over structured data.** "Any patterns or **trends**" and "**top 3 priorities**" ask ChatGPT to do numeric reasoning over a pasted table — trend detection, threshold comparisons, ranking. LLMs are unreliable at tabular arithmetic (silent miscalculations, hallucinated trends, miscounted rows); on a clean-schema CSV this is the wrong tool for the job, and it directly feeds Sarah's "a pilot gave me wrong covenant numbers" scar. | Prompt items 1 & 3 (the "[paste table…]" + "trends"/"priorities") | Reliability/accuracy (not a policy clause — an *engineering* fault that also undermines §4.2's facts-must-be-trustworthy premise) |

**The subtle one is V3.** It's tempting to think the fix is "move it from ChatGPT to Claude and add
a disclaimer." The policy forecloses that directly: *"When in doubt, the RM must author the credit
assessment language themselves,"* and a disclaimer is explicitly **not** a design. The architecture
itself has to stop the model from being the thing that decides who's risky.

---

## 3. AFTER — the Claude-native rebuild, and what each step fixes

The rebuild replaces the single paste with a **four-step pipeline**. The data is retrieved through a
tool (not pasted), the *who-needs-attention* judgment is computed by **deterministic code, not the
model**, the output is screened, and the result is RM-private and gated.

```
  ┌────────────┐   ┌─────────────────────┐   ┌──────────────────┐   ┌──────────────────────┐
  │ 1 RETRIEVE │ → │ 2 DETERMINISTIC      │ → │ 3 SCREEN         │ → │ 4 PRESENT            │
  │ MCP tools  │   │   FLAGS (code, not   │   │ screen_and_      │   │ RM-private watchlist │
  │ §2.1 strip │   │   the LLM)           │   │ finalize §4.2    │   │ §4.1 "pending CCO"   │
  │ §5 gate    │   │ covenant/trend/      │   │ + reliability    │   │ + §4.3 review tag    │
  │ server-side│   │ engagement/triage    │   │   footer         │   │                      │
  └────────────┘   └─────────────────────┘   └──────────────────┘   └──────────────────────┘
```

**Step 1 — Retrieve via the `centerline` MCP server (fixes V1, V2).**
The data is pulled through tools (`get_borrower_dossier`, `get_loan_performance`, …), never
hand-pasted. The server **strips `credit_grade` and watchlist/Special-Assets language server-side**
and **gates Special-Assets/litigation borrowers (§5)** before anything reaches the model — and it
does so on *every* surface (Claude Code via `.mcp.json`, Cowork via the desktop-config bridge). The
restricted-input risk stops being a matter of RM discipline and becomes a property of the system. The
personal-account problem disappears because this runs on bank-approved Claude for Work / Code.

**Step 2 — Deterministic flags, computed in code (fixes V3 — the important one).**
"Who needs attention" is no longer an LLM opinion. `check_covenant_compliance`,
`detect_deterioration_signals`, `measure_engagement_coverage`, and `assemble_watchlist` compute
**facts**: DSCR vs the covenant minimum and the cushion, the 17-month trend, revolver utilization vs
a threshold, days since substantive contact, and a **risk × neglect ranking**. The model orchestrates
and narrates; it does not decide who is risky. The ranking is reproducible (proven by 46 deterministic
tests) and identical run-to-run — which is also what answers Sarah's trust scar from the earlier
pilot that gave wrong covenant numbers.

**Step 3 — Screen the output (fixes V3, belt-and-suspenders).**
Every artifact is routed through `screen_and_finalize`, which scans for credit-characterizing /
predictive / recommending language and **blocks** it (§4.2), attaches a qualitative reliability footer
(Grounded / Partial / Unverified — **never a numeric %**, because a % reads as a credit-risk score),
and tags the artifact for RM review (§4.3). So even if a downstream draft drifted toward "elevated
risk," it can't leave.

**Step 4 — Present as RM-private, pending CCO (fixes V4).**
The watchlist is explicitly **RM-private and advisory** — the RM can dismiss or annotate any line, and
nothing auto-escalates. The automated-alerting piece is presented as **designed, pending CCO approval
(§4.1)** — which is the honest status, and §7 says the CCO will fast-track a well-designed
early-warning tool because it's her stated priority.

### Violation → fix traceability

| Violation | Killed by | How |
|---|---|---|
| V1 multi-account aggregation in personal account | Step 1 + surface | Approved Claude for Work/Code; data via tools, not paste |
| V2 restricted-input exposure (§2.1) | Step 1 | Server-side strip of `credit_grade` + watchlist/SA; §5 gate — enforced, not optional |
| V3 model makes the credit judgment (§4.2) | Steps 2 + 3 | Judgment is deterministic code; output screened for credit-adjacent language; RM owns the call |
| V4 unapproved monitoring (§4.1) | Step 4 | RM-private/advisory; automated alerting labeled "designed, pending CCO" |
| V5 LLM computing over structured data | Step 2 | Trends/thresholds/ranking computed in deterministic Python over the full sorted series — the model orchestrates and narrates, it does not calculate (see §4a) |

---

## 4. The architecture verdict (the question the brief actually asks)

**Was Tom's "single prompt with the data pasted in" the right architecture? No — and not for the
usual reason.** The split into steps here is required for **compliance, not cleverness.** Two of the
four steps exist *only* because of the policy:

- **The aggregation IS the compliance problem.** A single prompt that ingests the whole portfolio is
  precisely the higher-risk pattern FLAG #2 names. Retrieval has to be a separate, governed step so
  restricted fields are stripped and the surface is bank-approved — that can't happen inside one paste.
- **"Summarize who needs attention and why" is the model making a credit judgment.** §4.2 says that
  has to originate with the RM. The only way to keep the *value* of wf5 (the prioritized who-needs-me
  list) while obeying §4.2 is to make the prioritization **deterministic** — computed facts, not model
  characterization. That mandates a compute step distinct from any narration.

And there's a third reason that isn't about compliance at all — it's about **accuracy**: a single
prompt asks the LLM to compute trends and rankings over a table, which LLMs do unreliably. That alone
justifies a separate deterministic compute step (§4a below), independent of policy.

### 4a. Don't ask an LLM to compute over a CSV — the deterministic-tools point

There's a third, purely *engineering* reason wf5's architecture was wrong, independent of compliance:
**it pasted a clean-schema table and asked the model to find the trends and rank the priorities.**
That is exactly the task LLMs are unreliable at — arithmetic over tabular data, month-over-month trend
detection, counting, ranking — and Centerline already has a scar from it (Sarah's earlier pilot that
returned wrong covenant numbers). A confident-but-wrong DSCR or a hallucinated trend in an
attention-list isn't just a quality bug; it poisons the very facts §4.2 assumes are trustworthy.

**Our rebuild moves every computation into deterministic Python** (`mcp/centerline_mcp/core.py`); the
LLM's job shrinks to *pick the tool, pass the borrower name, narrate the returned facts.* Concretely:

- **Full sorted series, not a point-in-time eyeball** — `_lp_rows()` loads all 17 months and sorts by
  date (`core.py:167`); DSCR and revolver become numeric lists (`core.py:234-235`).
- **Covenant test = code arithmetic** — DSCR/leverage vs the borrower's own thresholds, cushion
  `round(dscr - dscr_min, 2)`, breach booleans (`core.py:196-208`). The model never evaluates 1.03 < 1.20.
- **DSCR trend** `dscr[-1] < dscr[0]` over N months (`core.py:238`); **revolver climb + ≥75% alert**
  (`core.py:241-244`).
- **The status-vs-trend mislabel** — *counts* the months where `covenant_status` read "Compliant" while
  DSCR fell month-over-month (`core.py:246-252`). This is precisely the structured-data labeling error
  an LLM scanning a table would miss or invent — here it's caught by a deterministic loop.
- **Thin cushion** `0 <= cushion <= 0.05` (`core.py:254-256`); **engagement gap** via real `datetime`
  arithmetic (`core.py:305-341`).
- **The watchlist ranking** — a deterministic `items.sort()` on the key tuple
  `(breach, signal_count, days_quiet)` (`core.py:365`). The ordering Tom asked ChatGPT to *produce* is
  *computed*, and it's identical run-to-run (the 46 deterministic tests prove it).

**Honest boundaries (we don't overclaim a math-free LLM).** Three touchpoints remain, by the nature of
an agentic system: (1) **tool selection is probabilistic** — mitigated because the critical math lives
in the tool, and expected-trace eval checks are the planned belt; (2) **narration could re-state a
number wrong** — mitigated by `grounding-claims-to-source`, the `screen_and_finalize` reliability
footer, and the §4.3 RM review, but not a hard guarantee; (3) **one free-text extraction is regex**
(construction pre-leasing %, `core.py:226`) — deterministic but phrasing-dependent. None of these put
arithmetic back in the model's hands; they're the residual surface we monitor and disclose.

**The honest converse — where a single prompt *is* still right.** Tom's *other* shadow workflows are
mostly content drafting (the draw-response letter, the client email, the call-prep brief). Those are
§3.1/§3.3-permitted, they don't wrap a credit judgment, and for them a single well-grounded prompt
(retrieval + review) is the correct, non-over-engineered call. We are not splitting for the sake of
it. wf5 specifically needed decomposition because **its output is a credit-relevant prioritization and
its input is a multi-account aggregation** — both of which are compliance triggers. (The relationship
memo, wf2, is the other genuine decompose-for-compliance case, handled in Track B.)

---

## 5. Captured outputs (real runs, both surfaces)

These are the actual outputs from the built system — Claude Code (native `mcp__centerline__*` tools)
and Claude Cowork (same tools, bridged in). Both agree, and both match the 46 deterministic tests.

### 5a. `assemble_watchlist` — the rebuilt wf5 (triage as of 2025-05-31)

Ranked by **covenant breach → deterioration-signal count → days since substantive contact**. This is a
facts-derived triage order, **not a credit rating.**

| # | Borrower | Lifecycle | Covenant | Signals | Days quiet | Top facts |
|---|---|---|---|---|---|---|
| 1 | Meridian Fabrication | operating | Breach | 4 | 78 | DSCR 1.45→1.03 (17 mo); revolver 38%→85% |
| 2 | BlueLine Logistics | operating | Breach | 4 | 60 | DSCR 1.58→0.95 (17 mo); revolver 42%→85% |
| 3 | Summit Retail Partners | operating | Compliant | 3 | 16 | DSCR 1.13→1.12; label lagged a 6-mo decline; only 0.02 above the 1.10 floor |
| 4 | Arcadia Property Group | construction | Construction | 2 | 52 | pre-leasing 71% vs 75% perm threshold; operating covenants not yet in effect |
| 5 | Crestwood Capital Advisors | operating | Compliant | 0 | 46 | no signals |

The engine's own notes surfaced two honest points unprompted: **Summit** is *labeled* Compliant but
carries a thin cushion and a status label that lagged a declining DSCR — exactly the mislabel the
deterioration lens exists to catch; and **Crestwood sinks to the bottom precisely because distress
monitoring is structurally blind to a clean borrower** (renewal/retention risk is a separate lens this
triage doesn't carry — see §6).

### 5b. `screen_and_finalize` — the §4.2 gate working

Input: `'This borrower is high credit risk and likely to default.'`

```
🚫 BLOCKED — did not pass the output guard.
Violations (§4.2): "high credit risk", "likely to default"  — credit-characterizing / predictive
Also flagged: no source citation detected
finalized_text: null   (nothing leaves)
```

This is the gate refusing to dress up a credit characterization. The compliant path is to restate it
as cited facts — *"DSCR declined 1.45→1.03 over 17 months (loan_performance); covenant test returns
Breach"* — and route that through RM review (§4.3), leaving the credit conclusion to the RM.

---

## 6. Honest evaluation (the 80/20)

**What it does well (the 80%):**
- **Compliance is designed in, not disclaimed.** §2.1 strip and §5 gate are server-side and
  cross-surface; the "who needs attention" judgment is deterministic, so §4.2 isn't a matter of model
  behavior; the output guard blocks credit-adjacent language; the monitoring is honestly labeled
  pending-CCO. Each violation maps to a step that removes it (§3 table).
- **It reproduces — and exceeds — wf5's real value.** It catches Tom's 6-week Crestwood gap *and* adds
  signals wf5 never had: the 78-day Meridian silence *during a breach*, the Summit status-label lag,
  and the construction-aware Arcadia lens. The math is reproducible (46 tests), which is the direct
  answer to Sarah's "a tool gave me wrong covenant numbers" scar.
- **It's a portfolio of small composable skills**, so the same retrieval + grounding + screening
  foundation powers Track B too.

**Where it falls short (the hard 20% — say it out loud to the panel):**
- **A flag is not an action — and we have proof.** Tom's *own* wf5 flagged the Crestwood gap, and he
  **still lost the relationship to inaction.** Detection is necessary but not sufficient; the
  deployment has to make the next action frictionless and avoid alert fatigue, or we've rebuilt the
  same dead-end more compliantly. This is the single most important honest point in Deliverable A.
- **The early-warning is structurally blind to a healthy borrower.** Crestwood ranks *last* (0
  signals) — yet Crestwood is the borrower quietly shopping his renewal elsewhere. Distress monitoring
  cannot see retention risk by construction. **That blind spot is exactly what Deliverable B (the
  retention radar) exists to cover** — which is why A and B belong together.
- **Output quality is bounded by data quality.** Self-reported, batch-arriving financials and a
  thin/sometimes back-dated activity log mean the flags are only as good as the inputs; the reliability
  footer surfaces this (evidence quality, not ground truth) but can't fix it.
- **§4.1 means it isn't launch-ready by itself.** Honestly, the automated-monitoring version needs the
  CCO sign-off before it can run unattended; what we demo is the RM-private, on-demand version.

---

## 7. One-line summary for the panel

> *"wf5 was a good instinct built the wrong way: it pasted the whole portfolio into a personal account
> and asked the model to decide who was risky. We kept the instinct, moved the data behind a tool that
> strips what policy forbids, made the 'who needs attention' call **deterministic code instead of a
> model opinion**, screened the output, and kept it RM-private pending CCO. Same Monday-morning value —
> now it's compliant, reproducible, and it even sees risks Tom's version couldn't. And we'll be honest:
> a flag isn't an action, and it's blind to the healthy client who's leaving — which is exactly what
> our second solution catches."*
