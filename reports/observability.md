# Observability — per-prompt scorecards

_Generated 2026-06-13 by `evals/observability.py` from the live `centerline_mcp` logic + the run-trace ledger._

**Performance is not one number.** It decomposes into **compliance (T2) + step-correctness (T3) + computation accuracy (T1) + generative quality (T4)**. T1/T2 are graded deterministically below; T3 is the expected-trace each prompt should exercise; T4 (emails/memos) is rubric + HITL edit-rate, reported with Track B — never a fabricated single %.

**Overall T1/T2: 95/95 cases passed.** Run-trace ledger: 44 tool-use event(s) recorded by the PreToolUse hook (Code-only).

## At a glance

| Prompt | Skills | MCP tools | T1/T2 cases | Reliability |
|---|---|---|---|---|
| **A1** Who needs attention this week? | assembling-watchlist-triage | 1 | 9/9 ✅ | Grounded — every line cited; ranking is deterministic, not a credit rating |
| **A2** Is Meridian covenant-compliant — cushion and trend? | checking-covenant-compliance, detecting-deterioration-signals | 2 | 29/29 ✅ | Grounded — math computed in code; status-vs-trend mislabel surfaced |
| **A3** Which distressed borrowers have I gone quiet on? ★ | measuring-engagement-coverage | 1 | 16/16 ✅ | Grounded — one-way notices excluded; 78d vs naive 33d |
| **B1** Prep me for Crestwood — retention radar ★ (the inverse of early-warning) | flagging-renewal-and-retention, building-client-360 | 1 | 2/2 ✅ | Grounded — facts + 'engage'; never a rate (pricing committee owns that); §4.1 for automation |
| **B2** Meridian covenant-package intake (doc-intel) | reviewing-covenant-package | 1 | 10/10 ✅ | Partial — certified-vs-recomputed mismatch + missing/unsigned/withheld surfaced; extraction is model-driven |
| **B3** Reconcile Arcadia emails vs the CRM log ★ (close-the-loop) | detecting-cross-source-discrepancies, verifying-commitment-fulfillment | 4 | 2/2 ✅ | Partial — synthesis kept honest by grounding + scribe-not-author + footer (not pretend-deterministic) |
| **B4** Summit annual relationship-review memo (decomposed §4.2) | drafting-relationship-review-memos, building-client-360 | 4 | — | T4 (generative) — rubric + HITL: facts cited, assessment RM-authored & non-empty; no deterministic golden case |
| **foundation** Cross-cutting compliance guards (every prompt routes through these) | redacting-restricted-fields, screening-and-gating-output, assessing-output-reliability | 1 | 27/27 ✅ | n/a — these ARE the reliability/compliance layer |

## Per-prompt detail

### A1 — Who needs attention this week?

- **Expected skills (T3):** assembling-watchlist-triage
- **Expected MCP tools (T3):** assemble_watchlist (composes check_covenant_compliance + detect_deterioration_signals + measure_engagement_coverage)
- **Guards that must fire:** §2.1 strip, §5 gate, screen_and_finalize (§4.2 + footer + §4.3)
- **Expected reliability footer:** Grounded — every line cited; ranking is deterministic, not a credit rating
- **Eval (T1/T2): 9/9 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|
| `A1-crestwood-zero-signals` | T1-neg | ✅ | loan_performance_monthly.csv (Crestwood pristine/improving -> early-warning blind) | ok |
| `A1-count` | T1 | ✅ | portfolio_reference.csv (5 borrowers) | ok |
| `A1-meridian-first` | T1 | ✅ | composed: breach + 4 signals + 78d gap -> ranked #1 | ok |
| `A1-meridian-breach-flag` | T1 | ✅ | computed covenant breach for Meridian | ok |
| `A1-blueline-second` | T1 | ✅ | breach + 4 signals + 60d gap -> ranked #2 (less neglect than Meridian) | ok |
| `A1-summit-third` | T1 | ✅ | no breach but 3 signals -> ranks above construction Arcadia (2 signals) | ok |
| `A1-arcadia-fourth` | T1 | ✅ | construction, 2 signals -> ranked #4 | ok |
| `A1-crestwood-last` | T1-neg | ✅ | compliant + 0 signals -> last (early-warning blind to a healthy borrower) | ok |
| `A1-crestwood-zero-entry` | T1-neg | ✅ | Crestwood watchlist entry: not breach, 0 signals | ok |

### A2 — Is Meridian covenant-compliant — cushion and trend?

- **Expected skills (T3):** checking-covenant-compliance, detecting-deterioration-signals
- **Expected MCP tools (T3):** check_covenant_compliance, detect_deterioration_signals
- **Guards that must fire:** §2.1 strip, §5 gate, screen_and_finalize (§4.2 + footer + §4.3)
- **Expected reliability footer:** Grounded — math computed in code; status-vs-trend mislabel surfaced
- **Eval (T1/T2): 29/29 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|
| `A2-meridian-dscr` | T1 | ✅ | loan_performance_monthly.csv (Meridian, 2025-05) | ok |
| `A2-meridian-cushion` | T1 | ✅ | computed: 1.03 - 1.20 | ok |
| `A2-meridian-leverage` | T1 | ✅ | loan_performance_monthly.csv (Meridian, 2025-05) | ok |
| `A2-meridian-status` | T1 | ✅ | loan_performance_monthly.csv (Meridian, 2025-05) | ok |
| `A2-meridian-revolver` | T1 | ✅ | loan_performance_monthly.csv (Meridian, 2025-05 = 85%) | ok |
| `A2-blueline-dscr` | T1 | ✅ | loan_performance_monthly.csv (BlueLine, 2025-05) | ok |
| `A2-blueline-leverage-barely-ok` | T1 | ✅ | loan_performance_monthly.csv (BlueLine, 4.4 vs 4.5 max — passes by 0.1) | ok |
| `A2-blueline-status` | T1 | ✅ | DSCR-driven breach (leverage passes) | ok |
| `A2-crestwood-compliant` | T1-neg | ✅ | loan_performance_monthly.csv (Crestwood pristine) | ok |
| `A2-crestwood-cushion` | T1-neg | ✅ | loan_performance_monthly.csv (Crestwood DSCR 2.61 vs 1.15) | ok |
| `A2-summit-compliant` | T1-neg | ✅ | loan_performance_monthly.csv (Summit) | ok |
| `A2-summit-thin-cushion-value` | T1 | ✅ | loan_performance_monthly.csv (Summit DSCR 1.12 vs 1.10 floor) | ok |
| `A2-arcadia-na` | T1 | ✅ | loan_performance_monthly.csv (Arcadia = Construction) | ok |
| `A2-arcadia-reported-construction` | T1 | ✅ | loan_performance_monthly.csv (Arcadia covenant_status = Construction) | ok |
| `A2-meridian-dscrtrend` | T1 | ✅ | loan_performance_monthly.csv (Meridian full series, 1.45->1.03) | ok |
| `A2-meridian-revtrend` | T1 | ✅ | loan_performance_monthly.csv (Meridian revolver 38->85%) | ok |
| `A2-meridian-revalert` | T1 | ✅ | loan_performance_monthly.csv (Meridian 85% >= 75% alert) | ok |
| `A2-meridian-mislabel` | T1 | ✅ | loan_performance_monthly.csv (status 'Compliant' during DSCR decline) | ok |
| `A2-meridian-4signals` | T1 | ✅ | composed: dscr_trend + revolver_trend + revolver_alert + status_vs_trend | ok |
| `A2-blueline-dscrtrend` | T1 | ✅ | loan_performance_monthly.csv (BlueLine 1.58->0.95) | ok |
| `A2-blueline-revalert` | T1 | ✅ | loan_performance_monthly.csv (BlueLine revolver 85%) | ok |
| `A2-blueline-mislabel` | T1 | ✅ | loan_performance_monthly.csv (BlueLine status lagged DSCR decline) | ok |
| `A2-blueline-4signals` | T1 | ✅ | composed: 4 signals | ok |
| `A2-summit-thincushion` | T1 | ✅ | loan_performance_monthly.csv (Summit 1.12 vs 1.10 floor) | ok |
| `A2-summit-dscrtrend` | T1 | ✅ | loan_performance_monthly.csv (Summit DSCR peaked 1.21 then declined to 1.12) | ok |
| `A2-summit-mislabel` | T1 | ✅ | loan_performance_monthly.csv (Summit status 'Compliant' during decline) | ok |
| `A2-summit-3signals` | T1 | ✅ | composed: dscr_trend + status_vs_trend + thin_cushion | ok |
| `A2-arcadia-leaseup` | T1 | ✅ | loan_performance_monthly.csv (Arcadia pre-leasing 71% vs 75%) | ok |
| `A2-arcadia-lifecycle` | T1 | ✅ | construction lifecycle signal (operating covenants N/A) | ok |

### A3 — Which distressed borrowers have I gone quiet on? ★

- **Expected skills (T3):** measuring-engagement-coverage
- **Expected MCP tools (T3):** measure_engagement_coverage
- **Guards that must fire:** §2.1 strip, §5 gate, screen_and_finalize (§4.2 + footer + §4.3)
- **Expected reliability footer:** Grounded — one-way notices excluded; 78d vs naive 33d
- **Eval (T1/T2): 16/16 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|
| `A3-meridian-gap-78` | T1 | ✅ | rm_activity_log.csv (Meridian last substantive 2025-03-14) vs as-of 2025-05-31 | ok |
| `A3-meridian-naive-33` | T1 | ✅ | rm_activity_log.csv (Meridian last any entry 2025-04-28) -> naive undercount | ok |
| `A3-meridian-undercount-45` | T1 | ✅ | computed: 78 - 33 = 45-day undercount the naive field hides | ok |
| `A3-meridian-asof` | T1 | ✅ | loan_performance_monthly.csv (latest month 2025-05 -> month-end as-of) | ok |
| `A3-meridian-lastsub` | T1 | ✅ | rm_activity_log.csv (Meridian 2025-03-14 substantive contact) | ok |
| `A3-meridian-onewaynotice` | T1 | ✅ | rm_activity_log.csv (Meridian 2025-04-28 = one-way overdue notice, not a contact) | ok |
| `A3-blueline-gap-60` | T1 | ✅ | rm_activity_log.csv (BlueLine last substantive 2025-04-01) vs as-of 2025-05-31 | ok |
| `A3-blueline-naive-29` | T1 | ✅ | rm_activity_log.csv (BlueLine last any entry 2025-05-02) | ok |
| `A3-blueline-lastsub` | T1 | ✅ | rm_activity_log.csv (BlueLine 2025-04-01 substantive) | ok |
| `A3-blueline-oneway` | T1 | ✅ | rm_activity_log.csv (BlueLine one-way entries after 04-01) | ok |
| `A3-crestwood-substantive` | T1 | ✅ | rm_activity_log.csv (Crestwood 2025-04-15 'Renewal Proposal Presented' = substantive; regression: must not match 'sent' in 'presented') | ok |
| `A3-crestwood-gap-46` | T1 | ✅ | rm_activity_log.csv (Crestwood last substantive 2025-04-15) vs as-of 2025-05-31 | ok |
| `A3-summit-gap-16` | T1 | ✅ | rm_activity_log.csv (Summit last substantive 2025-05-15) vs as-of 2025-05-31 | ok |
| `A3-summit-no-undercount` | T1-neg | ✅ | Summit's last entry IS substantive -> naive == true gap (the contact nuance is localized to Meridian) | ok |
| `A3-arcadia-gap-52` | T1 | ✅ | rm_activity_log.csv (Arcadia last substantive 2025-04-09) vs as-of 2025-05-31 | ok |
| `A3-arcadia-no-undercount` | T1-neg | ✅ | Arcadia naive == true gap (no one-way-notice undercount) | ok |

### B1 — Prep me for Crestwood — retention radar ★ (the inverse of early-warning)

- **Expected skills (T3):** flagging-renewal-and-retention, building-client-360
- **Expected MCP tools (T3):** flag_renewal_and_retention (reuses check_covenant_compliance + detect_deterioration_signals)
- **Guards that must fire:** §2.1 strip, §5 gate, screen_and_finalize (§4.2 + footer + §4.3)
- **Expected reliability footer:** Grounded — facts + 'engage'; never a rate (pricing committee owns that); §4.1 for automation
- **Eval (T1/T2): 2/2 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|
| `B1-retention-crestwood-fires` | T1 | ✅ | Crestwood: healthy/improving, matures 2026-08-31, First Midwest 4.90% term sheet on record, attrition noted | ok |
| `B1-retention-meridian-negative` | T1 | ✅ | negative case: a breached/distressed borrower is a DISTRESS flag, not a retention flag | ok |

### B2 — Meridian covenant-package intake (doc-intel)

- **Expected skills (T3):** reviewing-covenant-package
- **Expected MCP tools (T3):** cross_validate_covenant + review_package (deterministic — graded here); classify_document + extract_document_fields (model/API — graded by the live agent-eval + unit tests)
- **Guards that must fire:** §2.1 guarantor refusal (pre-screen), screen_and_finalize (§4.2 + footer + §4.3)
- **Expected reliability footer:** Partial — certified-vs-recomputed mismatch + missing/unsigned/withheld surfaced; extraction is model-driven
- **Eval (T1/T2): 10/10 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|
| `B2-xval-recompute-dscr` | T1 | ✅ | synthetic Meridian financials: GAAP EBITDA 10,100 / debt service 9,800 = 1.03 | ok |
| `B2-xval-no-reconcile` | T1 | ✅ | certified 1.23/3.76 vs recomputed 1.03/4.50 do not match | ok |
| `B2-xval-addback-bridge` | T1 | ✅ | Adjusted EBITDA 12,100 - GAAP 10,100 = 2,000 of add-backs | ok |
| `B2-xval-mismatches-dscr-and-leverage` | T1 | ✅ | both DSCR and leverage diverge certified-vs-recomputed | ok |
| `B2-xval-bank-corroborates` | T1 | ✅ | the bank's own loan_performance (Meridian, 2025-05) DSCR 1.03 agrees with the recompute | ok |
| `B2-pkg-missing-aerospace-po` | T2 | ✅ | Meridian Feb-14 follow-up list: aerospace PO not received | ok |
| `B2-pkg-missing-projections` | T2 | ✅ | Meridian Feb-14 follow-up list: updated 12-month projections not received | ok |
| `B2-pkg-unsigned-rep-letter` | T2 | ✅ | the management representation letter is unsigned (signed=false) | ok |
| `B2-pkg-ar-names-withheld` | T2 | ✅ | A/R aging present but customer names withheld (customer_names_present=false) | ok |
| `B2-pkg-guarantor-refused` | T2 | ✅ | §2.1: a guarantor personal financial statement is refused on intake | ok |

### B3 — Reconcile Arcadia emails vs the CRM log ★ (close-the-loop)

- **Expected skills (T3):** detecting-cross-source-discrepancies, verifying-commitment-fulfillment
- **Expected MCP tools (T3):** get_relationship_timeline, get_emails, get_activity_log, detect_deterioration_signals
- **Guards that must fire:** §2.1 redaction, §5 gate, scribe-not-author (§4.2), screen_and_finalize
- **Expected reliability footer:** Partial — synthesis kept honest by grounding + scribe-not-author + footer (not pretend-deterministic)
- **Eval (T1/T2): 2/2 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|
| `B3-timeline-merged-count` | T1 | ✅ | Arcadia: 11 activity-log entries + 5 email messages | ok |
| `B3-timeline-misdating-visible` | T1 | ✅ | the Apr-09 log row sorts immediately before the Apr-22 Draw #13 email it summarizes | ok |

### B4 — Summit annual relationship-review memo (decomposed §4.2)

- **Expected skills (T3):** drafting-relationship-review-memos, building-client-360
- **Expected MCP tools (T3):** get_loan_performance, check_covenant_compliance, detect_deterioration_signals, get_activity_log
- **Guards that must fire:** RM-authored assessment required (§4.2 origination), screen_and_finalize (§4.2 + footer + §4.3)
- **Expected reliability footer:** T4 (generative) — rubric + HITL: facts cited, assessment RM-authored & non-empty; no deterministic golden case
- **Eval (T1/T2): 0/0 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|

### foundation — Cross-cutting compliance guards (every prompt routes through these)

- **Expected skills (T3):** redacting-restricted-fields, screening-and-gating-output, assessing-output-reliability
- **Expected MCP tools (T3):** (server-side guards) + screen_and_finalize
- **Guards that must fire:** §2.1 strip, §5 gate, guarantor refusal, §4.2 output block, reliability footer
- **Expected reliability footer:** n/a — these ARE the reliability/compliance layer
- **Eval (T1/T2): 27/27 passed**

| Case | Tier | Result | Grounded in | Detail |
|---|---|---|---|---|
| `F-2.1-dossier-credit-grade-absent` | T2 | ✅ | portfolio_reference.csv credit_grade (B+/BB-/A-) is an internal rating (§2.1) | ok |
| `F-2.1-redaction-logged` | T2 | ✅ | the strip is logged for the §7 audit trail | ok |
| `F-2.1-loanperf-row-no-grade` | T2 | ✅ | loan_performance rows must not carry the internal rating | ok |
| `F-2.1-loanperf-covstatus-kept` | T2-neg | ✅ | covenant_status is FACTUAL (kept, not stripped) — decided 2026-06-09 | ok |
| `F-2.1-activitylog-row-no-grade` | T2 | ✅ | activity_log rows must not carry the internal rating | ok |
| `F-2.1-emails-no-designation` | T2 | ✅ | watchlist/Special-Assets designation language is §2.1-restricted in free text | ok |
| `F-2.1-emails-no-watchlist-word` | T2 | ✅ | the word 'watchlist' is a restricted designation (§2.1) | ok |
| `F-5-dossier-halts` | T2 | ✅ | §5 — no AI processing for Special-Assets/litigation borrowers | raised ComplianceRefusal |
| `F-5-covenant-halts` | T2 | ✅ | §5 gate applies to the analysis tools too | raised ComplianceRefusal |
| `F-5-activitylog-halts` | T2 | ✅ | §5 gate applies to the CRM read too | raised ComplianceRefusal |
| `F-5-emails-halts` | T2 | ✅ | §5 gate applies before reading the email thread | raised ComplianceRefusal |
| `F-5-no-false-halt` | T2-neg | ✅ | a normal (non-SA) borrower must NOT be halted | ok |
| `F-guarantor-refused` | T2 | ✅ | §2.1 — guarantor personal financials may not be sent to AI | raised ComplianceRefusal |
| `F-guarantor-normal-doc-ok` | T2-neg | ✅ | a normal covenant certificate must NOT be refused | ok |
| `F-4.2-block-high-credit-risk` | T2 | ✅ | §4.2 — characterizing + predictive + recommending language | ok |
| `F-4.2-block-downgrade` | T2 | ✅ | §4.2 — recommending a rating change | ok |
| `F-4.2-block-elevated-risk` | T2 | ✅ | §4.2 — the policy's own example ('elevated risk', even framed as information) | ok |
| `F-4.2-block-waiver` | T2 | ✅ | §4.2 — recommending a covenant waiver | ok |
| `F-4.2-block-creditworthy` | T2 | ✅ | §4.2 — characterizing creditworthiness | ok |
| `F-4.2-block-prob-default` | T2 | ✅ | §4.2 — predictive credit language | ok |
| `F-4.2-block-risk-rating` | T2 | ✅ | §4.2 — risk-rating language (RM initiates rating changes, not AI) | ok |
| `F-4.2-allow-factual` | T2-neg | ✅ | §4.2 — factual covenant status is allowed (not a characterization) | ok |
| `F-4.2-allow-cushion` | T2-neg | ✅ | §4.2 — a cushion figure is an observed fact | ok |
| `F-4.2-allow-missing-info` | T2-neg | ✅ | §4.2 explicitly permits flagging missing information | ok |
| `F-rel-uncited-unverified` | T2 | ✅ | an uncited factual claim is flagged Unverified (not blocked) | ok |
| `F-rel-toolsourced-grounded` | T2 | ✅ | regression (Cowork-surfaced): tool/as-of provenance must read Grounded, not Unverified | ok |
| `F-rel-lowconf-partial` | T2 | ✅ | a cited claim built on a low-confidence (reconstructed/back-dated) input -> Partial, not Grounded | ok |

## Honest limits

- **Skill selection is probabilistic.** Mitigated because the critical math/compliance lives in deterministic MCP tools (enforced + testable), not in model choice; the T3 expected-trace above is the check, and the eval cases pin the tool outputs.
- **The run-trace ledger is coarse today.** The PreToolUse hook records that a tool was used (Code-only), not which *skill* selected it. Full per-step attribution (a `log_step` MCP tool + a per-run `traces/run-<id>.jsonl`) is the production path; in prod the same hooks emit OpenTelemetry → Datadog as the §4.1 monitoring evidence.
- **The golden set is small and self-authored.** Mitigated by source-grounded expected answers and negative/adversarial cases (a clean borrower must not flag; a normal doc must not be refused); production path is a larger labeled set + real RM accept/edit/dismiss feedback.
