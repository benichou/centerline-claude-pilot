# reference/ — build guidance (NOT served by the MCP)

Material that informed **how we build**. The `centerline` MCP server does **not** serve any of it — none of
this is ever retrieved as borrower data. (Operational data lives in [`../data/`](../data/INDEX.md).)

| Path | What it is | How it's used |
|---|---|---|
| `compliance-policy/` (`00-purpose` … `08-escalation`) | the bank's AI-use policy — the § ruleset | the authority the **guardrail skills enforce deterministically + cite** (§2.1 / §4.1 / §4.2 / §4.3 / §5); never retrieved as data |
| `personas/` (sarah-okonkwo, tom-deluca, marcus-webb, adoption-spectrum, common-pain-points) | RM profiles + adoption guidance | shapes per-persona demo framing + skill design; never retrieved as data |
| `shadow-workflows/` (`00-setup`, `wf1`–`wf5`, `doesnt-work`, `wishlist`) | Tom's personal-ChatGPT workflows + the two compliance flags | the **spec for Deliverable A** (what to rebuild + fix); never retrieved as data |

> If a skill ever needs a policy §quote or a persona preference at runtime, we bake the minimal needed text
> into the skill or `CLAUDE.md` (or expose a narrow read-only tool) — we do **not** turn `reference/` into an
> MCP data source. That boundary is what keeps "build guidance" from leaking in as "borrower facts."
