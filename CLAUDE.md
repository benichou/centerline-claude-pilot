# CLAUDE.md — Centerline Claude Pilot

Project-level instructions for Claude Code / Cowork working in this repo. **These rules are always in effect and override default behavior.**

## What this is
A Forward-Deployed-Engineer pilot: a composable Claude **skill library** for Centerline Bank's Commercial Banking division, demoed as two "tracks":
- **Track A — Portfolio Risk & Early-Warning** (compliant rebuild of an RM's shadow workflow; deterministic flags; RM-private).
- **Track B — Relationship Review & Renewal Prep + Document-Intelligence** (meeting prep, covenant-package intake, reconciliation/close-the-loop, memos, client communications).

Build in **Claude Code** → demo in **Claude Cowork** ("Work in a folder"). Retrieval is via the local **`centerline` MCP server** over `data/` only (`structured/` · `emails/` · `memos/` · `synthetic/`); `reference/` (policy, personas, shadow-workflows) is **not** served.

## Data rules
- **All data here is synthetic / fictional.** Never invent new credit facts about the five borrowers
  (Meridian, BlueLine, Crestwood, Summit, Arcadia). Synthetic documents encode facts/directions already
  present in the data and live under `data/synthetic/`, clearly labeled.
- Nothing organization-internal and **no real credentials** ever enter this repo.

## Compliance guardrails (designed in — not disclaimers)
Reference the bank's AI policy sections (§). When working here, Claude MUST:
- **§2.1 — restricted inputs.** Never ingest internal credit ratings, watchlist, or Special-Assets
  designations, or **guarantor personal financials**. These are stripped server-side in the MCP; a
  guarantor personal-financial document must be **refused, not read**.
- **§4.2 — no credit-adjacent language.** Never characterize creditworthiness or generate anything
  readable as a credit decision (no "high risk", "likely to breach", "elevated risk"). **State facts;
  the credit judgment originates with the RM.** When surfacing a human's credit decision act as a
  **scribe** — quote it verbatim, attributed, with provenance — never paraphrase it into AI risk language.
- **§5 — prohibited borrowers.** No AI processing for any borrower in Special Assets or active litigation (the MCP gate stops these).
- **§4.3 — human review.** Any borrower-facing message or credit-file content requires RM review before it leaves; CRM enrichment is **proposed only**, written **after** RM approval.
- **§4.1 — monitoring.** Automated monitoring/alerting is presented as "designed, pending CCO approval," never as launched.

## Quality rules
- **Ground every claim to a source** (`file:row` / `doc:page` / email line). If a claim can't be cited, flag it as UNVERIFIED — do not assert it.
- **Do the math deterministically** — ratios, trends, gaps run in bundled scripts, not the model.
- Attach the **reliability footer** (`assessing-output-reliability`) to every artifact: a qualitative label + reasons (uncited claims, low-confidence inputs, cross-source agreement, completeness) — **never a numeric % ** (a percentage is mis-calibrated and reads as credit risk).
- Outputs are **file artifacts** written into the folder.

## Repo conventions
- Skills: `.claude/skills/<name>/SKILL.md` (+ optional `reference/`, `scripts/`)
- Sub-agents: `.claude/agents/<name>.md` (only for fan-out or headless/scheduled work; never wrap an interactive human-in-the-loop pause inside a sub-agent)
- Hooks: `.claude/settings.json` (`"hooks"` key) — deterministic guards, defense-in-depth with the MCP
- Local MCP: `.mcp.json` at repo root
