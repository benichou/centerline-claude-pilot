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
   Meridian and tell me whether credit_grade is absent and what the covenant_status is; then call
   assemble_watchlist and give me the borrower order.
2. SKILLS — Do you see plugin skills from the "centerline" plugin (e.g. assessing-output-reliability,
   measuring-engagement-coverage)? List the ones you can see.
3. HOOKS — Run a trivial shell command (e.g. echo hi). (Expected: no project hook fires in Cowork.)
```

> **SKILLS prerequisite:** check #2 only passes if `centerline-plugin.zip` is installed in Cowork via
> **Customize → Personal plugins → Upload plugin**. Project `.claude/skills/` are NOT auto-loaded in
> Cowork — the plugin is the only route. (The earlier `test-marker` probe skill was removed once this
> was confirmed.)

## 2. How to read the result
| Check | ✅ Aligned | ❌ Drifted / not loaded |
|---|---|---|
| **MCP** | `mcp__centerline__get_borrower_dossier` + 8 more listed; call returns **`credit_grade` absent** + **`covenant_status` = "Covenant Breach"**; watchlist order **Meridian → BlueLine → Summit → Arcadia → Crestwood** | no `mcp__centerline__*` tools |
| **SKILLS** | the 11 `centerline:*` plugin skills are listed (requires the uploaded plugin) | no `centerline:*` skills found → plugin not installed |
| **HOOKS** | none fires — **expected** (Cowork sandbox ignores project `.claude/settings.json` hooks; this is the known finding, not a failure) | (n/a — absence is the pass condition) |

## Result of the first run (2026-06-09)
- **MCP ✅** — `mcp__centerline__*` available; call stripped `credit_grade`, `covenant_status` = "Covenant Breach".
- **SKILLS ❌** — Cowork does **not** auto-load project `.claude/skills/` (only globally-installed/plugin skills).
- **HOOKS ❌** — project `.claude/settings.json` hooks do **not** fire in Cowork.
→ **Conclusion:** Cowork (folder-mode) loads **only** the bridged MCP server + file access from this repo —
not the project's `.claude/` skills or hooks. The full skill library + hooks run in **Claude Code**; to run
them on the Cowork surface they must be packaged as an **installed plugin**. On Cowork,
§2.1 therefore rests on the **MCP server chokepoint**, not project hooks.

## Update (2026-06-12) — plugin route confirmed
With `centerline-plugin.zip` uploaded (Customize → Personal plugins): **SKILLS ✅** — all 11
`centerline:*` skills load in Cowork. **HOOKS still ❌ by design** (the sandbox never fires project
hooks — confirmed). So the verified cross-surface picture is: **MCP = both surfaces · skills = both
(via the installed plugin) · hooks = Code-only · §2.1/§4.2 enforced server-side in the MCP.**

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
