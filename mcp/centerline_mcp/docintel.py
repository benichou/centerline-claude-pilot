"""Document-intelligence: classify + extract for the covenant-package PDFs.

Architecture (mirrors the rest of the system: the model reads, deterministic code decides):
  - `prescreen_section_2_1(path)` — DETERMINISTIC §2.1 gate on the filename/declared type, run BEFORE any API
    call. A guarantor personal-financial statement is refused here and never sent to a model.
  - `classify_document(path)` — calls the Anthropic API with the YAML+Jinja `classify` prompt, temp 0, and a
    Pydantic-forced tool schema -> a validated `Classification`.
  - `extract_document_fields(path, doc_type)` — dispatches to the per-type prompt + Pydantic model and forces
    that schema. `other` -> skipped (no schema); guarantor -> refused (defense in depth).
The extracted fields then feed deterministic recompute/cross-validate/completeness/quality (separate module).

API key comes from the environment (ANTHROPIC_API_KEY) — never committed. anthropic is imported lazily so the
server starts (and the deterministic prescreen/dispatch are testable) without a key or a network call.
"""

import base64
import os
from typing import List, Literal, Optional

from pydantic import BaseModel

from . import prompts

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_local_env():
    """Load KEY=VALUE lines from a gitignored repo-root `.env` into os.environ (only keys not already set).

    OPTIONAL by design — an absent `.env` is a silent no-op, so the server still starts for the
    deterministic tools (Track A, compliance, completeness/cross-validate) without any key. This keeps
    ANTHROPIC_API_KEY in `.env` (gitignored, the approved pattern) and OUT of `.mcp.json` /
    claude_desktop_config.json — and, because the bridged server is spawned on the host Mac in BOTH Code
    and Cowork, the same `.env` powers live classify/extract on both surfaces. (uv's `--env-file` was the
    obvious alternative but it hard-errors on a missing file, which would break the whole server.)
    """
    path = os.path.join(_REPO, ".env")
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key, val = key.strip(), val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val
    except OSError:
        pass


_load_local_env()
DEFAULT_MODEL = os.environ.get("CENTERLINE_DOCINTEL_MODEL", "claude-sonnet-4-6")

DocType = Literal[
    "covenant_compliance_certificate",
    "financial_statement",
    "ar_aging_report",
    "management_representation_letter",
    "guarantor_personal_financial_statement",
    "purchase_order",
    "financial_projections",
    "other",
]


# ---- Pydantic models (forced structured output) ----
class Classification(BaseModel):
    doc_type: DocType
    confidence: float
    rationale: str
    key_signals: List[str] = []
    is_restricted_personal_guarantor_info: bool = False


class AddBack(BaseModel):
    label: str
    amount: float


class CovenantCertificate(BaseModel):
    period_end: Optional[str] = None
    certified_dscr: Optional[float] = None
    dscr_min: Optional[float] = None
    certified_leverage: Optional[float] = None
    leverage_max: Optional[float] = None
    gaap_ebitda: Optional[float] = None
    adjusted_ebitda: Optional[float] = None
    addbacks: List[AddBack] = []
    total_funded_debt: Optional[float] = None
    total_debt_service: Optional[float] = None
    signed: bool = False
    signatory_name: Optional[str] = None
    signatory_title: Optional[str] = None
    signed_date: Optional[str] = None


class FinancialStatement(BaseModel):
    period: Optional[str] = None
    revenue_current: Optional[float] = None
    revenue_prior: Optional[float] = None
    ebitda_gaap: Optional[float] = None
    total_funded_debt: Optional[float] = None
    total_debt_service: Optional[float] = None
    accounts_receivable_net: Optional[float] = None


class ARaging(BaseModel):
    as_of: Optional[str] = None
    total_ar: Optional[float] = None
    current: Optional[float] = None
    d1_30: Optional[float] = None
    d31_60: Optional[float] = None
    d61_90: Optional[float] = None
    d90_plus: Optional[float] = None
    customer_names_present: bool = True


class RepLetter(BaseModel):
    letter_date: Optional[str] = None
    signed: bool = False
    signatory_name: Optional[str] = None
    signatory_title: Optional[str] = None
    signed_date: Optional[str] = None
    represents_covenant_compliance: bool = False


# doc_type -> (Pydantic model, prompt file name). Types absent here are not extracted.
SCHEMAS = {
    "covenant_compliance_certificate": (CovenantCertificate, "extract_covenant_compliance_certificate"),
    "financial_statement": (FinancialStatement, "extract_financial_statement"),
    "ar_aging_report": (ARaging, "extract_ar_aging_report"),
    "management_representation_letter": (RepLetter, "extract_management_representation_letter"),
}
_REFUSE_2_1 = "guarantor_personal_financial_statement"
_NO_EXTRACT = {"other", "purchase_order", "financial_projections", _REFUSE_2_1}


def _resolve(path):
    return path if os.path.isabs(path) else os.path.join(_REPO, path)


_DOC_EXTS = {".pdf", ".md", ".csv", ".txt", ".docx", ".xlsx"}


def list_documents(directory):
    """List the files in a directory HOST-SIDE so the agent can enumerate a package without guessing
    filenames or needing a Cowork sandbox grant (the MCP server runs on the host in both Code and Cowork,
    so it can read the real directory). `directory` is repo-relative (resolved against the repo root) or
    absolute. Hidden/dotfiles are skipped. Returns {directory, count, files:[{name, ext, is_document}],
    pdfs:[name...]} — `pdfs` is the convenience list the covenant-package review starts from."""
    abspath = _resolve(directory)
    if not os.path.isdir(abspath):
        return {"directory": directory, "error": f"not a directory: {directory}"}
    files = []
    for name in sorted(os.listdir(abspath)):
        full = os.path.join(abspath, name)
        if os.path.isfile(full) and not name.startswith("."):
            ext = os.path.splitext(name)[1].lower()
            files.append({"name": name, "ext": ext, "is_document": ext in _DOC_EXTS})
    return {
        "directory": directory,
        "count": len(files),
        "files": files,
        "pdfs": [f["name"] for f in files if f["ext"] == ".pdf"],
    }


def prescreen_section_2_1(path):
    """Deterministic §2.1 gate (filename/declared-type). Returns a refusal dict if the doc is a guarantor
    personal financial statement (so it is NEVER sent to a model), else None."""
    name = os.path.basename(path).lower()
    if "guarantor" in name and ("personal" in name or "pfs" in name) and "financ" in name:
        return {
            "path": os.path.basename(path),
            "refused": True,
            "policy": "§2.1",
            "doc_type": _REFUSE_2_1,
            "sent_to_model": False,
            "reason": "Guarantor personal financial statement — non-public personal financial information of an "
            "individual (§2.1). Refused on intake; not sent to any AI model.",
        }
    return None


def _read_pdf_b64(abspath):
    with open(abspath, "rb") as fh:
        return base64.standard_b64encode(fh.read()).decode("ascii")


def _call_structured(system, instruction, pdf_b64, model_cls, tool_name, api_model, max_tokens=2000):
    """One Anthropic call: PDF + instruction, forced to model_cls's JSON schema via tool_use; validate."""
    import anthropic  # lazy: only needed for a live call

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    resp = client.messages.create(
        model=api_model,
        max_tokens=max_tokens,
        temperature=0,
        system=system,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_b64},
                    },
                    {"type": "text", "text": instruction},
                ],
            }
        ],
        tools=[
            {
                "name": tool_name,
                "description": "Return the requested fields.",
                "input_schema": model_cls.model_json_schema(),
            }
        ],
        tool_choice={"type": "tool", "name": tool_name},
    )
    for block in resp.content:
        if getattr(block, "type", None) == "tool_use":
            return model_cls.model_validate(block.input)
    raise RuntimeError("model did not return a tool_use block")


def _confidence_band(confidence):
    """Qualitative band for the model's CLASSIFICATION confidence — a data-quality signal surfaced
    qualitatively. The skill narrates the band, NOT a numeric % (a % reads as a credit characterization,
    §4.2). Provenance for the classification itself is the rationale + key_signals already returned."""
    c = confidence or 0.0
    if c >= 0.85:
        return "high"
    if c >= 0.6:
        return "medium"
    return "low"


def classify_document(path, model=None):
    """Classify one document. Runs the §2.1 pre-screen first (no API for a guarantor doc); otherwise calls the
    Anthropic API with the YAML+Jinja `classify` prompt + the `Classification` schema (temp 0). The result
    carries provenance: the source `document`, the model's `rationale` + `key_signals`, and a qualitative
    `confidence_band` (high/medium/low) — so every classification is traceable, not just asserted."""
    refusal = prescreen_section_2_1(path)
    if refusal:
        return refusal
    abspath = _resolve(path)
    if not os.path.exists(abspath):
        return {"path": os.path.basename(path), "error": f"file not found: {path}"}
    system, instruction = prompts.render("classify")
    result = _call_structured(
        system, instruction, _read_pdf_b64(abspath), Classification, "classify", model or DEFAULT_MODEL
    )
    out = {
        "path": os.path.basename(path),
        "document": os.path.basename(path),
        "refused": False,
        "confidence_band": _confidence_band(result.confidence),
        **result.model_dump(),
    }
    if result.is_restricted_personal_guarantor_info or result.doc_type == _REFUSE_2_1:
        out.update(
            {
                "refused": True,
                "policy": "§2.1",
                "reason": "Classified as a guarantor personal financial statement — refuse extraction (§2.1).",
            }
        )
    return out


def extract_document_fields(path, doc_type, model=None):
    """Extract fields for a classified document. `other`/PO/projections -> skipped; guarantor -> refused (§2.1);
    otherwise dispatch to the per-type YAML+Jinja prompt + Pydantic model and force that schema."""
    if doc_type == _REFUSE_2_1:
        return {
            "path": os.path.basename(path),
            "extracted": None,
            "refused": True,
            "policy": "§2.1",
            "reason": "Guarantor personal financial statement — not extracted (§2.1).",
        }
    if doc_type in _NO_EXTRACT:
        return {
            "path": os.path.basename(path),
            "doc_type": doc_type,
            "extracted": None,
            "skipped": True,
            "reason": f"No extraction schema for document type '{doc_type}' — left unprocessed by design.",
        }
    if doc_type not in SCHEMAS:
        return {
            "path": os.path.basename(path),
            "error": f"unknown doc_type: {doc_type}",
            "known_types": sorted(SCHEMAS) + sorted(_NO_EXTRACT),
        }
    abspath = _resolve(path)
    if not os.path.exists(abspath):
        return {"path": os.path.basename(path), "error": f"file not found: {path}"}
    model_cls, prompt_name = SCHEMAS[doc_type]
    system, instruction = prompts.render(prompt_name)
    result = _call_structured(system, instruction, _read_pdf_b64(abspath), model_cls, "extract", model or DEFAULT_MODEL)
    return {"path": os.path.basename(path), "doc_type": doc_type, "skipped": False, "extracted": result.model_dump()}
