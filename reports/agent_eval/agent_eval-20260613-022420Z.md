# Agent-behavior eval (the LLM-driven decisions)

_Run 2026-06-13 02:24 UTC · model: claude-sonnet-4-6 · 3 run(s)/prompt · via `evals/agent_eval.py`._

Grades the **model's** decisions with deterministic code: tool selection, §4.2 on the agent's own narration, and fact faithfulness. Complements `runner.py` (which unit-tests the tool logic).

| Prompt | Runs passed | Tool selection | §4.2 on output | Facts |
|---|---|---|---|---|
| **A1** | 2/3 | 3/3 | 2/3 | 3/3 |
| **A2** | 3/3 | 3/3 | 3/3 | 3/3 |
| **A3** | 3/3 | 3/3 | 3/3 | 3/3 |

## Per-run detail (with the model's captured analysis)

### A1
- run 1: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 1 — model's analysis</summary>

  > Here is your portfolio triage as of **2025-05-31** (the most recent data in the system), ranked by breach → signal count → engagement gap. Facts only — the credit judgment is yours.
  > 
  > ---
  > 
  > ## Portfolio Triage — Week of 2026-06-13
  > 
  > *Data as-of: 2025-05-31 · RM-private/advisory · Automated alerting designed, pending CCO approval (§4.1)*
  > 
  > ---
  > 
  > ### 1. Meridian Fabrication LLC — Covenant Breach · 4 signals · 78-day contact gap
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | **Breach** | structured/meridian |
  > | DSCR trend | 1.45 → 1.03 over 17 months | loan_performance |
  > | Revolver utilization trend | 38% → 85% | loan_performance |
  > | Revolver alert threshold | 85% ≥ 75% alert level | loan_performance |
  > | Days since substantive contact | **78 days** | activity_log |
  > 
  > ---
  > 
  > ### 2. BlueLine Logistics LLC — Covenant Breach · 4 signals · 60-day contact gap
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | **Breach** | structured/blueline |
  > | DSCR trend | 1.58 → 0.95 over 17 months | loan_performance |
  > | Revolver utilization trend | 42% → 85% | loan_performance |
  > | Revolver alert threshold | 85% ≥ 75% alert level | loan_performance |
  > | Days since substantive contact | **60 days** | activity_log |
  > 
  > ---
  > 
  > ### 3. Summit Retail Partners — Compliant · 3 signals · 16-day contact gap
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | Compliant | structured/summit |
  > | DSCR trend | 1.13 → 1.12 over 17 months | loan_performance |
  > | Cushion above 1.10 floor | **0.02** | loan_performance |
  > | Status-vs-trend flag | "Compliant" label was carried for 6 months of DSCR decline | detect_deterioration |
  > | Days since substantive contact | 16 days | activity_log |
  > 
  > ---
  > 
  > ### 4. Arcadia Property Group — Construction phase · 2 signals · 52-day contact gap
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Lifecycle | Construction (operating covenants not yet in effect) | structured/arcadia |
  > | Pre-leasing | **71%** vs 75% perm-conversion threshold | structured/arcadia |
  > | Gap to conversion threshold | 4 pp | structured/arcadia |
  > | Items to monitor | % complete, schedule slip, interest-reserve runway | detect_deterioration |
  > | Days since substantive contact | **52 days** | activity_log |
  > 
  > ---
  > 
  > ### 5. Crestwood Capital Advisors — Compliant · 0 signals · 46-day contact gap
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | Compliant | structured/crestwood |
  > | Deterioration signals | 0 | detect_deterioration |
  > | Days since substantive contact | 46 days | activity_log |
  > 
  > > **Note:** Distress monitoring is structurally blind to a healthy borrower with 0 signals. Renewal/retention risk for Crestwood requires a separate lens.
  > 
  > ---
  > 
  > **Reliability:** Facts drawn directly from deterministic MCP tool output (`assemble_watchlist`). All figures are server-computed from `data/structured/` and `data/emails/`. No model-estimated figures. Data is as of **2025-05-31** — any changes since that date are not reflected.

  </details>
- run 2: ❌ FAIL · tools=['Skill', 'ToolSearch', 'assemble_watchlist'] · §4.2 hits=['creditworthiness'] · missing facts=[]

  <details><summary>run 2 — model's analysis</summary>

  > Here is the portfolio triage as of **2025-05-31** (latest available data). Ranked by: covenant breach → signal count → days since substantive contact. This is RM-private and advisory; automated alerting is designed, pending CCO approval (§4.1).
  > 
  > ---
  > 
  > ## Portfolio Triage — 2025-05-31
  > 
  > ---
  > 
  > ### 1. Meridian Fabrication LLC
  > **Covenant Breach · 4 signals · 78 days since substantive contact**
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | **Breach** | structured data: covenant_status |
  > | DSCR (latest) | **1.03** | performance data, 2025-05-31 |
  > | DSCR trend | 1.45 → 1.03 over 17 months | performance history |
  > | Revolver utilization | **85%** (alert threshold: 75%) | performance data |
  > | Revolver trend | 38% → 85% over 17 months | performance history |
  > | Days since substantive contact | **78** | CRM activity log |
  > 
  > **Why it leads:** Only borrower combining a breach, 4 signals, and the longest contact gap in the portfolio.
  > 
  > ---
  > 
  > ### 2. BlueLine Logistics LLC
  > **Covenant Breach · 4 signals · 60 days since substantive contact**
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | **Breach** | structured data: covenant_status |
  > | DSCR (latest) | **0.95** | performance data, 2025-05-31 |
  > | DSCR trend | 1.58 → 0.95 over 17 months | performance history |
  > | Revolver utilization | **85%** (alert threshold: 75%) | performance data |
  > | Revolver trend | 42% → 85% over 17 months | performance history |
  > | Days since substantive contact | **60** | CRM activity log |
  > 
  > **Notable:** DSCR has crossed below 1.0 (sub-1.0 means cash flow does not cover debt service at this reading). Same signal count as Meridian; ranks second on the contact-gap tiebreaker (60 vs 78 days).
  > 
  > ---
  > 
  > ### 3. Summit Retail Partners
  > **Compliant · 3 signals · 16 days since substantive contact**
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | Compliant | structured data: covenant_status |
  > | DSCR (latest) | **1.12** (floor: 1.10) | performance data, 2025-05-31 |
  > | Cushion above floor | **0.02** | computed |
  > | DSCR trend | 1.13 → 1.12 over 17 months | performance history |
  > | Status-vs-trend mislabel | `Compliant` label persisted during 6 months of DSCR decline | performance history |
  > | Days since substantive contact | **16** | CRM activity log |
  > 
  > **Notable:** The 0.02 cushion above the 1.10 floor is the thinnest in the operating portfolio. The label-lag signal means the status field did not reflect the trajectory — the numbers tell a different story than the status field alone.
  > 
  > ---
  > 
  > ### 4. Arcadia Property Group
  > **Construction phase · 2 signals · 52 days since substantive contact**
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Lifecycle | Construction | structured data |
  > | Operating covenants (DSCR/leverage) | Not in effect | structured data |
  > | Pre-leasing | **71%** (perm-conversion threshold: 75%) | performance data |
  > | Gap to threshold | **4 percentage points** | computed |
  > | Days since substantive contact | **52** | CRM activity log |
  > 
  > **Notable:** Operating covenants don't apply until conversion. The open items to monitor: % complete, schedule slip, interest-reserve runway, and whether pre-leasing reaches 75% before the conversion date.
  > 
  > ---
  > 
  > ### 5. Crestwood Capital Advisors
  > **Compliant · 0 signals · 46 days since substantive contact**
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | Compliant | structured data: covenant_status |
  > | Deterioration signals | 0 | computed |
  > | Days since substantive contact | **46** | CRM activity log |
  > 
  > **Structural note (from the tool):** Distress monitoring is designed to surface deterioration — it is structurally blind to a healthy borrower. Crestwood's 0-signal status means the monitoring lens has nothing to flag, not that no attention is warranted. Renewal/retention risk is a separate lens not captured here.
  > 
  > ---
  > 
  > **Reliability:** Facts are sourced from the `centerline` MCP server (structured performance data + CRM activity log). No figures are asserted without a source. No creditworthiness characterizations are made — all judgments originate with you. This readout is advisory; automated alerting designed, pending CCO approval (§4.1). Confidence is data-limited: as-of date is 2025-05-31; any activity or filings since then are not reflected.

  </details>
- run 3: ✅ PASS · tools=['Skill', 'ToolSearch', 'assemble_watchlist'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 3 — model's analysis</summary>

  > Here is the triage as of 2025-05-31, ranked by covenant breach → signal count → contact gap. Facts only — credit judgment is yours.
  > 
  > ---
  > 
  > ## Portfolio Triage — Week of 2026-06-13
  > 
  > ---
  > 
  > ### 1. Meridian Fabrication LLC — Covenant Breach | 4 signals | 78 days since substantive contact
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | **Breach** | covenant check |
  > | DSCR trend | 1.45 → 1.03 over 17 months | loan performance |
  > | Revolver utilization | 38% → **85%** (alert level: ≥75%) | loan performance |
  > | Days since substantive contact | **78** | activity log |
  > 
  > **Gaps:** Two distinct deterioration tracks (coverage compression + revolver draw) running simultaneously, with no substantive two-way contact in 78 days.
  > 
  > ---
  > 
  > ### 2. BlueLine Logistics LLC — Covenant Breach | 4 signals | 60 days since substantive contact
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | **Breach** | covenant check |
  > | DSCR trend | 1.58 → 0.95 over 17 months | loan performance |
  > | Revolver utilization | 42% → **85%** (alert level: ≥75%) | loan performance |
  > | Days since substantive contact | **60** | activity log |
  > 
  > **Gaps:** DSCR is below 1.0. Revolver at the same 85% level as Meridian. 60-day contact gap.
  > 
  > ---
  > 
  > ### 3. Summit Retail Partners — Compliant | 3 signals | 16 days since substantive contact
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | Compliant | covenant check |
  > | DSCR trend | 1.13 → 1.12 over 17 months | loan performance |
  > | Cushion above 1.10 floor | **0.02** | loan performance |
  > | Status-vs-trend lag | Label read "Compliant" during 6 months of DSCR decline | signal detection |
  > | Days since substantive contact | 16 | activity log |
  > 
  > **Gaps:** The compliance label has been trailing the trajectory. Cushion is 0.02 above the floor — one bad quarter closes it. Contact is current.
  > 
  > ---
  > 
  > ### 4. Arcadia Property Group — Construction | 2 signals | 52 days since substantive contact
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | Construction (operating covenants not yet in effect) | covenant check |
  > | Pre-leasing | **71%** vs 75% perm-conversion threshold | loan performance |
  > | Days since substantive contact | **52** | activity log |
  > 
  > **Gaps:** Pre-leasing is 4 points below the permanent-conversion threshold. Operating DSCR/leverage covenants don't apply yet; monitor % complete, schedule slip, interest-reserve runway, and pre-leasing progress. 52-day contact gap.
  > 
  > ---
  > 
  > ### 5. Crestwood Capital Advisors — Compliant | 0 signals | 46 days since substantive contact
  > 
  > | Metric | Value | Source |
  > |---|---|---|
  > | Covenant status | Compliant | covenant check |
  > | Deterioration signals | **0** | signal detection |
  > | Days since substantive contact | 46 | activity log |
  > 
  > **Note:** Zero signals means distress monitoring has nothing to flag — this tool is structurally blind to a healthy borrower. Renewal/retention risk is a separate lens not covered here.
  > 
  > ---
  > 
  > **Reliability:** Deterministic — all figures computed server-side from structured loan performance and activity log data. No model inference on the numbers. Contact gaps reflect last *substantive* two-way interaction, not last log entry. Data as of 2025-05-31; verify against current files before acting. This readout is RM-private and advisory; automated alerting is designed, pending CCO approval (§4.1).

  </details>

### A2
- run 1: ✅ PASS · tools=['Skill', 'ToolSearch', 'check_covenant_compliance'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 1 — model's analysis</summary>

  > **Meridian Fabrication LLC — Covenant Compliance as of 2025-05**
  > *(source: `check_covenant_compliance` server-side computation)*
  > 
  > ---
  > 
  > **DSCR**
  > | | |
  > |---|---|
  > | Reported DSCR | 1.03 |
  > | Covenant minimum | 1.20 |
  > | Cushion | **−0.17** |
  > | Breach | **Yes** |
  > 
  > **Leverage**
  > | | |
  > |---|---|
  > | Reported leverage | 4.5× |
  > | Covenant maximum | 4.0× |
  > | Headroom | **−0.5×** |
  > | Breach | **Yes** |
  > 
  > **Revolver utilization:** 85%
  > 
  > ---
  > 
  > **Reported status vs. computed status**
  > 
  > Both the reported `covenant_status` and the server-computed result are **"Covenant Breach"** — they match (`status_matches_computed: true`). There is no mislabeling; the reported status accurately reflects the math.
  > 
  > ---
  > 
  > *Facts only — the RM owns any credit judgment (§4.2). No credit characterization has been made.*

  </details>
- run 2: ✅ PASS · tools=['Skill', 'ToolSearch', 'check_covenant_compliance', 'detect_deterioration_signals'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 2 — model's analysis</summary>

  > Here are the facts for Meridian Fabrication LLC as of 2025-05.
  > 
  > ---
  > 
  > ## Covenant Compliance — Meridian Fabrication LLC (2025-05)
  > 
  > ### DSCR
  > | Metric | Value |
  > |---|---|
  > | Reported DSCR | 1.03 |
  > | Covenant minimum | 1.20 |
  > | Cushion | **−0.17** (breach) |
  > 
  > ### Leverage
  > | Metric | Value |
  > |---|---|
  > | Reported leverage | 4.5× |
  > | Covenant maximum | 4.0× |
  > | Headroom | **−0.5×** (breach) |
  > 
  > ### Other
  > - Revolver utilization: **85.0%** (≥ 75% alert level)
  > - Reported `covenant_status`: **Covenant Breach**
  > - Computed status: **Covenant Breach**
  > - Status matches computed: **Yes**
  > 
  > ---
  > 
  > ### Status vs. Trend
  > 
  > The current reported status is accurate — but it lagged the trajectory. DSCR declined from **1.45 → 1.03 over 17 months**, and the `covenant_status` field read **"Compliant" for 8 months of that decline** before the breach label appeared. Revolver utilization moved from **38% → 85%** over the same window, consistent with the DSCR direction.
  > 
  > Source: `check_covenant_compliance` + `detect_deterioration_signals`, Meridian Fabrication LLC, data/structured, as of 2025-05.
  > 
  > ---
  > 
  > **Reliability: Deterministic — High.** Both covenant tests and trend signals are computed server-side from structured loan-performance data. No model inference involved in the numbers. The status-lag finding is a direct comparison of the `covenant_status` field against the DSCR series. No cross-source conflicts identified.

  </details>
- run 3: ✅ PASS · tools=['Skill', 'ToolSearch', 'check_covenant_compliance'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 3 — model's analysis</summary>

  > Here are the facts for Meridian Fabrication LLC as of 2025-05:
  > 
  > **DSCR**
  > - Reported: **1.03** vs covenant minimum of **1.20**
  > - Cushion: **−0.17** (breach)
  > 
  > **Leverage**
  > - Reported: **4.5x** vs covenant maximum of **4.0x**
  > - Headroom: **−0.5x** (breach)
  > 
  > **Revolver utilization:** 85%
  > 
  > **Covenant status — reported vs computed:**
  > Both the reported `covenant_status` and the server-computed result are **"Covenant Breach"** — they match. There is no mislabeling gap.
  > 
  > ---
  > 
  > *Source: `check_covenant_compliance("Meridian")`, as_of 2025-05. The DSCR and leverage tests are computed server-side. The RM owns any credit judgment (§4.2).*
  > 
  > **Reliability: High** — numbers are deterministic (server-side math), reported and computed statuses agree, single source with no cross-source conflicts. No unverified claims. Trend direction (whether the breach is worsening) is not covered here — use the deterioration-signals skill for that.

  </details>

### A3
- run 1: ✅ PASS · tools=['Skill', 'ToolSearch', 'measure_engagement_coverage'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 1 — model's analysis</summary>

  > Here are the results as of 2025-05-31 (the data period), ranked by engagement gap:
  > 
  > ---
  > 
  > ## Engagement Coverage — All Borrowers
  > 
  > | Borrower | Last Substantive Contact | **Real Gap** | Naive Gap | Undercount |
  > |---|---|---|---|---|
  > | **Meridian Fabrication** | 2025-03-14 — Relationship Call | **78 days** | 33 days | −45 days |
  > | **BlueLine Logistics** | 2025-04-01 — Monthly Check-In | **60 days** | 29 days | −31 days |
  > | **Arcadia Property Group** | 2025-04-09 — Draw Review | **52 days** | 52 days | 0 |
  > | Crestwood Capital | 2025-04-15 — Renewal Meeting | 46 days | 19 days | −27 days |
  > | Summit Retail | 2025-05-15 — Relationship Call | 16 days | 16 days | 0 |
  > 
  > ---
  > 
  > ### Meridian — 78 days of silence
  > 
  > The log looks like only 33 days of quiet. The gap is actually **78 days** because the only entry since March 14 was an **April 28 Formal Notice (Sent — No Response)** — one-way, not a conversation. That notice inflates the naive count while the real relationship has gone cold.
  > 
  > **The undercount here is 45 days** — nearly six weeks of false comfort in the activity log.
  > 
  > ### BlueLine — 60 days, two one-way entries masking the gap
  > 
  > The April 14 Waiver Request (received) and the May 2 Internal Credit Committee Briefing both appear in the log but neither is a client conversation. The real gap to the last actual check-in is 60 days — **31 days hidden** behind process entries.
  > 
  > ### Arcadia — 52 days, no mask
  > 
  > The April 9 Draw Review ended with docs requested. Nothing since — no follow-up logged at all, one-way or otherwise. The gap is what the log says it is. Worth noting: docs were requested and the file shows no receipt or re-contact.
  > 
  > ### Crestwood and Summit — lower priority
  > 
  > Crestwood's 46-day gap follows an active Renewal Meeting; the log shows follow-ups (even if one-way). Summit had a substantive call 16 days ago. Neither is a silence concern at this snapshot.
  > 
  > ---
  > 
  > **Bottom line (facts):** Meridian has 78 days without a real conversation; BlueLine has 60. Both gaps are materially longer than their activity logs suggest. Arcadia's 52-day silence is unmasked but docs remain outstanding. The credit judgment on what these gaps mean is yours.
  > 
  > *Sources: `measure_engagement_coverage` MCP — deterministic, server-side. As-of: 2025-05-31. Excludes one-way notices, emails sent without response, missed calls, and internal prep per §4.2.*

  </details>
- run 2: ✅ PASS · tools=['Skill', 'ToolSearch', 'measure_engagement_coverage'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 2 — model's analysis</summary>

  > Here's what the data shows, as of the MCP's reference date of **2025-05-31**.
  > 
  > ---
  > 
  > ## Engagement Coverage — Distressed Borrowers
  > 
  > ### Meridian Fabrication LLC — 78 days since last two-way contact
  > | | |
  > |---|---|
  > | Last substantive contact | 2025-03-14 — Relationship Call (Completed) |
  > | Naive "days since any entry" | 33 days |
  > | **Undercount** | **45 days** hidden by a single one-way Formal Notice sent 2025-04-28 (no response) |
  > 
  > The formal notice on Apr 28 is the entire reason a naive log-check reads "only 33 days." Strip it out — as the tool does — and the real silence is 78 days. A formal notice with no response is not engagement.
  > 
  > ---
  > 
  > ### BlueLine Logistics LLC — 60 days since last two-way contact
  > | | |
  > |---|---|
  > | Last substantive contact | 2025-04-01 — Monthly Check-In (Completed) |
  > | Naive "days since any entry" | 29 days |
  > | **Undercount** | **31 days** hidden by a waiver request receipt (2025-04-14) and an internal credit-committee prep note (2025-05-02) |
  > 
  > The waiver request was *received from the borrower* but was not a substantive two-way conversation. The internal briefing is pure prep — no borrower contact at all. Real gap: 60 days, not 29.
  > 
  > ---
  > 
  > ### Arcadia Property Group — 52 days since last two-way contact
  > | | |
  > |---|---|
  > | Last substantive contact | 2025-04-09 — Draw Review (Docs Requested) |
  > | Naive "days since any entry" | 52 days (no undercount) |
  > | **Undercount** | **None** — no one-way contacts logged either |
  > 
  > Arcadia's gap is the "clean" kind: no activity at all since the draw review, not even a one-way notice. The last contact ended with docs outstanding.
  > 
  > ---
  > 
  > ### For completeness — non-distressed picture
  > 
  > | Borrower | Days since substantive contact | Undercount |
  > |---|---|---|
  > | Crestwood Capital Advisors | 46 days (renewal meeting 2025-04-15) | 27 days masked by follow-up emails |
  > | Summit Retail Partners | 16 days (relationship call 2025-05-15) | 0 |
  > 
  > ---
  > 
  > ## What stands out
  > 
  > **Meridian is the most acute gap among borrowers in apparent stress** — 78 days, with the only logged activity being an unanswered formal notice. The naive count would have hidden 45 of those days.
  > 
  > **BlueLine** is second at 60 days, with internal prep activity inflating the appearance of engagement.
  > 
  > **Arcadia** at 52 days has no masking at all — you simply haven't been in contact since docs were requested at the draw review.
  > 
  > ---
  > 
  > *Source: `mcp__centerline__measure_engagement_coverage`, all five borrowers, as_of 2025-05-31. Gaps are facts; credit judgments belong with the RM.*
  > 
  > ---
  > 
  > **Reliability: Moderate-High.** Deterministic computation from the MCP's activity log. Completeness depends on whether all contacts were logged — if any calls or meetings weren't entered, the gaps would be understated. Crestwood and Summit not characterized as distressed based on activity type alone; pair with `detecting-deterioration-signals` to confirm which borrowers warrant priority follow-up.

  </details>
- run 3: ✅ PASS · tools=['Skill', 'ToolSearch', 'measure_engagement_coverage'] · §4.2 hits=[] · missing facts=[]

  <details><summary>run 3 — model's analysis</summary>

  > Here are the results, ranked by engagement gap. All figures are as reported by the server (data as of **2025-05-31**).
  > 
  > ---
  > 
  > ## Engagement Coverage — Distressed / At-Risk Borrowers
  > 
  > | Borrower | Last substantive contact | Days silent | Naive days | Undercount | Notes since last real contact |
  > |---|---|---|---|---|---|
  > | **Meridian Fabrication** | 2025-03-14 — Relationship Call | **78 days** | 33 | **45 days** | 1× Formal Notice sent (2025-04-28) — no response |
  > | **BlueLine Logistics** | 2025-04-01 — Monthly Check-In | **60 days** | 29 | **31 days** | Waiver Request received (04-14); Internal Briefing / CC prep (05-02) — neither counts |
  > | **Arcadia Property Group** | 2025-04-09 — Draw Review | **52 days** | 52 | 0 | Docs requested at that meeting; nothing logged since |
  > | Crestwood Capital | 2025-04-15 — Renewal Meeting | 46 days | 19 | 27 days | Pricing follow-up + holding-pattern update — both one-way |
  > | Summit Retail | 2025-05-15 — Relationship Call | 16 days | 16 | 0 | Concerns noted; no gap issue |
  > 
  > ---
  > 
  > ### Meridian — your specific question
  > 
  > **78 days** since the last real two-way contact (2025-03-14 Relationship Call), as of 2025-05-31.
  > 
  > The April 28 Formal Notice does **not** count — it was sent with no response, making it one-way. The naive log shows only 33 days because that notice created an entry; the true gap is 45 days longer than it appears. Meridian is the most concerning combination: the longest silence in the book, and the only entry in that window is an unanswered formal notice.
  > 
  > ---
  > 
  > ### What stands out
  > 
  > - **Meridian** and **BlueLine** both have large undercounts — the CRM looks more active than it is because one-way touches and internal prep are inflating the "days since last entry" metric.
  > - **Arcadia** has no undercount because there's simply been no activity at all since the draw-review docs request — 52 days with nothing logged.
  > - **Summit** is the only borrower where the naive count and substantive count match and the gap is short.
  > 
  > ---
  > 
  > *Source: `mcp__centerline__measure_engagement_coverage` — deterministic, server-side. Facts only (§4.2); no credit characterization. RM review required before any escalation action.*

  </details>

## Honest limits

- **Non-deterministic** — the model can vary run to run; read the pass-rate, run with `--runs N`.
- **§4.2 use-vs-mention** — the scanner flags a blocked phrase even if the agent is *quoting* it to explain a block; rare for A1/A2/A3, noted not fatal.
- **Small prompt set** — the three Track-A prompts; Track-B prompts (emails/memos) will add a generative-quality layer that may warrant an LLM-as-judge (a signal, not ground truth).

