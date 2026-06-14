# BUILD — local setup & how to run

## Requirements
- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — manages the environment and launches the MCP server.
  Dependencies are declared in **`pyproject.toml`** and pinned in **`uv.lock`** (reproducible); the server
  uses the official MCP SDK (**FastMCP**). `uv run --project <repo>` provisions the locked env automatically
  — **no manual `pip install`** (uv creates a gitignored `.venv/`).

## Run the deterministic guard/core tests (no SDK needed — pure stdlib)
```bash
PYTHONPATH=mcp python3 mcp/tests/test_compliance.py
```
`core.py` / `guards.py` are SDK-free, so the §2.1 strip / redaction / §5 gate / guarantor-refusal /
covenant_status checks (11) run with a plain `python3`.

## Run the doc-intel tests (needs the uv env — pydantic / jinja2 / pyyaml; NO Anthropic API call)
```bash
PYTHONPATH=mcp uv run python mcp/tests/test_docintel.py
```
Covers the deterministic, model-independent parts of `docintel.py`: the §2.1 pre-screen, the
`other`/guarantor/unknown extract short-circuits, the schema↔prompt wiring, and Pydantic validation.
The LIVE `classify_document` / `extract_document_fields` calls (which spend tokens) are run by hand on
the real `data/synthetic/meridian-package/` PDFs — they read `ANTHROPIC_API_KEY` from the environment.

## Linting & formatting (black + flake8, via pre-commit, uv-native)
Dev tools are pinned in `uv.lock` (the `dev` dependency group), so everyone runs the same versions.
**black** owns formatting (line-length 120); **flake8** lints real issues (it defers line-length to black —
see `.flake8`). Pre-commit runs them via `uv run` (config in `.pre-commit-config.yaml`).
```bash
uv run pre-commit install          # one-time: install the git hook (runs on every commit)
uv run pre-commit run --all-files  # run all hooks now
uv run black .                     # format
uv run flake8 .                    # lint
```
First commit after `pre-commit install`: if a hygiene hook (trailing-whitespace / end-of-file-fixer)
auto-fixes a file, the commit aborts with the fix applied — just `git add -u` and re-commit. `data/` and
`reference/` (the synthetic corpus) are excluded from formatting.

## Smoke-test the MCP server (FastMCP via uv)
```bash
PYTHONPATH=mcp CENTERLINE_DATA_DIR=$(pwd)/data \
  /opt/homebrew/bin/uv run --project $(pwd) python -m centerline_mcp.server
```
Speaks MCP over stdio (normally launched by the client). To regenerate the lock after changing deps: `uv lock`.

## Use it in Claude Code / Cowork
- **Claude Code:** `.mcp.json` (repo ROOT) registers `centerline`, launched via
  `/opt/homebrew/bin/uv run --project ${CLAUDE_PROJECT_DIR} python -m centerline_mcp.server`
  (`PYTHONPATH=${CLAUDE_PROJECT_DIR}/mcp`, `CENTERLINE_DATA_DIR=${CLAUDE_PROJECT_DIR}/data`). Registers as
  `mcp__centerline__*`.
- **Claude Cowork:** does **not** read `.mcp.json` (sandboxed VM). The server is registered in
  `~/Library/Application Support/Claude/claude_desktop_config.json` (same `uv run --project <abs repo>`
  command, **absolute** paths); Claude Desktop spawns it on the host and SDK-bridges it into the VM.
  Full how-to + gotchas: **[`docs/mcp_local_cowork.md`](./docs/mcp_local_cowork.md)**.

> The absolute `/opt/homebrew/bin/uv` path is used because GUI apps launch with a minimal PATH. First launch
> resolves the locked env (then cached) — pre-warm with the smoke test above before a live demo.

## What the server serves
Only `data/` (structured CSVs · email threads · input memo · synthetic/). `reference/` (policy, personas,
shadow-workflows) is **never** served. Compliance guards (§2.1 strip, §5 gate, guarantor refusal) live in
`centerline_mcp/guards.py` + `core.py` (so they apply even on direct calls).

## Tools (Phase 1)
- `get_borrower_dossier(borrower_name)` — profile + latest performance + memo presence
- `get_loan_performance(borrower_name, months?)` — monthly rows (covenant_status kept)
