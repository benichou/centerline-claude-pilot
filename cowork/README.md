# cowork/ — Cowork sanity & alignment

## Why this folder exists
Claude **Cowork** runs the agent in a **sandboxed Linux VM** and **does not read this repo's `.mcp.json`**
(and may not load our project `.claude/` skills/hooks). It uses its own configuration — the local MCP server
is **bridged in** via `~/Library/Application Support/Claude/claude_desktop_config.json`, and Cowork reads that
config (and its session toolset) **at startup**.

Because Cowork's config and session state live **outside this repo**, it's easy for Cowork to **drift** from
what the repo actually defines:
- a stale `claude_desktop_config.json` (edited but Cowork not relaunched),
- a **resumed conversation** that keeps an old toolset,
- project skills/hooks that Cowork may or may not load.

So this folder holds the **standard checks we run inside Cowork after any change**, so the **RM-facing demo
surface stays aligned with the repo** (the MCP tools are present, project skills load, hooks fire).

## What's here
- **[`verification.md`](./verification.md)** — the exact relaunch steps + the prompts to paste into a Cowork
  session, and how to read the results.
- **Setup + the "why Cowork ≠ `.mcp.json`" learnings:** [`../docs/mcp_local_cowork.md`](../docs/mcp_local_cowork.md).

## When to run the checks
- After changing the MCP server, `.mcp.json`, or `claude_desktop_config.json`.
- After adding/renaming skills or hooks.
- Before any demo or dry-run.

## The golden rule
Cowork reads its config **only at startup**, and a **resumed conversation keeps its old toolset**. So always
**fully quit Cowork (Cmd-Q), reopen, open the project, and start a NEW task** before verifying — otherwise
you're testing a stale session, not the current repo state.
