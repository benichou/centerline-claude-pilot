---
source: centerline-bank/data/compliance_policy.pdf
section: "Section 2 — Data Handling Requirements"
restricted_fields: []
key_constraint: "§2.1 bars internal credit ratings / watchlist / Special Assets designations as AI inputs even in approved tools — so credit_grade must be excluded from anything sent to Claude."
---

# Section 2 — Data Handling Requirements

## 2.1 Prohibited data inputs

The following data categories may **NOT** be entered into any AI tool, including approved tools, without explicit written approval from the Chief Compliance Officer:

- Social Security numbers, EIN, or other government identifiers of borrowers or guarantors.
- Non-public personal financial information of individual guarantors (personal tax returns, personal bank statements, personal net worth statements).
- Proprietary borrower financial data that has been disclosed under a confidentiality agreement.
- **Internal credit ratings, watchlist classifications, or Special Assets designations.**
- Information subject to attorney-client privilege.

## 2.2 Data that may be used in approved tools

The following data categories are approved for use in Claude for Work and Copilot for M365:

- Business financial data from covenant packages (revenue, EBITDA, DSCR, leverage) — borrower name may be included.
- Email correspondence between RMs and commercial borrowers.
- Draw request documentation.
- Publicly available information about borrowers (news, website, industry data).
- Internal call notes and relationship logs (non-privileged).
- Standard loan and covenant terms.

## 2.3 Data residency

Claude for Work is configured under an enterprise agreement with data processing within U.S. borders and no training on bank data. Staff should not assume any other AI tool meets this requirement.
