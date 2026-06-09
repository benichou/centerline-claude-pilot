---
source: centerline-bank/data/tom_shadow_workflows.pdf
workflow: 1
name: Draw Request Response Letter
architecture: single-turn prompt (paste draw request + notes)
self_reported_quality: 85% usable; 45 min → ~10 min editing
compliance_flag: none
restricted_fields: []
---

# Workflow 1 — Draw Request Response Letter

This one took me about 3 weeks to get right. I paste in the draw request details and it drafts the formal response including the missing docs checklist. I then edit it — maybe 10 minutes of cleanup vs. 45 minutes of writing from scratch.

**Prompt (verbatim):**
```
You are a commercial real estate lending officer at a regional bank.
Draft a professional letter responding to a construction loan draw request.

Draw details: [paste draw request summary]
Missing documentation: [list what's missing]
Project status: [paste from my notes]

The letter should:
- Acknowledge receipt of the draw request
- List specifically what documentation is still needed before funding
- Give a realistic timeline for funding once docs are received
- Be professional but direct — we have a good relationship with this borrower
- Not make any promises about approval

Use formal business letter format. Keep it under 300 words.
```

**How I use it:** Copy the draw request email, pull my notes on what's missing, paste both into the prompt. Takes about 5 minutes total. Output is 85% usable, I always review and adjust.

**What I edit:** Anything that sounds too stiff or legal. I want it to sound like me.
