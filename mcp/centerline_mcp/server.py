"""MCP server (official SDK / FastMCP), launched via `uv run --with mcp`.

uv fetches the `mcp` SDK into an ephemeral env at launch (no manual install). This works on
BOTH surfaces because the server is spawned on the HOST Mac (where uv lives):
  - Claude Code: from the repo-root `.mcp.json`.
  - Claude Cowork: from `~/Library/Application Support/Claude/claude_desktop_config.json`, which
    Claude Desktop SDK-bridges into its sandboxed VM.

All tool logic + the §2.1/§5 guards live in core.py / guards.py (stdlib, SDK-free), so they are
unit-testable without the SDK and apply even on direct calls.
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP

from . import core

mcp = FastMCP("centerline")


@mcp.tool()
def get_borrower_dossier(borrower_name: str) -> dict:
    """Retrieve a borrower's dossier from the bank's data (profile + latest performance + memo
    presence). The internal credit rating is stripped (§2.1); watchlist/Special-Assets designation
    language is redacted; Special-Assets/litigation borrowers are halted (§5). covenant_status is
    returned as a factual field.
    """
    return core.get_borrower_dossier(borrower_name)


@mcp.tool()
def get_loan_performance(borrower_name: str, months: Optional[int] = None) -> dict:
    """Retrieve monthly loan-performance rows for a borrower. DSCR/leverage/revolver/covenant_status
    are returned as factual data; free-text notes have restricted designation language redacted (§2.1).
    """
    return core.get_loan_performance(borrower_name, months)


@mcp.tool()
def screen_and_finalize(text: str, requires_rm_review: bool = True) -> dict:
    """Screen a drafted artifact before presenting/sending it (the cross-surface OUTPUT guard).

    Scans for §4.2 credit-characterizing/predictive/recommending language (blocks if found — the RM owns the
    credit judgment), attaches a deterministic reliability footer (label + reasons, never a numeric %), and
    tags the output for RM review (§4.3). Route ALL generated artifacts (briefs, digests, emails, memos,
    readouts) through this before they leave.
    """
    return core.screen_and_finalize(text, requires_rm_review=requires_rm_review)


@mcp.tool()
def get_activity_log(borrower_name: str, limit: Optional[int] = None) -> dict:
    """Retrieve a borrower's CRM contact log (entries). Free-text raw_notes have restricted designation
    language redacted (§2.1); Special-Assets/litigation borrowers are halted (§5)."""
    return core.get_activity_log(borrower_name, limit)


@mcp.tool()
def get_emails(borrower_name: str) -> dict:
    """Retrieve a borrower's email thread. Watchlist/Special-Assets designation language is redacted (§2.1);
    Special-Assets/litigation borrowers are halted (§5)."""
    return core.get_emails(borrower_name)


@mcp.tool()
def check_covenant_compliance(borrower_name: str) -> dict:
    """Deterministic covenant test (latest month): DSCR/leverage vs the borrower's covenant thresholds,
    cushion/headroom, breach flags, and whether the reported covenant_status matches the computed result.
    Returns facts only — the RM owns any credit judgment (§4.2). Construction loans return applicable=false."""
    return core.check_covenant_compliance(borrower_name)


@mcp.tool()
def detect_deterioration_signals(borrower_name: str, revolver_alert_pct: float = 75.0) -> dict:
    """Deterministic deterioration signals over the full history: DSCR/revolver trends, threshold crossings,
    the status-vs-trend mislabel, thin cushion, and construction lifecycle signals (pre-leasing vs 75%).
    Facts only — no creditworthiness characterization (§4.2)."""
    return core.detect_deterioration_signals(borrower_name, revolver_alert_pct)


@mcp.tool()
def measure_engagement_coverage(borrower_name: str) -> dict:
    """Deterministic engagement gap: days since the last SUBSTANTIVE two-way contact (a one-way notice /
    email-sent / missed call / internal prep does NOT count), vs the naive days-since-any-entry. Surfaces
    where engagement has thinned — especially silence during distress. Facts only (§4.2); RM-private."""
    return core.measure_engagement_coverage(borrower_name)


@mcp.tool()
def assemble_watchlist(borrowers: Optional[list] = None) -> dict:
    """Portfolio triage: compose covenant compliance + deterioration signals + engagement gap across borrowers,
    ranked by risk × neglect (facts-derived order, NOT a credit rating). RM-private; automated alerting needs
    CCO approval (§4.1). Facts only (§4.2)."""
    return core.assemble_watchlist(borrowers)


def main():
    mcp.run()  # stdio transport by default


if __name__ == "__main__":
    main()
