"""Doc-intel deterministic tests — the §2.1 pre-screen + classify/extract dispatch + prompt wiring.

NO Anthropic API calls (those are exercised live by Franck on the real PDFs). This covers the parts that must
be correct regardless of the model: the §2.1 gate, the routing of `other`/guarantor/unknown types, the schema
↔ prompt wiring, and that the Pydantic models validate.

Needs the uv env (pydantic / jinja2 / pyyaml):
    PYTHONPATH=mcp uv run python mcp/tests/test_docintel.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from centerline_mcp import docintel, package_review, prompts  # noqa: E402

_passed = 0


def check(name, cond):
    global _passed
    print(("PASS " if cond else "FAIL "), name)
    assert cond, f"FAILED: {name}"
    _passed += 1


_PKG = "data/synthetic/meridian-package"
guarantor = f"{_PKG}/meridian_guarantor_personal_financial_statement.pdf"
cert = f"{_PKG}/meridian_covenant_compliance_certificate_Q1-2025.pdf"

# --- §2.1 pre-screen (deterministic, BEFORE any API call) ---
pre = docintel.prescreen_section_2_1(guarantor)
check("§2.1 pre-screen refuses the guarantor PFS on filename", bool(pre) and pre["refused"] is True)
check("§2.1 refusal records it was NOT sent to a model", pre["sent_to_model"] is False and pre["policy"] == "§2.1")
check("§2.1 pre-screen does NOT refuse the covenant certificate", docintel.prescreen_section_2_1(cert) is None)
check(
    "§2.1 pre-screen does NOT refuse a financial statement",
    docintel.prescreen_section_2_1(f"{_PKG}/x_financial_statement.pdf") is None,
)

# --- extract dispatch (deterministic short-circuits; no API, no file read needed) ---
o = docintel.extract_document_fields("any.pdf", "other")
check("extract: 'other' is skipped (not extracted)", o["skipped"] is True and o["extracted"] is None)
g = docintel.extract_document_fields("any.pdf", "guarantor_personal_financial_statement")
check("extract: guarantor refused (§2.1), not extracted", g["refused"] is True and g["extracted"] is None)
po = docintel.extract_document_fields("any.pdf", "purchase_order")
check("extract: purchase_order skipped (no schema)", po["skipped"] is True)
bogus = docintel.extract_document_fields("any.pdf", "bogus_type")
check("extract: unknown doc_type errors", "error" in bogus)

# --- schema ↔ prompt wiring: every extractable type has a renderable YAML+Jinja prompt ---
for dt, (model_cls, prompt_name) in docintel.SCHEMAS.items():
    s, i = prompts.render(prompt_name)
    check(
        f"prompt renders + persona present for {dt}", bool(s) and bool(i) and "commercial-banking document expert" in s
    )

# classify prompt renders + lists every doc type from the catalog
cs, ci = prompts.render("classify")
check("classify prompt renders with persona", "commercial-banking document expert" in cs)
check("classify prompt lists all catalog doc types", all(t["name"] in ci for t in prompts.DOC_TYPES))

# --- Pydantic models validate (forced-output shapes) ---
c = docintel.Classification(doc_type="other", confidence=0.9, rationale="insurance certificate", key_signals=["ACORD"])
check(
    "Classification validates + defaults is_restricted=False",
    c.doc_type == "other" and c.is_restricted_personal_guarantor_info is False,
)
cc = docintel.CovenantCertificate(
    certified_dscr=1.23,
    gaap_ebitda=10100,
    adjusted_ebitda=12100,
    addbacks=[{"label": "non-recurring legal", "amount": 800}],
    signed=True,
)
check(
    "CovenantCertificate validates incl. nested addbacks",
    cc.addbacks[0].label == "non-recurring legal" and cc.certified_dscr == 1.23,
)

# --- package_review: recompute + cross-validate + completeness/quality (deterministic; no API) ---
# Grounded in the synthetic Meridian package (generate_meridian_package.py).
_FIN = {"ebitda_gaap": 10100, "total_debt_service": 9800, "total_funded_debt": 45450}
_CERT = {
    "certified_dscr": 1.23,
    "dscr_min": 1.20,
    "certified_leverage": 3.76,
    "leverage_max": 4.00,
    "gaap_ebitda": 10100,
    "adjusted_ebitda": 12100,
    "addbacks": [{"label": "non-recurring legal & restructuring", "amount": 2000}],
    "total_debt_service": 9800,
    "total_funded_debt": 45450,
}

rr = package_review.recompute_ratios(10100, 9800, 45450)
check("recompute: GAAP DSCR = 1.03", rr["dscr"] == 1.03)
check("recompute: GAAP leverage = 4.50", rr["leverage"] == 4.50)
check(
    "recompute: missing input -> None (no guessing)", package_review.recompute_ratios(None, 9800, 45450)["dscr"] is None
)

xv = package_review.cross_validate_covenant(_CERT, _FIN, "Meridian Fabrication")
check(
    "cross-validate: certified 1.23 vs recomputed 1.03 (do NOT reconcile)",
    xv["ratios_reconcile"] is False and xv["recomputed"]["dscr"]["value"] == 1.03,
)
check("cross-validate: $2,000k add-back bridge surfaced", xv["addback_bridge"]["total"] == 2000.0)
check(
    "cross-validate: a DSCR certified-clears-but-recompute-below finding fires",
    any("below the minimum" in f["statement"] for f in xv["findings"]),
)
check(
    "cross-validate: bank loan_performance corroborates (DSCR 1.03, agreement=agree)",
    xv["bank_loan_performance"]["available"]
    and float(xv["bank_loan_performance"]["dscr"]) == 1.03
    and xv["cross_source_agreement"] == "agree",
)
# Provenance (Sarah's scar): every figure traces to a document + field, and findings carry sources.
check(
    "provenance: recomputed DSCR has a derivation + sources naming the financial-statement fields",
    "derivation" in xv["recomputed"]["dscr"]
    and {(s.get("document"), s.get("field")) for s in xv["recomputed"]["dscr"]["sources"]}
    == {("financial_statement", "ebitda_gaap"), ("financial_statement", "total_debt_service")},
)
check(
    "provenance: certified DSCR is sourced to the covenant certificate field",
    xv["certified"]["dscr"]["source"] == {"document": "covenant_compliance_certificate", "field": "certified_dscr"},
)
check(
    "provenance: bank figure is sourced to the check_covenant_compliance tool",
    xv["bank_loan_performance"]["source"].get("tool") == "check_covenant_compliance",
)
check(
    "provenance: every finding carries at least one source",
    all(f.get("sources") for f in xv["findings"]),
)
check(
    "footer tie-in: cross_source_mismatches lists DSCR + leverage (ready for screen_and_finalize)",
    {m["metric"] for m in xv["cross_source_mismatches"]} == {"DSCR", "leverage"},
)

items = [
    {
        "doc_type": "covenant_compliance_certificate",
        "path": "meridian_covenant_compliance_certificate_Q1-2025.pdf",
        "extracted": _CERT,
    },
    {"doc_type": "financial_statement", "path": "meridian_financial_statement_Q1-2025.pdf", "extracted": _FIN},
    {"doc_type": "ar_aging_report", "extracted": {"total_ar": 9800, "customer_names_present": False}},
    {"doc_type": "management_representation_letter", "extracted": {"signed": False}},
    {"doc_type": "guarantor_personal_financial_statement", "refused": True, "policy": "§2.1"},
    {"doc_type": "other", "skipped": True},
]
rp = package_review.review_package(items, "Meridian Fabrication")
check(
    "review_package: missing docs = aerospace PO + projections",
    {m["document"] for m in rp["missing_documents"]} == {"aerospace_purchase_order", "cash_flow_projections"},
)
check(
    "review_package: outstanding data element = A/R customer names",
    any("customer_names" in e for e in rp["outstanding_data_elements"]),
)
check("review_package: unsigned rep letter flagged", any(q["flag"] == "unsigned" for q in rp["quality_flags"]))
check(
    "review_package: withheld A/R names flagged",
    any(q["flag"] == "customer_names_withheld" for q in rp["quality_flags"]),
)
check(
    "provenance: each quality flag carries its source (document + field + value)",
    all({"document", "field", "value"} <= set(q["source"]) for q in rp["quality_flags"]),
)
check(
    "review_package: guarantor PFS recorded as a §2.1 refusal",
    any(r["doc_type"] == "guarantor_personal_financial_statement" for r in rp["section_2_1_refusals"]),
)
check(
    "footer tie-in: low_confidence_inputs covers missing + unsigned + withheld (for screen_and_finalize)",
    any("aerospace_purchase_order" in i for i in rp["low_confidence_inputs"])
    and any("unsigned" in i for i in rp["low_confidence_inputs"]),
)
check(
    "review_package: a clean borrower with all docs has no missing",
    package_review.review_package(
        [
            {"doc_type": t, "extracted": {}}
            for t in package_review._PACKAGES["Meridian Fabrication"]["required_document_types"]
        ],
        "Meridian Fabrication",
    )["missing_documents"]
    == [],
)

# confidence band (qualitative; no numeric % in narration) — testable without the API
check(
    "classify confidence band: 0.92->high, 0.7->medium, 0.3->low",
    (docintel._confidence_band(0.92), docintel._confidence_band(0.7), docintel._confidence_band(0.3))
    == ("high", "medium", "low"),
)

# --- list_documents: host-side enumeration (no sandbox grant, no guessing) ---
ld = docintel.list_documents(_PKG)
check("list_documents: finds the 6 package PDFs", len(ld["pdfs"]) == 6)
check(
    "list_documents: includes the guarantor PFS + the ACORD COI (the §2.1 + `other` cases)",
    "meridian_guarantor_personal_financial_statement.pdf" in ld["pdfs"]
    and "meridian_certificate_of_insurance.pdf" in ld["pdfs"],
)
check("list_documents: bad directory -> error (no crash)", "error" in docintel.list_documents("nope/not/here"))

# --- render_pdf: screened markdown (incl. a GFM table) -> valid PDF, banner/footer preserved (no API) ---
from centerline_mcp import pdf_render  # noqa: E402

_MD = (
    "# Meridian — Intake Readout\n\n"
    "*Requires RM review (§4.3).*\n\n"
    "| Covenant | Threshold | Certified | Recomputed |\n|---|---|---|---|\n"
    "| DSCR | >= 1.20 | 1.23 | 1.03 |\n| Leverage | <= 4.00 | 3.76 | 4.50 |\n\n"
    "## Quality flags\n- Rep letter **unsigned** [signed=false].\n\n---\nReliability: **Partial** — 2 mismatches."
)
_pdf = pdf_render.render_pdf(_MD, title=None, output_path="reports/pdf/_test_render.pdf")
_abs = os.path.join(pdf_render._REPO, _pdf["path"])
check("render_pdf: returns ok + a path under reports/pdf", _pdf["ok"] and _pdf["path"].startswith("reports/pdf/"))
check(
    "render_pdf: produced a non-empty, valid PDF (handles headings/table/bullets/rule)",
    _pdf["bytes"] > 1000 and open(_abs, "rb").read(5) == b"%PDF-",
)
import re as _re  # noqa: E402

check(
    "render_pdf: filename is UTC-timestamped + unique (no overwrite)",
    bool(_re.search(r"_\d{8}T\d{6}Z\.pdf$", _pdf["path"])),
)
_pdf2 = pdf_render.render_pdf(_MD, output_path="reports/pdf/_test_render.pdf", timestamp=False)
check("render_pdf: timestamp=False writes the exact name", _pdf2["path"] == "reports/pdf/_test_render.pdf")
check(
    "render_pdf: body leading with an H1 suppresses the title arg (no duplicate title)",
    pdf_render._leading_h1("# Title\n\nbody") is True and pdf_render._leading_h1("body only") is False,
)
os.remove(_abs)  # don't leave test artifacts in the tree
os.remove(os.path.join(pdf_render._REPO, _pdf2["path"]))

print(f"\nALL {_passed} DOC-INTEL CHECKS PASSED")
