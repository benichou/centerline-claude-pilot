# Hooks in Claude Code vs Claude Cowork — what we learned

## TL;DR
- **Hooks fire in Claude CODE** (project `.claude/settings.json` and plugin `hooks/hooks.json`). Verified: a
  `PreToolUse` hook fired on every tool use (5× in one session).
- **Hooks do NOT fire in Claude COWORK — at ANY scope:** user, project, plugin, *and even
  enterprise-managed/MDM*. Confirmed empirically (two probes) and by tracked bugs. It's a platform/sandbox
  limitation, **not** a misconfiguration.

## Evidence
- **Empirical:** a project `.claude/settings.json` hook and a plugin `hooks/hooks.json` hook (both `.*`
  `PreToolUse`) — **neither fired in Cowork**; both fire in Code.
- **Tracked issues (anthropics/claude-code):**
  - [#27398](https://github.com/anthropics/claude-code/issues/27398) — plugin hooks excluded in Cowork (it spawns the CLI with `--setting-sources user`).
  - [#40495](https://github.com/anthropics/claude-code/issues/40495) — the Cowork sandbox ignores **all** settings sources (user **+ managed/MDM** + env); it looks for a `cowork_settings.json` that doesn't exist, so resolution silently returns empty.
  - [#47993](https://github.com/anthropics/claude-code/issues/47993) — SessionStart hooks don't fire in Cowork.
- The same reports confirm **MCP loads** (passed via `--mcp-config`) and **skills load** (via `--plugin-dir`)
  in Cowork — **only the hook/settings layer is broken.**

## What this means for our architecture
- **Don't depend on hooks for cross-surface enforcement.** Put deterministic guard logic in the
  **MCP server tools** (run on both surfaces) and **skill scripts**, and route generated artifacts through a
  **`screen_and_finalize` MCP tool** (§4.2 language scan + grounding + reliability footer).
- **§2.1 strip · §5 gate · guarantor refusal** already live in the MCP server → enforced on both surfaces.
- **§4.3 human review** on Cowork = its **native approval** prompts ("Needs approval" / "Allow Claude to…").
- **Hooks = a Code-only deterministic "belt"** — most valuable for the **run-ledger / observability trace**
  and for **backstopping the MCP guards** (e.g., blocking a raw-file read of a restricted field) on the Code
  surface. Honest limit: no surface (hook or otherwise) can deterministically scan the model's *free-form
  chat reply* — hooks only see *tool* I/O — so §4.2 = model behavior + artifact screening + human review.

## Related
- MCP setup + the Cowork bridge: [`mcp_local_cowork.md`](./mcp_local_cowork.md)
- Cowork verification runbook: [`../cowork/`](../cowork/README.md)
