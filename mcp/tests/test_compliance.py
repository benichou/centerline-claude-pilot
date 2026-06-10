"""Deterministic guard/core tests — stdlib only (no `mcp` SDK needed).

Run:  PYTHONPATH=mcp python3 mcp/tests/test_compliance.py
Exits non-zero on the first failed assertion.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from centerline_mcp import core, guards  # noqa: E402

_passed = 0


def check(name, cond):
    global _passed
    print(("PASS " if cond else "FAIL "), name)
    assert cond, f"FAILED: {name}"
    _passed += 1


# --- §2.1: credit_grade stripped from the dossier profile ---
d = core.get_borrower_dossier("Meridian")
check("dossier returned (no error)", "profile" in d and not d.get("error"))
check("§2.1 credit_grade stripped from profile", "credit_grade" not in d["profile"])
check(
    "redaction logged (strip_field credit_grade)",
    any(e["action"] == "strip_field" and e["field"] == "credit_grade" for e in d["_compliance"]["redactions"]),
)

# --- covenant_status preserved (decided: factual/allowed) ---
p = core.get_loan_performance("Meridian", months=3)
check("performance rows returned", p.get("months", 0) >= 1)
check("covenant_status preserved (factual)", "covenant_status" in p["performance"][-1])
check("credit_grade absent from performance rows", all("credit_grade" not in r for r in p["performance"]))

# --- §2.1: free-text designation redaction (unit) ---
red, hits = guards.redact_text("Borrower placed on the watchlist; discussing Special Assets.")
check(
    "watchlist / Special-Assets language redacted in free text",
    "watchlist" not in red.lower() and "special assets" not in red.lower() and bool(hits),
)

# --- §5 gate: halts a Special-Assets borrower (status-based) ---
borrower = d["borrower"]
guards.SPECIAL_ASSETS_BORROWERS.add(borrower)
try:
    core.get_borrower_dossier(borrower)
    check("§5 gate halts SA borrower", False)
except guards.ComplianceRefusal:
    check("§5 gate halts SA borrower", True)
finally:
    guards.SPECIAL_ASSETS_BORROWERS.discard(borrower)

# §5 gate does NOT fire for the same borrower once de-listed (no false halt)
check("§5 does not false-halt a normal borrower", "profile" in core.get_borrower_dossier(borrower))

# --- §2.1: guarantor personal-financial document refused ---
try:
    guards.refuse_if_guarantor_doc({"doc_type": "guarantor_personal_financial_statement"})
    check("guarantor doc refused", False)
except guards.ComplianceRefusal:
    check("guarantor doc refused", True)

# a normal document is NOT refused (negative case)
guards.refuse_if_guarantor_doc({"doc_type": "covenant_certificate"})
check("normal document is not refused", True)

# --- §4.2 output guard: screen_and_finalize ---
# factual covenant language is ALLOWED (not flagged) and gets a footer + §4.3 tag
ok_text = "Meridian DSCR is 1.03 vs the 1.20 covenant minimum (loan_performance, 2025-05); covenant_status: Covenant Breach."
r = core.screen_and_finalize(ok_text)
check("factual covenant text is NOT blocked (§4.2)", r["ok"] and not r["violations"])
check("reliability footer attached", "Reliability:" in (r["finalized_text"] or ""))
check("§4.3 RM-review tag attached", "RM review" in (r["finalized_text"] or ""))
check("cited factual text rated Grounded", r["reliability"]["label"] == "Grounded")

# credit-characterizing / predictive / recommending language is BLOCKED
bad_text = "This borrower is high credit risk and likely to default; I recommend waiving the covenant."
b = core.screen_and_finalize(bad_text)
check("credit-adjacent language is BLOCKED (§4.2)", b["blocked"] and len(b["violations"]) >= 1)
check("blocked output is not finalized", b["finalized_text"] is None)

# uncited text is flagged Unverified (not blocked)
u = core.screen_and_finalize("Revolver utilization climbed to 85% this quarter.")
check("uncited factual text -> Unverified (not blocked)", u["ok"] and u["reliability"]["label"] == "Unverified")

# regression (Cowork-surfaced): a tool/as-of-sourced output must read Grounded, not "Unverified"
tool_sourced = "DSCR 1.03 vs the 1.20 minimum. Source: centerline MCP check_covenant_compliance, as-of 2025-05."
ts = core.screen_and_finalize(tool_sourced)
check("tool/as-of-sourced output rated Grounded (citation heuristic recognizes provenance)", ts["reliability"]["label"] == "Grounded")

# --- new retrieval tools: get_activity_log + get_emails (§2.1 redaction, §5 gate) ---
al = core.get_activity_log("Meridian")
check("activity_log returned", al.get("entries", 0) >= 1 and not al.get("error"))
check("activity_log rows carry no credit_grade", all("credit_grade" not in e for e in al["activity"]))
check("activity_log free-text has no raw watchlist/Special-Assets", all(
    "watchlist" not in (e.get("raw_notes") or "").lower() and "special assets" not in (e.get("raw_notes") or "").lower()
    for e in al["activity"]))

em = core.get_emails("Meridian")
check("emails thread returned", bool(em.get("thread")) and not em.get("error"))
check("emails thread has no raw watchlist/Special-Assets designation", (
    "watchlist" not in em["thread"].lower() and "special assets" not in em["thread"].lower()))

# §5 gate also halts these tools for a configured SA borrower
guards.SPECIAL_ASSETS_BORROWERS.add(al["borrower"])
try:
    core.get_activity_log(al["borrower"]); check("§5 halts get_activity_log for SA borrower", False)
except guards.ComplianceRefusal:
    check("§5 halts get_activity_log for SA borrower", True)
finally:
    guards.SPECIAL_ASSETS_BORROWERS.discard(al["borrower"])

# --- Track A: deterministic covenant compliance (grounded in real numbers) ---
cc = core.check_covenant_compliance("Meridian")
check("Meridian DSCR breach computed (1.03 < 1.20)", cc["dscr"]["breach"] and cc["dscr"]["value"] == 1.03 and cc["dscr"]["min"] == 1.20)
check("Meridian DSCR cushion = -0.17", cc["dscr"]["cushion"] == -0.17)
check("Meridian leverage breach computed (4.5 > 4.0)", cc["leverage"]["breach"])
check("Meridian computed_status = Covenant Breach", cc["computed_status"] == "Covenant Breach")

cw = core.check_covenant_compliance("Crestwood")
check("Crestwood compliant (no breach)", not cw["dscr"]["breach"] and not cw["leverage"]["breach"] and cw["computed_status"] == "Compliant")

ar = core.check_covenant_compliance("Arcadia")
check("Arcadia (construction) covenant test not applicable", ar.get("applicable") is False)

# --- Track A: deterministic deterioration signals ---
def _types(res):
    return {s["type"] for s in res["signals"]}

dm = core.detect_deterioration_signals("Meridian")
mt = _types(dm)
check("Meridian: DSCR-decline signal", "dscr_trend" in mt)
check("Meridian: revolver ≥75% alert signal", "revolver_alert" in mt)
check("Meridian: status-vs-trend mislabel signal", "status_vs_trend" in mt)

dc = core.detect_deterioration_signals("Crestwood")
check("Crestwood: NO deterioration signals (healthy → early-warning blind)", len(dc["signals"]) == 0)

ds = core.detect_deterioration_signals("Summit")
check("Summit: thin-cushion signal (+0.02 above floor)", "thin_cushion" in _types(ds))

da_ = core.detect_deterioration_signals("Arcadia")
check("Arcadia: construction lifecycle + pre-leasing-vs-75% signal", da_["lifecycle"] == "construction" and "lease_up" in _types(da_))

# --- Track A: engagement coverage (the ★ gem), grounded in the 78-day Meridian finding ---
eg = core.measure_engagement_coverage("Meridian")
check("Meridian as_of = 2025-05-31 (end of latest data month)", eg["as_of"] == "2025-05-31")
check("Meridian last substantive contact = 2025-03-14", eg["last_substantive_contact"]["date"] == "2025-03-14")
check("Meridian days since substantive contact = 78", eg["days_since_substantive_contact"] == 78)
check("Meridian naive days since any entry = 33 (undercount surfaced)", eg["days_since_any_logged_entry"] == 33)
check("Meridian: the entry since (4/28) is a one-way notice, not contact", len(eg["one_way_contacts_since"]) >= 1)

# --- Track A: watchlist triage (A1) ---
wl = core.assemble_watchlist()
order = [it["borrower"] for it in wl["watchlist"]]
check("watchlist #1 is Meridian (breach + signals + gap)", order[0].startswith("Meridian"))
check("Crestwood is last (compliant, 0 signals — early-warning blind)", order[-1].startswith("Crestwood"))
crest = next(it for it in wl["watchlist"] if it["borrower"].startswith("Crestwood"))
check("Crestwood entry: not breach, 0 signals", (not crest["breach"]) and crest["signal_count"] == 0)

# regression: "Renewal Proposal Presented" must count as substantive (don't substring-match "sent" in "presented")
ce = core.measure_engagement_coverage("Crestwood")
check("Crestwood last substantive = 2025-04-15 renewal meeting (no 'sent'-in-'presented' bug)", ce["last_substantive_contact"]["date"] == "2025-04-15")

print(f"\nALL {_passed} CHECKS PASSED")
