"""Tool logic (pure Python, no MCP dependency) — so it's directly unit-testable.

Every borrower-facing read passes through the §2.1 / §5 guards before returning.
covenant_status is a FACTUAL field and is preserved (decided 2026-06-09).
"""
from . import data_access as da
from . import guards


def _not_found(borrower_name):
    return {"error": f"borrower not found: {borrower_name}", "known_borrowers": da.list_borrowers()}


def get_borrower_dossier(borrower_name):
    """A borrower dossier from data/ — §2.1 stripped, §5 gated, with a compliance log."""
    log = []
    rows = da.match_borrower(borrower_name, da.portfolio())
    if not rows:
        return _not_found(borrower_name)
    profile_raw = rows[0]
    borrower = profile_raw["borrower_name"]

    guards.assert_processable(borrower, log=log)  # §5

    profile = guards.strip_record(profile_raw, free_text_fields=(), log=log)  # §2.1: credit_grade
    lp_rows = da.match_borrower(borrower, da.loan_performance())
    latest = guards.strip_record(lp_rows[-1], free_text_fields=("notes",), log=log) if lp_rows else None

    return {
        "borrower": borrower,
        "profile": profile,                         # credit_grade removed
        "latest_performance": latest,               # covenant_status kept; notes redacted
        "has_relationship_memo": da.memo_path_for(borrower) is not None,
        "_compliance": {"policy": ["§2.1", "§5"], "redactions": log},
    }


def get_loan_performance(borrower_name, months=None):
    """Monthly loan-performance rows — covenant_status preserved; notes redacted."""
    log = []
    rows = da.match_borrower(borrower_name, da.loan_performance())
    if not rows:
        return _not_found(borrower_name)
    borrower = rows[0]["borrower_name"]

    guards.assert_processable(borrower, log=log)  # §5

    if months:
        rows = rows[-int(months):]
    clean = [guards.strip_record(r, free_text_fields=("notes",), log=log) for r in rows]
    return {
        "borrower": borrower,
        "months": len(clean),
        "performance": clean,                       # covenant_status preserved
        "_compliance": {"policy": ["§2.1", "§5"], "redactions": log},
    }


import re as _re

# heuristic: does the text carry a source citation? — file:row, known data files, an as-of date, or a
# centerline MCP tool/provenance reference (outputs grounded in the deterministic tools cite those by name).
_CITATION_RE = _re.compile(
    r"(:L?\d+\b|\bL\d+\b|\(source:|loan_perf|activity_log|portfolio_ref|thread-\d|meridian-review"
    r"|\.csv\b|\.md\b|\.pdf\b|\bcenterline\b|\bmcp\b|as[\s\-]of|\b\d{4}-\d{2}\b"
    r"|check_covenant_compliance|detect_deterioration_signals|measure_engagement_coverage|assemble_watchlist"
    r"|get_borrower_dossier|get_loan_performance|get_activity_log|get_emails)",
    _re.IGNORECASE,
)


def screen_and_finalize(text, low_confidence_inputs=None, cross_source_mismatches=None, requires_rm_review=True):
    """Cross-surface OUTPUT guard (runs in Code AND Cowork via the MCP).

    Route every generated artifact through this before presenting/sending:
      - §4.2 scan for credit-characterizing/predictive/recommending language (block if found),
      - attach a deterministic reliability footer (label + reasons; NEVER a numeric %),
      - tag for RM review (§4.3).
    """
    low_confidence_inputs = low_confidence_inputs or []
    cross_source_mismatches = cross_source_mismatches or []

    violations = guards.scan_credit_language(text)
    has_citation = bool(_CITATION_RE.search(text or ""))

    reasons = []
    label = "Grounded"
    if violations:
        label = "BLOCKED (§4.2)"
        reasons.append(f"credit-adjacent language: {sorted(set(violations))}")
    if not has_citation:
        if label == "Grounded":
            label = "Unverified"
        reasons.append("no source citation detected")
    if low_confidence_inputs:
        if label == "Grounded":
            label = "Partial"
        reasons.append(f"{len(low_confidence_inputs)} low-confidence input(s)")
    if cross_source_mismatches:
        if label == "Grounded":
            label = "Partial"
        reasons.append(f"{len(cross_source_mismatches)} cross-source mismatch(es)")

    footer = f"Reliability: {label}" + (" · " + " · ".join(reasons) if reasons else " · 0 issues")
    blocked = bool(violations)
    finalized = None
    if not blocked:
        finalized = text.rstrip() + "\n\n---\n" + footer
        if requires_rm_review:
            finalized += "\n(Requires RM review before client/credit-file use — §4.3)"

    return {
        "ok": not blocked,
        "blocked": blocked,
        "violations": violations,
        "reliability": {"label": label, "reasons": reasons, "footer": footer},
        "finalized_text": finalized,
        "_compliance": {"policy": ["§4.2", "§4.3"], "scanned": True},
    }


def get_activity_log(borrower_name, limit=None):
    """CRM contact log for a borrower — §5 gated; free-text raw_notes have restricted designation language redacted (§2.1)."""
    log = []
    rows = da.match_borrower(borrower_name, da.activity_log())
    if not rows:
        return _not_found(borrower_name)
    borrower = rows[0]["borrower_name"]
    guards.assert_processable(borrower, log=log)
    if limit:
        rows = rows[-int(limit):]
    clean = [guards.strip_record(r, free_text_fields=("raw_notes",), log=log) for r in rows]
    return {
        "borrower": borrower,
        "entries": len(clean),
        "activity": clean,
        "_compliance": {"policy": ["§2.1", "§5"], "redactions": log},
    }


def get_emails(borrower_name):
    """Email thread for a borrower — §5 gated; watchlist/Special-Assets designation language redacted (§2.1)."""
    log = []
    pf = da.match_borrower(borrower_name, da.portfolio())
    borrower = pf[0]["borrower_name"] if pf else borrower_name
    guards.assert_processable(borrower, log=log)
    text = da.emails_for(borrower_name)
    if text is None:
        return {"error": f"no email thread: {borrower_name}", "known_borrowers": da.list_borrowers()}
    redacted, _ = guards.redact_text(text, log=log, field="emails")
    return {
        "borrower": borrower,
        "thread": redacted,
        "_compliance": {"policy": ["§2.1", "§5"], "redactions": log},
    }


# ---- Track A: deterministic portfolio-risk computations (facts only — the RM owns the credit judgment) ----

def _f(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _lp_rows(borrower_name):
    rows = da.match_borrower(borrower_name, da.loan_performance())
    rows.sort(key=lambda r: r.get("date", ""))
    return rows


def _is_construction(latest):
    return (latest.get("covenant_status", "").strip().lower() == "construction") or (
        _f(latest.get("covenant_dscr_min")) == 0 and _f(latest.get("covenant_leverage_max")) == 0
    )


def check_covenant_compliance(borrower_name):
    """Deterministic covenant test on the latest month: DSCR/leverage vs the borrower's own covenant
    thresholds, cushion/headroom, and whether the reported status matches the computed result. Facts only."""
    log = []
    rows = _lp_rows(borrower_name)
    if not rows:
        return _not_found(borrower_name)
    borrower = rows[0]["borrower_name"]
    guards.assert_processable(borrower, log=log)
    latest = rows[-1]
    comp = {"policy": ["§2.1", "§4.2", "§5"], "redactions": log, "note": "factual covenant computation; the RM owns the credit judgment"}

    if _is_construction(latest):
        return {"borrower": borrower, "as_of": latest["date"], "applicable": False,
                "reason": "Construction phase — operating DSCR/leverage covenants are not yet in effect; see detect_deterioration_signals for lifecycle signals.",
                "reported_status": latest.get("covenant_status"), "_compliance": comp}

    dscr, dscr_min = _f(latest.get("dscr_ttm")), _f(latest.get("covenant_dscr_min"))
    lev, lev_max = _f(latest.get("leverage_ratio")), _f(latest.get("covenant_leverage_max"))
    dscr_breach, lev_breach = dscr < dscr_min, lev > lev_max
    computed = "Covenant Breach" if (dscr_breach or lev_breach) else "Compliant"
    reported = latest.get("covenant_status", "")
    return {
        "borrower": borrower, "as_of": latest["date"],
        "dscr": {"value": dscr, "min": dscr_min, "cushion": round(dscr - dscr_min, 2), "breach": dscr_breach},
        "leverage": {"value": lev, "max": lev_max, "headroom": round(lev_max - lev, 2), "breach": lev_breach},
        "revolver_utilization_pct": _f(latest.get("revolver_utilization_pct")),
        "reported_status": reported, "computed_status": computed,
        "status_matches_computed": (("breach" in reported.lower()) == (computed == "Covenant Breach")),
        "_compliance": comp,
    }


def detect_deterioration_signals(borrower_name, revolver_alert_pct=75.0):
    """Deterministic deterioration signals over the full series — trends, threshold crossings, the
    status-vs-trend mislabel, thin cushion, and lifecycle (construction) signals. Facts only."""
    log = []
    rows = _lp_rows(borrower_name)
    if not rows:
        return _not_found(borrower_name)
    borrower = rows[0]["borrower_name"]
    guards.assert_processable(borrower, log=log)
    latest, comp = rows[-1], {"policy": ["§2.1", "§4.2", "§5"], "redactions": log}
    signals = []

    if _is_construction(latest):
        note = latest.get("notes", "") or ""
        m = _re.search(r"pre-leasing\s+(\d+)\s*%", note, _re.IGNORECASE)
        if m:
            pl = int(m.group(1))
            signals.append({"type": "lease_up", "fact": f"pre-leasing {pl}% vs the 75% perm-conversion threshold", "gap_pp": 75 - pl})
        signals.append({"type": "lifecycle",
                        "fact": "construction phase — operating DSCR/leverage covenants not in effect; monitor % complete, schedule slip, interest-reserve runway, and pre-leasing vs the 75% perm threshold"})
        return {"borrower": borrower, "as_of": latest["date"], "lifecycle": "construction", "signals": signals, "_compliance": comp}

    dscr = [_f(r.get("dscr_ttm")) for r in rows]
    rev = [_f(r.get("revolver_utilization_pct")) for r in rows]
    dscr_min = _f(latest.get("covenant_dscr_min"))

    if dscr[-1] < dscr[0]:
        signals.append({"type": "dscr_trend", "fact": f"DSCR declined {dscr[0]}→{dscr[-1]} over {len(rows)} months",
                        "floor": dscr_min, "below_floor": dscr[-1] < dscr_min})
    if rev[-1] > rev[0]:
        signals.append({"type": "revolver_trend", "fact": f"revolver utilization rose {rev[0]}%→{rev[-1]}%"})
    if rev[-1] >= revolver_alert_pct:
        signals.append({"type": "revolver_alert", "fact": f"revolver utilization {rev[-1]}% ≥ {revolver_alert_pct}% alert level (non-covenant metric)"})

    compliant_declining = sum(
        1 for i in range(1, len(rows))
        if rows[i].get("covenant_status", "").strip().lower() == "compliant" and dscr[i] < dscr[i - 1]
    )
    if compliant_declining >= 3:
        signals.append({"type": "status_vs_trend",
                        "fact": f"covenant_status read 'Compliant' during {compliant_declining} months of DSCR decline — the label lagged the trajectory"})

    cushion = round(dscr[-1] - dscr_min, 2)
    if 0 <= cushion <= 0.05:
        signals.append({"type": "thin_cushion", "fact": f"DSCR {dscr[-1]} is only {cushion} above the {dscr_min} floor (thin)"})

    return {"borrower": borrower, "as_of": latest["date"], "lifecycle": "operating", "signals": signals, "_compliance": comp}


import calendar as _cal
from datetime import date as _date


def _parse_date(s):
    s = (s or "").strip()
    try:
        p = s.split("-")
        if len(p) == 3:
            return _date(int(p[0]), int(p[1]), int(p[2]))
        if len(p) == 2:
            return _date(int(p[0]), int(p[1]), 1)
    except (ValueError, IndexError):
        return None
    return None


def _as_of_date():
    """Dataset 'now' = the last day of the latest month present in loan_performance (the reporting as-of)."""
    dates = [r.get("date", "") for r in da.loan_performance() if r.get("date")]
    if not dates:
        return None
    latest = max(dates)  # "YYYY-MM"
    y, m = int(latest[:4]), int(latest[5:7])
    return _date(y, m, _cal.monthrange(y, m)[1])


# word-boundary match so "sent" doesn't match "pre-SENT-ed"; 0-min already excludes email-sent notices
_NON_CONTACT_RE = _re.compile(r"\b(no answer|voicemail|no response|missed)\b", _re.IGNORECASE)


def _is_substantive(r):
    """A substantive two-way contact: not internal, duration > 0, and not a non-answer / one-way notice."""
    if (r.get("contact_direction", "") or "").strip().lower() == "internal":
        return False
    if _f(r.get("duration_minutes")) <= 0:
        return False
    if _NON_CONTACT_RE.search(r.get("outcome", "") or ""):
        return False
    if "formal notice" in (r.get("contact_type", "") or "").lower():
        return False
    return True


def measure_engagement_coverage(borrower_name, as_of=None):
    """Deterministic engagement gap: days since the last SUBSTANTIVE two-way contact (a one-way notice /
    email-sent / missed call / internal prep does NOT count), vs the naive 'days since any logged entry'.
    Facts only — surfaces where engagement has thinned; the RM judges significance."""
    log = []
    rows = da.match_borrower(borrower_name, da.activity_log())
    if not rows:
        return _not_found(borrower_name)
    rows.sort(key=lambda r: r.get("log_date", ""))
    borrower = rows[0]["borrower_name"]
    guards.assert_processable(borrower, log=log)
    as_of_d = _parse_date(as_of) if as_of else _as_of_date()
    subs = [r for r in rows if _is_substantive(r)]
    last_sub = subs[-1] if subs else None
    last_sub_d = _parse_date(last_sub["log_date"]) if last_sub else None
    last_any_d = _parse_date(rows[-1]["log_date"])
    days_sub = (as_of_d - last_sub_d).days if (as_of_d and last_sub_d) else None
    days_any = (as_of_d - last_any_d).days if (as_of_d and last_any_d) else None
    one_way_since = [
        {"date": r["log_date"], "type": r.get("contact_type"), "outcome": r.get("outcome")}
        for r in rows
        if last_sub_d and _parse_date(r["log_date"]) and _parse_date(r["log_date"]) > last_sub_d and not _is_substantive(r)
    ]
    return {
        "borrower": borrower,
        "as_of": as_of_d.isoformat() if as_of_d else None,
        "last_substantive_contact": (
            {"date": last_sub["log_date"], "type": last_sub.get("contact_type"), "outcome": last_sub.get("outcome")}
            if last_sub else None
        ),
        "days_since_substantive_contact": days_sub,
        "days_since_any_logged_entry": days_any,
        "undercount_days": (days_sub - days_any) if (days_sub is not None and days_any is not None) else None,
        "one_way_contacts_since": one_way_since,
        "note": "a one-way notice / email-sent / missed call / internal prep is NOT a two-way contact; the gap is to the last substantive contact",
        "_compliance": {"policy": ["§2.1", "§5"], "redactions": log},
    }


def run_evals():
    """Run the golden-set evaluation against THIS live tool logic and refresh the observability report.

    Deterministic, no LLM in the grader: each case calls the real core/guards function and checks
    source-grounded expectations (T1 ground-truth) + compliance assertions (T2). Also regenerates
    reports/observability.md so the per-prompt scorecards stay in sync. Returns a structured summary
    Claude can render in-console on either surface (Code or Cowork)."""
    import os
    import sys

    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    evals_dir = os.path.join(repo, "evals")
    if evals_dir not in sys.path:
        sys.path.insert(0, evals_dir)
    import runner  # evals/runner.py — stdlib, dispatches cases to this same core/guards logic
    import observability  # evals/observability.py — writes reports/observability.md

    results = runner.run_all()
    report_path, _, _ = observability.build(results)

    by_prompt, by_tier = {}, {}
    for r in results:
        for bucket, key in ((by_prompt, r["prompt"]), (by_tier, r["tier"])):
            agg = bucket.setdefault(key, {"passed": 0, "total": 0})
            agg["total"] += 1
            agg["passed"] += 1 if r["passed"] else 0
    npass = sum(1 for r in results if r["passed"])
    failures = [{"id": r["id"], "detail": r["detail"]} for r in results if not r["passed"]]

    return {
        "total": len(results),
        "passed": npass,
        "failed": len(results) - npass,
        "all_passed": npass == len(results),
        "by_prompt": by_prompt,
        "by_tier": by_tier,
        "failures": failures,
        "observability_report": os.path.relpath(report_path, repo),
        "_compliance": {
            "note": "Deterministic eval of the live MCP tool logic — T1 source-grounded ground truth + "
                    "T2 binary compliance assertions (§2.1 strip / §5 halt / guarantor refusal / §4.2 "
                    "block) + negatives. NO LLM in the grader; 'accuracy' is a clean number only here, "
                    "never a fabricated single % for generative output."
        },
    }


def assemble_watchlist(borrowers=None):
    """Compose covenant + deterioration + engagement into a portfolio triage list, ranked by
    risk × neglect (facts-derived order, NOT a credit rating). RM-private; §4.1 monitoring → CCO approval."""
    names = borrowers or da.list_borrowers()
    items = []
    for n in names:
        cc = check_covenant_compliance(n)
        det = detect_deterioration_signals(n)
        eng = measure_engagement_coverage(n)
        construction = det.get("lifecycle") == "construction"
        breach = (not construction) and cc.get("computed_status") == "Covenant Breach"
        signals = det.get("signals", [])
        items.append({
            "borrower": n,
            "lifecycle": det.get("lifecycle"),
            "covenant_status": (cc.get("reported_status") if construction else cc.get("computed_status")),
            "breach": breach,
            "signal_count": len(signals),
            "top_signals": [s["fact"] for s in signals[:3]],
            "days_since_substantive_contact": eng.get("days_since_substantive_contact"),
        })
    items.sort(key=lambda it: (1 if it["breach"] else 0, it["signal_count"], it["days_since_substantive_contact"] or 0), reverse=True)
    aod = _as_of_date()
    return {
        "as_of": aod.isoformat() if aod else None,
        "ranked_by": "covenant breach, then deterioration-signal count, then days-since-substantive-contact (facts-derived triage order — NOT a credit rating)",
        "watchlist": items,
        "note": "facts only (§4.2); RM-private/advisory; automated alerting needs CCO approval (§4.1). A compliant borrower with 0 signals (e.g., Crestwood) sinks to the bottom — distress monitoring is structurally blind to it; renewal/retention risk is a separate lens.",
        "_compliance": {"policy": ["§2.1", "§4.1", "§4.2", "§5"]},
    }
