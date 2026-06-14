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
def screen_and_finalize(
    text: str,
    requires_rm_review: bool = True,
    low_confidence_inputs: list = None,
    cross_source_mismatches: list = None,
) -> dict:
    """Screen a drafted artifact before presenting/sending it (the cross-surface OUTPUT guard).

    Scans for §4.2 credit-characterizing/predictive/recommending language (blocks if found — the RM owns the
    credit judgment), attaches a deterministic reliability footer (label + reasons, never a numeric %), and
    tags the output for RM review (§4.3). Route ALL generated artifacts (briefs, digests, emails, memos,
    readouts) through this before they leave.

    For an HONEST footer, pass `cross_source_mismatches` (e.g. the list from cross_validate_covenant) and
    `low_confidence_inputs` (e.g. from review_package — missing docs, unsigned letter, withheld names): with
    either present the footer reads **Partial** with reasons, instead of a false "Grounded · 0 issues".
    """
    return core.screen_and_finalize(
        text,
        low_confidence_inputs=low_confidence_inputs,
        cross_source_mismatches=cross_source_mismatches,
        requires_rm_review=requires_rm_review,
    )


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
def get_relationship_timeline(borrower_name: str) -> dict:
    """Merge the CRM activity log + the email thread into ONE source-tagged, chronological timeline so the
    RM can reconcile the system of record against the actual correspondence — mis-dated / conflated log
    entries (a log row dated before the emails it summarizes) and decisions that live only in email surface
    immediately. Each event = {date, source, who, kind, summary, ref}. §2.1-redacted, §5-gated, facts only
    (§4.2). Use for "reconcile X's emails vs the log — what happened, what's mis-dated, what's only in email?"
    """
    return core.get_relationship_timeline(borrower_name)


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


@mcp.tool()
def flag_renewal_and_retention(borrower_name: str) -> dict:
    """Proactive renewal/retention radar — the INVERSE of the early-warning watchlist. Fires when a
    borrower is HEALTHY *and* approaching renewal / being courted by a competitor / has renewal activity on
    record — the attrition risk distress-monitoring is structurally blind to (e.g. Crestwood: pristine
    metrics, but a competitor term sheet on the table and the renewal stalling). Surfaces the maturity
    clock, health & trend, the competitive signal, and relationship value as FACTS (§4.2) and flags that
    the RM should ENGAGE — it NEVER recommends a rate/price (pricing committee owns that). §4.1: automated
    alerting needs CCO approval. Use for "who am I about to lose?" / "prep me for <healthy borrower>"."""
    return core.flag_renewal_and_retention(borrower_name)


@mcp.tool()
def run_evals() -> dict:
    """Run the golden-set evaluation suite against the live tool logic and refresh the observability report.

    Use when asked to "run the evals", "check accuracy", "prove the numbers", or "show the scorecard".
    Grades source-grounded ground-truth cases (T1: e.g. Meridian DSCR 1.03/breach, the 78-day gap) and
    binary compliance assertions (T2: §2.1 strip, §5 halt, guarantor refusal, §4.2 block) — plus negative
    cases. The grader is deterministic Python (NO LLM), calling the same code the demo uses. Also regenerates
    reports/observability.md. Returns pass/fail totals, per-prompt and per-tier breakdowns, and any failures."""
    return core.run_evals()


@mcp.tool()
def get_latest_report(kind: str = "improvements", pull: bool = True) -> dict:
    """Fetch the latest eval/improvement report, refreshing from git FIRST so you always get the newest.

    Use when asked to show the latest proposed improvements / eval results / scorecard. Runs a read-only
    `git pull --rebase` host-side (NEVER commits/pushes, NEVER the GitHub API), then returns the report
    CONTENT — so it's current even in Cowork (whose file view can lag). kind: 'improvements' (proposed skill
    changes), 'agent_eval' (the agent-behavior eval), or 'observability' (deterministic scorecards)."""
    return core.get_latest_report(kind, pull)


@mcp.tool()
def list_documents(directory: str) -> dict:
    """List the files in a package directory HOST-SIDE — use this FIRST to enumerate a covenant package
    instead of guessing filenames or listing from the sandbox (which would trigger a Cowork folder-access
    prompt). The server runs on the host in both Code and Cowork, so it reads the real directory. `directory`
    is repo-relative (e.g. data/synthetic/meridian-package) or absolute. Returns {count, files, pdfs};
    classify each entry in `pdfs` next. Deterministic (no API)."""
    from . import docintel

    return docintel.list_documents(directory)


@mcp.tool()
def classify_document(path: str) -> dict:
    """Classify one covenant-package document (PDF) into a document type. Runs the §2.1 pre-screen first — a
    guarantor personal financial statement is refused on intake and NEVER sent to a model. Otherwise calls the
    Anthropic API (temp 0, Pydantic-forced schema) and returns {doc_type, confidence, rationale, key_signals,
    is_restricted_personal_guarantor_info}. `path` is the PDF path (absolute, or relative to the repo)."""
    from . import docintel

    return docintel.classify_document(path)


@mcp.tool()
def extract_document_fields(path: str, doc_type: str) -> dict:
    """Extract structured fields from a classified document, using the per-type schema. `other` (and
    purchase_order/financial_projections) are skipped (no schema); a guarantor personal financial statement is
    refused (§2.1). Otherwise returns the validated extracted fields for the type. Call classify_document first
    to get `doc_type`."""
    from . import docintel

    return docintel.extract_document_fields(path, doc_type)


@mcp.tool()
def cross_validate_covenant(certificate: dict, financials: dict, borrower: str = "Meridian Fabrication") -> dict:
    """Reconcile a covenant certificate's CERTIFIED ratios against the RECOMPUTED ratios from the attached
    unadjusted (GAAP) financials AND the bank's own loan_performance. Surfaces the EBITDA add-back bridge
    that drives any gap and flags — as a factual covenant-test result (§4.2) — where the certified figure
    clears a threshold the recomputed figure does not. EVERY figure is provenance-tagged (document + field
    + value; the bank figure to the deriving tool) and each finding carries its `sources` — assert nothing
    untraceable (the RM was burned by an unreliable AI). Also returns `cross_source_mismatches` — pass it to
    `screen_and_finalize` so the reliability footer is honest. Pass the `extracted` dicts from
    extract_document_fields for the certificate and the financial statement. Deterministic (no API)."""
    from . import package_review

    return package_review.cross_validate_covenant(certificate, financials, borrower)


@mcp.tool()
def review_package(items: list, borrower: str = "Meridian Fabrication") -> dict:
    """Intake summary for a classified+extracted covenant package: completeness (required vs received →
    missing documents + outstanding data elements), quality flags (unsigned rep letter, withheld A/R
    names) — each tagged with its source document + field + value — and the §2.1 refusals. `items` = list
    of classify/extract result dicts ({doc_type, path?, extracted?, refused?, skipped?}). Also returns
    `low_confidence_inputs` — pass it to `screen_and_finalize` so the reliability footer reflects the
    package's gaps. Facts only (§4.2). Deterministic (no API)."""
    from . import package_review

    return package_review.review_package(items, borrower)


@mcp.tool()
def render_pdf(text: str, title: str = None, output_path: str = None, timestamp: bool = True) -> dict:
    """Render a SCREENED artifact (markdown) to a credit-file-grade PDF, host-side (works in Code AND
    Cowork). Pass the `finalized_text` from screen_and_finalize so the DRAFT / "Requires RM review" banner
    and the reliability footer are preserved in the PDF. This is an ADDITIONAL output — the markdown
    artifact is unchanged and still renders inline. Renders a small markdown subset (headings, bold/italic,
    bullet/numbered lists, GFM tables, rules). `output_path` is repo-relative (default reports/pdf/); a UTC
    timestamp is appended so each save is a unique, sortable file (timestamp=False writes the exact name).
    Returns {ok, path, bytes}. Deterministic (no API)."""
    from . import pdf_render

    return pdf_render.render_pdf(text, title=title, output_path=output_path, timestamp=timestamp)


def main():
    mcp.run()  # stdio transport by default


if __name__ == "__main__":
    main()
