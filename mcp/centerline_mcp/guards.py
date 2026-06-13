"""Server-side compliance guards (the universal chokepoint).

Enforces the unambiguous policy controls deterministically:
  - §2.1  strip the internal credit rating field (`credit_grade`)
  - §2.1  redact watchlist / Special-Assets *designation* language from free text
  - §2.1  refuse guarantor personal-financial *documents* (never read)
  - §5    halt processing for borrowers in Special Assets / active litigation

DESIGN NOTES (honest):
  - §5 is a STATUS check (config list / explicit status), NOT a free-text token scan.
    The corpus *mentions* "Special Assets"/"watchlist" in narrative (e.g. an RM's
    "watchlist trigger" plan); scanning tokens would wrongly halt healthy borrowers.
  - The free-text designation REDACTION scope (esp. whether an RM's own narrative
    "watchlist trigger" counts as a restricted designation — it interacts with the
    close-the-loop skill) is a POLICY-INTERPRETATION refinement still to settle with
    the user. For now we redact explicit designation phrasing in CSV notes only.
"""

import re

# §2.1 — hard-restricted structured field (internal credit rating: B+/BB-/A- …)
RESTRICTED_FIELDS = ("credit_grade",)

# §2.1 — explicit designation language to redact from surfaced free text
_REDACT_PATTERNS = [
    re.compile(r"\bspecial[\s-]*assets?\b", re.IGNORECASE),
    re.compile(r"\bwatch[\s-]*list(ed)?\b", re.IGNORECASE),
]
REDACTION_TAG = "[REDACTED §2.1]"

# §5 — borrowers in Special Assets / active litigation → no AI processing.
# STATUS-based (config / explicit status), not a token scan. None of the 5 qualify.
SPECIAL_ASSETS_BORROWERS = set()


class ComplianceRefusal(Exception):
    """Raised when policy forbids processing (e.g. §5 halt, or a guarantor doc)."""


def redact_text(text, log=None, field=None):
    """Redact §2.1 designation language; return (clean_text, pattern_hits)."""
    if not text:
        return text, []
    hits, out = [], text
    for pat in _REDACT_PATTERNS:
        if pat.search(out):
            hits.append(pat.pattern)
            out = pat.sub(REDACTION_TAG, out)
    if hits and log is not None:
        log.append({"action": "redact_text", "policy": "§2.1", "field": field, "patterns": hits})
    return out, hits


def strip_record(record, free_text_fields=(), log=None):
    """Return a copy with §2.1 restricted fields removed and free text redacted."""
    clean = dict(record)
    for f in RESTRICTED_FIELDS:
        if f in clean:
            clean.pop(f, None)
            if log is not None:
                log.append({"action": "strip_field", "policy": "§2.1", "field": f})
    for f in free_text_fields:
        if clean.get(f):
            clean[f], _ = redact_text(clean[f], log=log, field=f)
    return clean


def assert_processable(borrower, log=None):
    """§5 gate — STOP if the borrower is in Special Assets / active litigation."""
    if borrower in SPECIAL_ASSETS_BORROWERS:
        if log is not None:
            log.append({"action": "halt", "policy": "§5", "borrower": borrower})
        raise ComplianceRefusal(
            f"§5: '{borrower}' is in Special Assets or active litigation — AI processing not permitted."
        )


def refuse_if_guarantor_doc(doc_meta, log=None):
    """§2.1 — guarantor personal-financial documents must be refused, not read."""
    dtype = (doc_meta or {}).get("doc_type", "").lower()
    if "guarantor" in dtype and ("personal" in dtype or "financial" in dtype):
        if log is not None:
            log.append({"action": "refuse_doc", "policy": "§2.1", "doc_type": dtype})
        raise ComplianceRefusal(
            "§2.1: guarantor personal-financial documents may not be processed — refused, not read."
        )


# §4.2 — characterizing / predictive / recommending CREDIT language (NOT factual covenant status).
# These deliberately do NOT match factual statements like "covenant breach", "DSCR below the floor",
# or "revolver at 85%" — those are observed facts the RM may see; only credit *characterization*,
# *prediction*, and *recommendation* are forbidden.
_CREDIT_LANGUAGE_PATTERNS = [
    re.compile(r"\b(high(ly)?|elevated|increasing|significant)\s+(credit\s+)?risk\b", re.IGNORECASE),
    re.compile(r"\bcredit\s+risk\s+is\b", re.IGNORECASE),
    re.compile(r"\bcreditworth(y|iness)\b", re.IGNORECASE),
    re.compile(r"\blikely\s+to\s+(default|breach)\b", re.IGNORECASE),
    re.compile(r"\b(at\s+risk\s+of|expected\s+to)\s+(default|breach)\b", re.IGNORECASE),
    re.compile(r"\bprobability\s+of\s+default\b", re.IGNORECASE),
    re.compile(r"\b(poor|weak|strong|deteriorating|improving)\s+credit\s+(quality|profile|risk)\b", re.IGNORECASE),
    re.compile(r"\brisky\s+borrower\b", re.IGNORECASE),
    re.compile(
        r"\b(recommend|suggest|advise|should)\s+(approv|den(y|ie)|waiv|modif|restructur|downgrad|upgrad)", re.IGNORECASE
    ),
    re.compile(r"\b(risk\s+rating|risk\s+grade)\b", re.IGNORECASE),
]


def scan_credit_language(text):
    """§4.2 — return any credit-characterizing/predictive/recommending phrases found (factual status is not flagged)."""
    hits = []
    for pat in _CREDIT_LANGUAGE_PATTERNS:
        for m in pat.finditer(text or ""):
            hits.append(m.group(0).strip())
    return hits
