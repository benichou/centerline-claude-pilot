---
source: centerline-bank/data/tom_shadow_workflows.pdf
workflow: 3
name: Client Email Drafts
architecture: single-turn prompt with structured situation/context/tone/points fields
self_reported_quality: good first draft for routine notices; NOT for bad-news/credit-status emails (Tom writes those himself)
compliance_flag: "Borrower-facing → §4.3 (RM review before sending). Personal-account use is the §1 breach."
restricted_fields: []
---

# Workflow 3 — Client Email Drafts

Simple one. I describe what I need to say and it drafts the email. Most useful for:
- Covenant package overdue notices (I hate writing these — they always sound either too harsh or too soft)
- Draw request missing doc requests
- Renewal preliminary conversations

**Prompt (verbatim):**
```
Draft a professional email from a commercial banker to a client.

Situation: [describe what happened and what I need to communicate]
Relationship context: [how long we've known them, current relationship health]
Tone goal: [firm but respectful / warm and relationship-focused / etc.]
Key points to include: [list them]
Key things to avoid: [anything I don't want to say]

Keep it under 200 words. Use a professional but not stiff tone.
```

**Works great for:** Overdue notices, draw documentation requests, renewal openers.
**Doesn't work well for:** Anything involving bad news about credit status — I always write those myself.
