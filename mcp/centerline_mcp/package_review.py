"""Covenant-package review — the DETERMINISTIC half of doc-intelligence (NO Anthropic API call).

Doc-intel splits cleanly: the MODEL reads the PDFs (`docintel.classify_document` /
`extract_document_fields`), then this module's deterministic code DECIDES — exactly the pattern the rest
of the system uses (the model never does the arithmetic or the compliance call).

  - `recompute_ratios(...)`           — DSCR / leverage from the UNADJUSTED (GAAP) financials.
  - `cross_validate_covenant(...)`    — the headline: certified (as the certificate claims) vs recomputed
    (GAAP) vs the bank's own loan_performance, plus the EBITDA add-back bridge that explains the gap.
  - `review_package(...)`             — intake inventory: completeness (required vs received → missing) +
    quality flags (unsigned rep letter, withheld A/R names) + the §2.1 refusals, for one borrower.

PROVENANCE IS FIRST-CLASS (Sarah was burned by an unreliable AI): every figure and every flag carries the
**document + field + value** (or the deriving **tool**) it came from, so nothing is asserted without a
trace. The functions also emit `cross_source_mismatches` / `low_confidence_inputs` lists ready to hand to
`screen_and_finalize`, so the reliability footer reflects the actual provenance coverage.

All outputs are FACTS (§4.2) — a covenant-test result is a fact (same as `check_covenant_compliance`);
none of this characterizes creditworthiness. The RM owns the judgment.
"""

from . import core

# Per-borrower intake expectation. Grounded in the Meridian memo's Feb-14 follow-up list + the package INDEX.
_PACKAGES = {
    "Meridian Fabrication": {
        "required_document_types": [
            "covenant_compliance_certificate",
            "financial_statement",
            "ar_aging_report",
            "management_representation_letter",
            "aerospace_purchase_order",
            "cash_flow_projections",
        ],
        "required_data_elements": [
            "accounts_receivable_customer_names (60-90 day automotive balances)",
        ],
    }
}


def _num(v):
    """Coerce an extracted value to float, or None if absent/non-numeric."""
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _src(document=None, field=None, tool=None, basis=None, value=None):
    """A provenance tag — where a figure/flag came from. Any subset of {document, field, value} or a
    deriving {tool}. Keeps every conclusion traceable to its source (Sarah's trust scar)."""
    s = {}
    if document is not None:
        s["document"] = document
    if field is not None:
        s["field"] = field
    if value is not None:
        s["value"] = value
    if tool is not None:
        s["tool"] = tool
    if basis is not None:
        s["basis"] = basis
    return s


def recompute_ratios(gaap_ebitda, total_debt_service, total_funded_debt):
    """DSCR / leverage on the UNADJUSTED (GAAP) basis — no add-backs. Returns None for a ratio whose
    inputs are missing rather than guessing."""
    e, ds, fd = _num(gaap_ebitda), _num(total_debt_service), _num(total_funded_debt)
    return {
        "basis": "unadjusted GAAP EBITDA (no add-backs)",
        "gaap_ebitda": e,
        "total_debt_service": ds,
        "total_funded_debt": fd,
        "dscr": round(e / ds, 2) if e is not None and ds else None,
        "leverage": round(fd / e, 2) if fd is not None and e else None,
    }


def cross_validate_covenant(certificate, financials, borrower="Meridian Fabrication"):
    """Three-way reconciliation of the covenant ratios, every figure provenance-tagged:

      1. CERTIFIED   — what the borrower's compliance certificate claims (Adjusted-EBITDA basis).
      2. RECOMPUTED  — what the attached UNADJUSTED financials produce (GAAP basis), computed here.
      3. BANK        — the bank's own loan_performance for the latest month (`check_covenant_compliance`).

    Surfaces the EBITDA add-back bridge (Adjusted − GAAP) that drives any gap, returns `findings` with
    their sources, and emits `cross_source_mismatches` ready for `screen_and_finalize`. `certificate` /
    `financials` are the `extracted` dicts from `extract_document_fields`.
    """
    certificate = certificate or {}
    financials = financials or {}
    CERT, FIN = "covenant_compliance_certificate", "financial_statement"

    dscr_min = _num(certificate.get("dscr_min"))
    lev_max = _num(certificate.get("leverage_max"))
    certified_dscr = _num(certificate.get("certified_dscr"))
    certified_lev = _num(certificate.get("certified_leverage"))
    gaap_ebitda = _num(financials.get("ebitda_gaap"))
    adj_ebitda = _num(certificate.get("adjusted_ebitda"))
    # Prefer the financial statement for the recompute inputs; fall back to the certificate's own figures.
    ds_doc, fd_doc = FIN, FIN
    debt_service = _num(financials.get("total_debt_service"))
    if debt_service is None:
        debt_service, ds_doc = _num(certificate.get("total_debt_service")), CERT
    funded_debt = _num(financials.get("total_funded_debt"))
    if funded_debt is None:
        funded_debt, fd_doc = _num(certificate.get("total_funded_debt")), CERT

    rc = recompute_ratios(gaap_ebitda, debt_service, funded_debt)
    rc_dscr, rc_lev = rc["dscr"], rc["leverage"]

    # The bank's own view (loan_performance, latest month) — deterministic, server-side.
    bank = {"dscr": None, "leverage": None, "as_of": None, "available": False}
    try:
        cc = core.check_covenant_compliance(borrower)
        if cc.get("applicable", True) and "dscr" in cc:
            bank = {
                "dscr": cc["dscr"].get("value"),
                "leverage": cc["leverage"].get("value"),
                "as_of": cc.get("as_of"),
                "available": True,
            }
    except Exception:  # noqa: BLE001 — loan_perf is a corroborating source; absence must not break review
        pass

    addbacks = certificate.get("addbacks") or []
    addback_total = round(adj_ebitda - gaap_ebitda, 1) if (adj_ebitda is not None and gaap_ebitda is not None) else None

    def _clears(value, limit, maximum):
        if value is None or limit is None:
            return None
        return (value <= limit) if maximum else (value >= limit)

    cert_dscr_ok = _clears(certified_dscr, dscr_min, maximum=False)
    rc_dscr_ok = _clears(rc_dscr, dscr_min, maximum=False)
    cert_lev_ok = _clears(certified_lev, lev_max, maximum=True)
    rc_lev_ok = _clears(rc_lev, lev_max, maximum=True)

    findings, mismatches = [], []
    if cert_dscr_ok and rc_dscr_ok is False:
        findings.append(
            {
                "statement": f"DSCR: certified {certified_dscr} clears the {dscr_min} minimum, but the unadjusted "
                f"financials recompute to {rc_dscr} — below the minimum. The certification rests on Adjusted EBITDA.",
                "sources": [
                    _src(document=CERT, field="certified_dscr", value=certified_dscr),
                    _src(document=FIN, field="ebitda_gaap", value=gaap_ebitda),
                    _src(document=ds_doc, field="total_debt_service", value=debt_service),
                ],
            }
        )
        mismatches.append({"metric": "DSCR", "certified": certified_dscr, "recomputed": rc_dscr, "minimum": dscr_min})
    if cert_lev_ok and rc_lev_ok is False:
        findings.append(
            {
                "statement": f"Leverage: certified {certified_lev} is within the {lev_max} maximum, but the unadjusted "
                f"financials recompute to {rc_lev} — above the maximum.",
                "sources": [
                    _src(document=CERT, field="certified_leverage", value=certified_lev),
                    _src(document=fd_doc, field="total_funded_debt", value=funded_debt),
                    _src(document=FIN, field="ebitda_gaap", value=gaap_ebitda),
                ],
            }
        )
        mismatches.append({"metric": "leverage", "certified": certified_lev, "recomputed": rc_lev, "maximum": lev_max})
    if addback_total:
        labels = ", ".join(f"{a.get('label')} ({a.get('amount')})" for a in addbacks) if addbacks else "unspecified"
        findings.append(
            {
                "statement": f"EBITDA add-back bridge: Adjusted {adj_ebitda} vs GAAP {gaap_ebitda} = {addback_total} of "
                f"add-backs [{labels}]. Applying them is what moves the ratios from breach to compliant.",
                "sources": [
                    _src(document=CERT, field="adjusted_ebitda", value=adj_ebitda),
                    _src(document=FIN, field="ebitda_gaap", value=gaap_ebitda),
                    _src(document=CERT, field="addbacks"),
                ],
            }
        )

    agreement = "unknown"
    if bank["available"] and rc_dscr is not None and _num(bank["dscr"]) is not None:
        agree = abs(rc_dscr - _num(bank["dscr"])) <= 0.05
        agreement = "agree" if agree else "disagree"
        findings.append(
            {
                "statement": f"Corroboration: the bank's loan_performance ({bank['as_of']}) shows DSCR {bank['dscr']} / "
                f"leverage {bank['leverage']} — {'consistent with' if agree else 'differs from'} the recomputed "
                f"{rc_dscr} / {rc_lev}.",
                "sources": [
                    _src(tool="check_covenant_compliance", basis=f"loan_performance latest month ({bank['as_of']})")
                ],
            }
        )

    reconciles = (certified_dscr == rc_dscr) and (certified_lev == rc_lev)
    return {
        "borrower": borrower,
        "thresholds": {
            "dscr_min": dscr_min,
            "leverage_max": lev_max,
            "source": _src(document=CERT, field="dscr_min / leverage_max"),
        },
        "certified": {
            "dscr": {"value": certified_dscr, "source": _src(document=CERT, field="certified_dscr")},
            "leverage": {"value": certified_lev, "source": _src(document=CERT, field="certified_leverage")},
            "basis": "Adjusted EBITDA (per certificate)",
        },
        "recomputed": {
            "dscr": {
                "value": rc_dscr,
                "derivation": f"GAAP EBITDA {gaap_ebitda} ÷ total debt service {debt_service}",
                "sources": [
                    _src(document=FIN, field="ebitda_gaap", value=gaap_ebitda),
                    _src(document=ds_doc, field="total_debt_service", value=debt_service),
                ],
            },
            "leverage": {
                "value": rc_lev,
                "derivation": f"total funded debt {funded_debt} ÷ GAAP EBITDA {gaap_ebitda}",
                "sources": [
                    _src(document=fd_doc, field="total_funded_debt", value=funded_debt),
                    _src(document=FIN, field="ebitda_gaap", value=gaap_ebitda),
                ],
            },
            "basis": rc["basis"],
        },
        "bank_loan_performance": {
            **bank,
            "source": _src(tool="check_covenant_compliance", basis="loan_performance latest month"),
        },
        "addback_bridge": {
            "total": addback_total,
            "adjusted_ebitda": {"value": adj_ebitda, "source": _src(document=CERT, field="adjusted_ebitda")},
            "gaap_ebitda": {"value": gaap_ebitda, "source": _src(document=FIN, field="ebitda_gaap")},
            "addbacks": addbacks,
        },
        "ratios_reconcile": reconciles,
        "cross_source_agreement": agreement,
        "findings": findings,
        "cross_source_mismatches": mismatches,
        "note": "Facts only (§4.2). Every figure is tagged to its document + field; the RM reviews the add-back support.",
    }


def review_package(items, borrower="Meridian Fabrication"):
    """Intake summary for a classified+extracted package. `items` = list of dicts shaped like the
    classify/extract outputs: {doc_type, path?, extracted?|None, refused?, skipped?}. Deterministic:
    completeness (required vs received → missing) + quality flags + the §2.1 refusals — each tagged to
    its source document/field — plus a `low_confidence_inputs` list ready for `screen_and_finalize`."""
    spec = _PACKAGES.get(borrower, {"required_document_types": [], "required_data_elements": []})
    items = items or []

    inventory, refusals, quality = [], [], []
    received_types, by_type = [], {}
    for it in items:
        dt = it.get("doc_type")
        doc = it.get("path") or dt
        status = "refused (§2.1)" if it.get("refused") else ("skipped" if it.get("skipped") else "extracted")
        inventory.append({"doc_type": dt, "document": doc, "status": status})
        if it.get("refused"):
            refusals.append({"doc_type": dt, "document": doc, "policy": it.get("policy", "§2.1")})
            continue
        if dt:
            received_types.append(dt)
            by_type[dt] = it.get("extracted") or {}

    missing = [
        {"document": t, "basis": "required for the package (memo Feb-14 follow-up list); not received"}
        for t in spec["required_document_types"]
        if t not in received_types
    ]

    rep = by_type.get("management_representation_letter")
    if rep is not None and rep.get("signed") is False:
        quality.append(
            {
                "doc_type": "management_representation_letter",
                "flag": "unsigned",
                "detail": "Representation letter extraction returned signed=false — not executed; cannot be relied on.",
                "source": _src(document="management_representation_letter", field="signed", value=False),
            }
        )
    ar = by_type.get("ar_aging_report")
    if ar is not None and ar.get("customer_names_present") is False:
        quality.append(
            {
                "doc_type": "ar_aging_report",
                "flag": "customer_names_withheld",
                "detail": "A/R aging present but customer names withheld — the 60-90 day automotive balances are unnamed.",
                "source": _src(document="ar_aging_report", field="customer_names_present", value=False),
            }
        )

    # Ready-to-pass list for screen_and_finalize so the reliability footer reflects provenance coverage.
    low_confidence_inputs = (
        [f"missing document: {m['document']}" for m in missing]
        + [f"{q['doc_type']}: {q['flag']}" for q in quality]
        + [f"outstanding data element: {e}" for e in spec["required_data_elements"]]
    )

    return {
        "borrower": borrower,
        "inventory": inventory,
        "received_document_types": received_types,
        "missing_documents": missing,
        "outstanding_data_elements": spec["required_data_elements"],
        "quality_flags": quality,
        "section_2_1_refusals": refusals,
        "low_confidence_inputs": low_confidence_inputs,
        "note": "Facts only (§4.2). Completeness/quality are intake checks; the RM owns any credit judgment.",
    }
