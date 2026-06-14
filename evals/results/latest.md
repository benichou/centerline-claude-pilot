# Eval results

_Generated 2026-06-13 by `evals/runner.py` against the live `centerline_mcp` logic._

**95/95 cases passed.**

Grading is deterministic: each case calls the real tool/guard and checks source-grounded
expectations. "Accuracy" is a clean number only here (T1/T2 ground truth); generative quality
(T4) is rubric + edit-rate, reported separately — never a fabricated single %.

| Case | Tier | Prompt | Result | Detail |
|---|---|---|---|---|
| `F-2.1-dossier-credit-grade-absent` | T2 | foundation | ✅ PASS | ok |
| `F-2.1-redaction-logged` | T2 | foundation | ✅ PASS | ok |
| `F-2.1-loanperf-row-no-grade` | T2 | foundation | ✅ PASS | ok |
| `F-2.1-loanperf-covstatus-kept` | T2-neg | foundation | ✅ PASS | ok |
| `F-2.1-activitylog-row-no-grade` | T2 | foundation | ✅ PASS | ok |
| `F-2.1-emails-no-designation` | T2 | foundation | ✅ PASS | ok |
| `F-2.1-emails-no-watchlist-word` | T2 | foundation | ✅ PASS | ok |
| `F-5-dossier-halts` | T2 | foundation | ✅ PASS | raised ComplianceRefusal |
| `F-5-covenant-halts` | T2 | foundation | ✅ PASS | raised ComplianceRefusal |
| `F-5-activitylog-halts` | T2 | foundation | ✅ PASS | raised ComplianceRefusal |
| `F-5-emails-halts` | T2 | foundation | ✅ PASS | raised ComplianceRefusal |
| `F-5-no-false-halt` | T2-neg | foundation | ✅ PASS | ok |
| `F-guarantor-refused` | T2 | foundation | ✅ PASS | raised ComplianceRefusal |
| `F-guarantor-normal-doc-ok` | T2-neg | foundation | ✅ PASS | ok |
| `F-4.2-block-high-credit-risk` | T2 | foundation | ✅ PASS | ok |
| `F-4.2-block-downgrade` | T2 | foundation | ✅ PASS | ok |
| `F-4.2-block-elevated-risk` | T2 | foundation | ✅ PASS | ok |
| `F-4.2-block-waiver` | T2 | foundation | ✅ PASS | ok |
| `F-4.2-block-creditworthy` | T2 | foundation | ✅ PASS | ok |
| `F-4.2-block-prob-default` | T2 | foundation | ✅ PASS | ok |
| `F-4.2-block-risk-rating` | T2 | foundation | ✅ PASS | ok |
| `F-4.2-allow-factual` | T2-neg | foundation | ✅ PASS | ok |
| `F-4.2-allow-cushion` | T2-neg | foundation | ✅ PASS | ok |
| `F-4.2-allow-missing-info` | T2-neg | foundation | ✅ PASS | ok |
| `F-rel-uncited-unverified` | T2 | foundation | ✅ PASS | ok |
| `F-rel-toolsourced-grounded` | T2 | foundation | ✅ PASS | ok |
| `F-rel-lowconf-partial` | T2 | foundation | ✅ PASS | ok |
| `A2-meridian-dscr` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-cushion` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-leverage` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-status` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-revolver` | T1 | A2 | ✅ PASS | ok |
| `A2-blueline-dscr` | T1 | A2 | ✅ PASS | ok |
| `A2-blueline-leverage-barely-ok` | T1 | A2 | ✅ PASS | ok |
| `A2-blueline-status` | T1 | A2 | ✅ PASS | ok |
| `A2-crestwood-compliant` | T1-neg | A2 | ✅ PASS | ok |
| `A2-crestwood-cushion` | T1-neg | A2 | ✅ PASS | ok |
| `A2-summit-compliant` | T1-neg | A2 | ✅ PASS | ok |
| `A2-summit-thin-cushion-value` | T1 | A2 | ✅ PASS | ok |
| `A2-arcadia-na` | T1 | A2 | ✅ PASS | ok |
| `A2-arcadia-reported-construction` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-dscrtrend` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-revtrend` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-revalert` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-mislabel` | T1 | A2 | ✅ PASS | ok |
| `A2-meridian-4signals` | T1 | A2 | ✅ PASS | ok |
| `A2-blueline-dscrtrend` | T1 | A2 | ✅ PASS | ok |
| `A2-blueline-revalert` | T1 | A2 | ✅ PASS | ok |
| `A2-blueline-mislabel` | T1 | A2 | ✅ PASS | ok |
| `A2-blueline-4signals` | T1 | A2 | ✅ PASS | ok |
| `A1-crestwood-zero-signals` | T1-neg | A1 | ✅ PASS | ok |
| `A2-summit-thincushion` | T1 | A2 | ✅ PASS | ok |
| `A2-summit-dscrtrend` | T1 | A2 | ✅ PASS | ok |
| `A2-summit-mislabel` | T1 | A2 | ✅ PASS | ok |
| `A2-summit-3signals` | T1 | A2 | ✅ PASS | ok |
| `A2-arcadia-leaseup` | T1 | A2 | ✅ PASS | ok |
| `A2-arcadia-lifecycle` | T1 | A2 | ✅ PASS | ok |
| `A3-meridian-gap-78` | T1 | A3 | ✅ PASS | ok |
| `A3-meridian-naive-33` | T1 | A3 | ✅ PASS | ok |
| `A3-meridian-undercount-45` | T1 | A3 | ✅ PASS | ok |
| `A3-meridian-asof` | T1 | A3 | ✅ PASS | ok |
| `A3-meridian-lastsub` | T1 | A3 | ✅ PASS | ok |
| `A3-meridian-onewaynotice` | T1 | A3 | ✅ PASS | ok |
| `A3-blueline-gap-60` | T1 | A3 | ✅ PASS | ok |
| `A3-blueline-naive-29` | T1 | A3 | ✅ PASS | ok |
| `A3-blueline-lastsub` | T1 | A3 | ✅ PASS | ok |
| `A3-blueline-oneway` | T1 | A3 | ✅ PASS | ok |
| `A3-crestwood-substantive` | T1 | A3 | ✅ PASS | ok |
| `A3-crestwood-gap-46` | T1 | A3 | ✅ PASS | ok |
| `A3-summit-gap-16` | T1 | A3 | ✅ PASS | ok |
| `A3-summit-no-undercount` | T1-neg | A3 | ✅ PASS | ok |
| `A3-arcadia-gap-52` | T1 | A3 | ✅ PASS | ok |
| `A3-arcadia-no-undercount` | T1-neg | A3 | ✅ PASS | ok |
| `A1-count` | T1 | A1 | ✅ PASS | ok |
| `A1-meridian-first` | T1 | A1 | ✅ PASS | ok |
| `A1-meridian-breach-flag` | T1 | A1 | ✅ PASS | ok |
| `A1-blueline-second` | T1 | A1 | ✅ PASS | ok |
| `A1-summit-third` | T1 | A1 | ✅ PASS | ok |
| `A1-arcadia-fourth` | T1 | A1 | ✅ PASS | ok |
| `A1-crestwood-last` | T1-neg | A1 | ✅ PASS | ok |
| `A1-crestwood-zero-entry` | T1-neg | A1 | ✅ PASS | ok |
| `B2-xval-recompute-dscr` | T1 | B2 | ✅ PASS | ok |
| `B2-xval-no-reconcile` | T1 | B2 | ✅ PASS | ok |
| `B2-xval-addback-bridge` | T1 | B2 | ✅ PASS | ok |
| `B2-xval-mismatches-dscr-and-leverage` | T1 | B2 | ✅ PASS | ok |
| `B2-xval-bank-corroborates` | T1 | B2 | ✅ PASS | ok |
| `B2-pkg-missing-aerospace-po` | T2 | B2 | ✅ PASS | ok |
| `B2-pkg-missing-projections` | T2 | B2 | ✅ PASS | ok |
| `B2-pkg-unsigned-rep-letter` | T2 | B2 | ✅ PASS | ok |
| `B2-pkg-ar-names-withheld` | T2 | B2 | ✅ PASS | ok |
| `B2-pkg-guarantor-refused` | T2 | B2 | ✅ PASS | ok |
| `B3-timeline-merged-count` | T1 | B3 | ✅ PASS | ok |
| `B3-timeline-misdating-visible` | T1 | B3 | ✅ PASS | ok |
| `B1-retention-crestwood-fires` | T1 | B1 | ✅ PASS | ok |
| `B1-retention-meridian-negative` | T1 | B1 | ✅ PASS | ok |
