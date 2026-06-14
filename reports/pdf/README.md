# reports/pdf/ — rendered artifact PDFs

Credit-file-grade PDFs produced by the `render_pdf` MCP tool from **screened** artifacts (the
`finalized_text` returned by `screen_and_finalize`) — so each one keeps its **DRAFT / "Requires RM
review" (§4.3)** banner and its **reliability footer**.

- **Versioned, not ignored.** This folder is tracked in git (unlike `traces/`), so rendered artifacts are
  part of the audit trail / demo record.
- **Filenames are UTC-timestamped** (`<name>_YYYYMMDDTHHMMSSZ.pdf`) — each render is a unique, sortable
  file; nothing is overwritten.
- **Generated, not hand-authored.** Re-running a review regenerates a new timestamped PDF here. Prune old
  ones as you like; this README keeps the folder present.

Produced cross-surface (the MCP server runs on the host in both Claude Code and Cowork). The source-of-
truth markdown still renders inline in the session; the PDF is an additional, fileable copy.
