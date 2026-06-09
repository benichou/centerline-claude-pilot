---
source: centerline-bank/data/tom_shadow_workflows.pdf
workflow: 2
name: Relationship Review Memo Draft
architecture: single-turn prompt; Tom writes his own 2-3 sentence assessment first, then pastes everything else in
self_reported_quality: 70% usable; structure always right; 3-4 hrs → ~45 min
compliance_flag: "FLAG #1 — pasted borrower financial data (DSCR, revenue, leverage) and borrower NAMES into a personal (non-enterprise) ChatGPT account. Data-handling breach (§1 personal-account tool, §2 data handling, §5/§6); the memo output also risks §4.2 (credit-adjacent language). Doc cites '§4.2'."
restricted_fields: []
is_solution_a_target: true
---

# Workflow 2 — Relationship Review Memo Draft

This is the big one. These memos take me 3-4 hours normally. With this prompt and my notes, I'm down to about 45 minutes including review.

> ⚠️ **COMPLIANCE FLAG (noted by IT audit):** Tom was pasting borrower financial data from covenant packages directly into ChatGPT. This includes DSCR, revenue figures, leverage ratios, and in at least two cases, borrower names. This may violate the bank's data handling policy for confidential client information. Tom has been using a personal (non-enterprise) ChatGPT account with no data privacy protections. *See compliance policy section 4.2.*
>
> *(Analyst note: the data-handling breach maps to §1 / §2 / §5 / §6; §4.2 is the separate credit-language constraint the memo OUTPUT must also respect. This workflow trips both.)*

**Prompt (verbatim):**
```
You are helping a commercial banker draft an annual relationship review memorandum.

Borrower background: [paste my notes on the company]
Financial summary: [paste covenant package highlights]
Covenant history: [paste from my tracking sheet]
Recent communications: [paste notes from my call log]
My assessment: [write 2-3 sentences of what I actually think]

Draft a relationship review memo that covers:
1. Credit overview (one paragraph)
2. Business description (one paragraph — keep it factual)
3. Financial performance (use the numbers I provided)
4. Covenant compliance history
5. Key risks (based on what I've told you — don't make stuff up)
6. Recommended action

Write this in a professional banking tone. The audience is our Chief Credit Officer.
Do NOT make any credit recommendations beyond what I've explicitly stated in my assessment.
Flag anywhere you're uncertain or where I haven't given you enough information.
```

**How I use it:** I write my own 2-3 sentence assessment first — that's important, I don't let the AI decide what I think. Then I paste everything else in. Output is usually 70% usable but the structure is always right which saves a ton of time.

**Notable:** Crestwood memo I drafted this way came back from Marcus Chen with zero edits. He didn't know I used AI. Not sure if I should have told him. *(Analyst note: ties to §5 — "representing AI-generated content as independently authored.")*
