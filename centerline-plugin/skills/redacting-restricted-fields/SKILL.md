---
name: redacting-restricted-fields
description: Reference — what §2.1 prohibits as AI inputs and how it's enforced. Read when handling borrower data or documents, especially anything that looks like a rating, watchlist/Special-Assets status, or a guarantor's personal financials.
---

# Redacting restricted fields (§2.1) — enforced server-side

The `centerline` MCP server **strips/guards restricted inputs before they reach you**, so you normally never
see them. The §2.1-prohibited inputs:

- **Internal credit ratings** (e.g., `credit_grade`), **watchlist**, and **Special-Assets designations** →
  stripped / redacted.
- **Guarantor personal financial documents** (personal tax returns, bank statements, net-worth statements) →
  **REFUSED, not read.**
- Also (not present in this corpus): SSN/EIN, NDA-restricted data, attorney-client-privileged material.

**§5:** borrowers in **Special Assets or active litigation** → processing **HALTS**.

## Your responsibilities
- **Always retrieve through the `centerline` MCP tools** — never read raw files to get around the strip.
- If you ever encounter a restricted field or a guarantor document, **do not process it** — note the refusal.
- Factual covenant status (e.g., "covenant_status: Covenant Breach") is **allowed** and stays — it's an
  observed fact, not a rating.

Enforcement is **server-side (works in Code and Cowork)**, plus a Code-side hook as defense-in-depth.
