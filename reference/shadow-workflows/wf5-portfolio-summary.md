---
source: centerline-bank/data/tom_shadow_workflows.pdf
workflow: 5
name: Portfolio Summary for Myself (Weekly)
architecture: single-turn prompt; paste a portfolio table (borrower, DSCR, covenant status, last contact, next action) across MULTIPLE accounts
self_reported_quality: "honestly impressive"; flagged the 6-week Crestwood contact gap Tom had lost track of
compliance_flag: "FLAG #2 — compiled portfolio-level summaries (borrower names + loan balances + DSCR across multiple accounts) into a single personal-ChatGPT prompt. Higher-risk aggregation (§1/§2). Also: the auto-flagging of contact gaps / deterioration is §4.1 automated monitoring → needs CCO approval before launch."
restricted_fields: []
---

# Workflow 5 — Portfolio Summary for Myself (Weekly)

Every Monday morning I do this to get my head straight for the week. Takes me about 15 minutes including the AI step.

> ⚠️ **COMPLIANCE FLAG:** Tom was compiling portfolio-level summaries that included borrower names, loan balances, and DSCR figures across multiple accounts and pasting them into ChatGPT in a single prompt. This represents a higher-risk data handling pattern than single-account queries.
>
> *(Analyst note: the contact-gap / deterioration flagging this produces is §4.1 automated monitoring — needs CCO approval before deployment, though it maps directly to the CCO's stated early-warning priority in §7.)*

**Prompt (verbatim):**
```
Here is a summary of my commercial loan portfolio as of [date]:
[paste table with: borrower, DSCR, covenant status, last contact date, next action needed]

Summarize:
1. Which borrowers need attention this week and why
2. Any patterns or trends I should be aware of across the portfolio
3. My top 3 priorities for the week

Be concise. I don't need explanations — just the most important things.
```

**Output quality is honestly impressive.** Last week it flagged that I hadn't contacted Crestwood in over 6 weeks and there was a pending renewal item. I had completely lost track of it.

*(Note: This is the Whitmore situation. Tom flagged it via AI before Sarah flagged it to him. He had not yet escalated to management as of the audit date.)*
