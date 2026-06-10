# Running a local MCP server in Claude Code vs Claude Cowork — what we learned

*(Engagement learnings, 2026-06-09. The `centerline` local stdio MCP server, getting it to work on
both surfaces.)*

## TL;DR
- **Claude Code** loads a project's **root `.mcp.json`** and launches local stdio MCP servers natively.
- **Claude Cowork** runs the agent in a **sandboxed Linux VM** and does **NOT** read a project `.mcp.json`.
  A local stdio server (a child process on the host) can't connect to the VM directly.
- To use a local stdio server in **Cowork**, register it in the **Claude Desktop** config:
  **`~/Library/Application Support/Claude/claude_desktop_config.json`**. Claude Desktop **SDK-bridges** it
  into the Cowork VM — it shows up as `"type": "sdk"`. **Restart Cowork** and start a **new task** to pick it up.

## Why it behaves this way
- Cowork's VM is sandboxed → no access to host child processes spawned over stdio.
- `.mcp.json` is **Claude Code's** project config. Cowork uses the **Desktop** config plus its own built-in
  servers (`cowork`, `workspace`, `visualize`, `scheduled-tasks`, `plugins`, `skills`, …) and remote connectors.
- This was confirmed empirically: with only a repo `.mcp.json`, Cowork listed its built-in servers but **no
  `mcp__centerline__*`**; after adding the entry to `claude_desktop_config.json` and relaunching, the tools appeared.

## How we made it work in this repo
1. **Server uses the official SDK (FastMCP), launched via `uv` against a locked project.** Dependencies are
   declared in `pyproject.toml` and pinned in `uv.lock`; `uv run --project <repo>` provisions the reproducible
   env (the `mcp` SDK) at launch (cached after the first run). *(Journey note: we briefly
   made the server stdlib-only when we wrongly believed Cowork ran the server **inside** its VM — where the
   Mac `uv` doesn't exist. In fact the Desktop bridge **spawns the server on the host Mac**, so `uv` is
   available and FastMCP is the cleaner choice.)* `core.py`/`guards.py` stay SDK-free so tests need nothing installed.
2. **Absolute uv path.** Command is **`/opt/homebrew/bin/uv`** — GUI apps launch with a minimal PATH, so a
   bare `uv`/`python3` may not resolve. (Pre-warm `uv`'s cache once before a live demo so first launch is fast.)
3. **Code surface** — repo-root `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "centerline": {
         "type": "stdio",
         "command": "/opt/homebrew/bin/uv",
         "args": ["run", "--project", "${CLAUDE_PROJECT_DIR}", "python", "-m", "centerline_mcp.server"],
         "env": {
           "PYTHONPATH": "${CLAUDE_PROJECT_DIR}/mcp",
           "CENTERLINE_DATA_DIR": "${CLAUDE_PROJECT_DIR}/data"
         }
       }
     }
   }
   ```
4. **Cowork surface** — `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "centerline": {
         "command": "/opt/homebrew/bin/uv",
         "args": ["run", "--project", "/Users/.../centerline-claude-pilot", "python", "-m", "centerline_mcp.server"],
         "env": {
           "PYTHONPATH": "/Users/.../centerline-claude-pilot/mcp",
           "CENTERLINE_DATA_DIR": "/Users/.../centerline-claude-pilot/data"
         }
       }
     }
   }
   ```
   **Use ABSOLUTE paths here** — the Desktop config is global, so `${CLAUDE_PROJECT_DIR}` does **not** resolve.

## Gotchas
- **Restart + new task.** Cowork reads the Desktop config only at startup, and a *resumed* conversation keeps
  its original tool set. After editing: fully quit Cowork (Cmd-Q), reopen, start a **New task**.
- **Absolute paths in the Desktop config** (no `${CLAUDE_PROJECT_DIR}`).
- **`${CLAUDE_PROJECT_DIR}` is NOT substituted under `--mcp-config` / `--strict-mcp-config`** in Claude Code
  (only under plain auto-load). Symptom: `-32000` + `ModuleNotFoundError: No module named 'centerline_mcp'`
  (PYTHONPATH stayed literal). Fix: use **absolute paths in `.mcp.json`** — works in both strict and auto-load
  modes. To launch Code with ONLY this server: `claude --strict-mcp-config --mcp-config .mcp.json
  --setting-sources project` (run from the repo root).
- **Cowork loads NONE of the project's `.claude/` (verified 2026-06-09):** not `.mcp.json`, not
  `.claude/skills/`, not `.claude/settings.json` hooks. It loads only the **bridged MCP server** + file access
  + globally-installed plugins/skills. ⇒ The skill library + hooks run in **Claude Code**; to run them on the
  Cowork surface, package them as an **installed plugin** (verify first).
- **MCP is not a hard chokepoint in Cowork, and project hooks can't backstop it there.** The Cowork agent has
  file/bash tools and can read raw `data/` directly, bypassing the §2.1 strip — and since project hooks don't
  fire in Cowork, §2.1 on this surface relies on the **MCP server path** (guards also live in `core.py`) plus,
  for full coverage, the plugin route. (In **Claude Code**, project hooks *do* fire and enforce §2.1.)
- **Community-discovered.** The SDK-bridge route is not fully official documentation — behavior may change as
  Cowork (a research preview) evolves. **Back up `claude_desktop_config.json` before editing.**
- **Production alternative.** For a deployed setup, use a **remote/HTTP MCP connector** (Cowork supports
  remote connectors); local stdio is a dev/demo convenience.

## Sources
- [How We Got Local MCP Servers Working in Claude Cowork (dev.to)](https://dev.to/murat-a-a/how-we-got-local-mcp-servers-working-in-claude-cowork-the-missing-guide-nbc)
- [Getting Started with Local MCP Servers on Claude Desktop (Claude Help Center)](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Connect to local MCP servers (Model Context Protocol)](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
