# data/ — operational corpus (the ONLY content the MCP serves)

This folder is the **bank's data** that the `centerline` MCP server retrieves over. Everything here is
**synthetic / fictional**. Build/guidance material (compliance policy, personas, Tom's shadow workflows)
lives in **`../reference/`** and is **NOT served by the MCP** — it informs how we build, it is never
retrieved as borrower data.

## Manifest
| Path | Content | Served as |
|---|---|---|
| `structured/portfolio_reference.csv` | 5 borrowers × relationship metadata | `get_borrower_dossier` |
| `structured/loan_performance_monthly.csv` | 17 months of financials + covenant data | `get_loan_performance` / `get_covenant_history` |
| `structured/rm_activity_log.csv` | CRM contact log (3 RMs) | `get_activity_log` |
| `emails/thread-1..4-*.md` | 4 email threads (Meridian, BlueLine, Crestwood, Arcadia) | `get_emails` |
| `memos/relationship-review/meridian-review.md` | the one (input) relationship-review memo | part of `get_borrower_dossier` (Meridian) |
| `synthetic/` | synthetic covenant package(s) — Phase 3 | `list_documents` / `get_document` |

## §2.1 restricted-field map (the MCP strips/guards these server-side, before anything reaches the model)
- **HARD-restricted field → strip:** `portfolio_reference.credit_grade` (internal credit rating: B+ / BB- / A- …). Never leaves the server.
- **Free-text scan → redact** (in `loan_performance.notes`, `rm_activity_log.raw_notes`, emails, memo): explicit **watchlist** / **Special Assets** / **active-litigation** designations, and any restated internal credit rating.
- **Guarantor:** `portfolio_reference.personal_guarantee` (Yes/No) is a structural flag and may stay; but any **guarantor *personal financial* document** is **refused, not read** (doc layer, Phase 3+).
- **§5 gate:** if a borrower is in **Special Assets** or **active litigation**, processing **STOPS** (no AI). *(None of the 5 are currently SA/litigation; the gate exists regardless.)*

### `covenant_status` — DECIDED (2026-06-09): keep as factual/allowed
- **`loan_performance.covenant_status`** (`Compliant / Watch / Breach`) is **kept** — a **factual covenant-compliance result** (like "DSCR < floor"), surfaced as a **fact, never a risk characterization** (§4.2). It is **not** an internal credit rating (that's `credit_grade`, which is stripped). We also **recompute compliance deterministically** (`recompute_ratios.py`) and treat the label with suspicion — the Meridian finding is that the label *mislabeled the trend*. So the field stays in the corpus and is surfaced as data; the real compliance call comes from the recompute.

> Restricted content is **kept in the corpus for fidelity** but is stripped/guarded at retrieval — it never reaches the model. The §2.1 strip + §5 gate are enforced **server-side** (universal chokepoint) and mirrored as hooks.
