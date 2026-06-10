# Cowork verification runbook

Run these inside **Claude Cowork** to confirm it's aligned with the repo (MCP bridged, project skills load,
hooks fire). See [`README.md`](./README.md) for *why*, and [`../docs/mcp_local_cowork.md`](../docs/mcp_local_cowork.md)
for one-time setup.

## 0. Always relaunch first (the golden rule)
Cowork reads `claude_desktop_config.json` + project config **only at startup**, and a resumed task keeps its
old toolset.

1. **Quit Cowork completely: Cmd-Q.**
2. Reopen Cowork.
3. Open the **centerline-claude-pilot** project (Projects → Use an existing folder, if not already there).
4. Click **➕ New task** (do **not** resume an old conversation).

## 1. The 3-in-1 check — paste into the new task
```
Three checks for this project — report each explicitly:
1. MCP — List any tools named mcp__centerline__*. If present, call get_borrower_dossier for
   Meridian and tell me whether credit_grade is absent and what the covenant_status is.
2. SKILLS — Is there a project skill named test-marker? If yes, invoke it and paste its exact output token.
3. HOOKS — Run a trivial shell command (e.g. echo hi), then read the file .claude/hook-probe.log
   and show its contents (or say it doesn't exist).
```

## 2. How to read the result
| Check | ✅ Aligned | ❌ Drifted / not loaded |
|---|---|---|
| **MCP** | `mcp__centerline__get_borrower_dossier` + `get_loan_performance` listed; call returns **`credit_grade` absent** + **`covenant_status` = "Covenant Breach"** | no `mcp__centerline__*` tools |
| **SKILLS** | `test-marker` listed + outputs `TEST-MARKER-SKILL-LOADED-7F3A` | skill not found |
| **HOOKS** | `.claude/hook-probe.log` contains a `HOOK-FIRED-9B2E …` line | file missing |

## Result of the first run (2026-06-09)
- **MCP ✅** — `mcp__centerline__*` available; call stripped `credit_grade`, `covenant_status` = "Covenant Breach".
- **SKILLS ❌** — Cowork does **not** auto-load project `.claude/skills/` (only globally-installed/plugin skills).
- **HOOKS ❌** — project `.claude/settings.json` hooks do **not** fire in Cowork.
→ **Conclusion:** Cowork (folder-mode) loads **only** the bridged MCP server + file access from this repo —
not the project's `.claude/` skills or hooks. The full skill library + hooks run in **Claude Code**; to run
them on the Cowork surface they must be packaged as an **installed plugin** (to be verified). On Cowork,
§2.1 therefore rests on the **MCP server chokepoint**, not project hooks.

## 3. Troubleshooting
- **No `mcp__centerline__*`:** check `~/Library/Application Support/Claude/claude_desktop_config.json` has the
  `centerline` entry (absolute `/opt/homebrew/bin/uv` + `run --project <abs repo>` + absolute
  `PYTHONPATH`/`CENTERLINE_DATA_DIR`); confirm you **fully relaunched** and started a **NEW task**. First launch
  resolves the uv/locked env (then cached) — pre-warm with the smoke test in `BUILD.md` before a demo.
- **Skills/hooks missing:** Cowork may not load project `.claude/` constructs. That's a *finding*, not a fix —
  note it; on the Cowork surface, §2.1 then can't rely on project hooks and must be enforced another way
  (e.g., via the MCP server path + `CLAUDE.md` guidance).

## 4. Note on the probe artifacts
`test-marker` (skill) and the `.claude/settings.json` hook + `.claude/hook-probe.log` are **temporary loading
probes**. Once we've confirmed Cowork's loading behavior, the probe skill/hook are removed and replaced with
the real Phase-1 foundation skills + guard hooks.
