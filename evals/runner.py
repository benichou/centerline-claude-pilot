"""Golden-set eval runner — stdlib only (no MCP SDK needed).

Loads the JSONL cases in evals/cases/, dispatches each to the REAL tool logic
(centerline_mcp.core / .guards), grades it against source-grounded expectations,
and writes evals/results/latest.md.

Run:  PYTHONPATH=mcp python3 evals/runner.py
      (also works as `python3 evals/runner.py` — it adds mcp/ to sys.path itself)

Tiers (see evals/GOLDEN.md):
  T1     objective ground truth (value verifiable from a source row)
  T1-neg negative ground truth (a clean borrower must NOT flag)
  T2     compliance assertion (binary/hard)
  T2-neg negative compliance (a normal doc must NOT be refused)

Exit code is non-zero if any case fails (CI-friendly).
"""

import datetime
import glob
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "mcp"))

from centerline_mcp import core, guards  # noqa: E402
from centerline_mcp import data_access as da  # noqa: E402

_CASES_DIR = os.path.join(_REPO, "evals", "cases")
_RESULTS_DIR = os.path.join(_REPO, "evals", "results")

# name -> callable. `tool` cases hit core (the MCP tool logic); `fn` cases hit guards directly.
_TOOLS = {
    "get_borrower_dossier": core.get_borrower_dossier,
    "get_loan_performance": core.get_loan_performance,
    "get_activity_log": core.get_activity_log,
    "get_emails": core.get_emails,
    "screen_and_finalize": core.screen_and_finalize,
    "check_covenant_compliance": core.check_covenant_compliance,
    "detect_deterioration_signals": core.detect_deterioration_signals,
    "measure_engagement_coverage": core.measure_engagement_coverage,
    "assemble_watchlist": core.assemble_watchlist,
}
_FNS = {"refuse_if_guarantor_doc": guards.refuse_if_guarantor_doc}
_EXC = {"ComplianceRefusal": guards.ComplianceRefusal}

_MISSING = object()


def _resolve(path, obj):
    """Resolve a dotted path. Supports `prefix[].suffix` (map suffix over a list) and integer
    indices. Returns _MISSING if any segment is absent (used by `absent` assertions)."""
    if "[]." in path:
        pre, post = path.split("[].", 1)
        base = _resolve(pre, obj)
        if base is _MISSING or not isinstance(base, list):
            return _MISSING
        return [_resolve(post, el) for el in base]
    cur = obj
    for seg in path.split("."):
        try:
            if isinstance(cur, list):
                cur = cur[int(seg)]
            elif isinstance(cur, dict):
                if seg not in cur:
                    return _MISSING
                cur = cur[seg]
            else:
                return _MISSING
        except (ValueError, IndexError, KeyError, TypeError):
            return _MISSING
    return cur


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _compare(actual, spec):
    """True if `actual` satisfies `spec`. Scalar spec = equality; dict spec = one comparator."""
    if isinstance(spec, dict):
        ((op, val),) = spec.items()
        try:
            if op == "contains":
                return val in actual
            if op == "excludes_ci":
                return val.lower() not in str(actual).lower()
            if op == "truthy":
                return bool(actual) == val
            if op == "len":
                return len(actual) == val
            if op == "minlen":
                return len(actual) >= val
            if op == "startswith":
                return str(actual).startswith(val)
            if op == "first_startswith":
                return len(actual) >= 1 and str(actual[0]).startswith(val)
            if op == "last_startswith":
                return len(actual) >= 1 and str(actual[-1]).startswith(val)
            if op == "gte":
                return actual >= val
            if op == "lte":
                return actual <= val
        except (TypeError, AttributeError):
            return False
        return False
    if _num(actual) and _num(spec):
        return abs(actual - spec) < 1e-9
    return actual == spec


def _dispatch(case):
    """Run the case's tool/fn (applying any setup), returning (result, raised_exception_or_None)."""
    name = case.get("tool") or case.get("fn")
    fn = _TOOLS.get(name) or _FNS.get(name)
    if fn is None:
        raise KeyError(f"unknown tool/fn: {name}")
    args = case.get("args", {})

    full = None
    if case.get("setup") == "special_assets":
        rows = da.match_borrower(args.get("borrower_name", ""), da.portfolio())
        full = rows[0]["borrower_name"] if rows else args.get("borrower_name")
        guards.SPECIAL_ASSETS_BORROWERS.add(full)
    try:
        return fn(**args), None
    except Exception as exc:  # noqa: BLE001 — eval harness records the exception type
        return None, exc
    finally:
        if full is not None:
            guards.SPECIAL_ASSETS_BORROWERS.discard(full)


def _grade(case):
    """Return (passed: bool, detail: str)."""
    expect_raise = case.get("raises")
    try:
        result, raised = _dispatch(case)
    except KeyError as e:
        return False, str(e)

    # raises-based cases (§5 halt, guarantor refusal)
    if expect_raise:
        if raised is None:
            return False, f"expected {expect_raise}, none raised"
        if not isinstance(raised, _EXC.get(expect_raise, ())):
            return False, f"expected {expect_raise}, got {type(raised).__name__}"
        return True, f"raised {expect_raise}"
    if raised is not None:
        return False, f"unexpected {type(raised).__name__}: {raised}"

    # absent assertions (a field must NOT be present)
    for path in case.get("absent", []):
        if _resolve(path, result) is not _MISSING:
            return False, f"{path} should be absent but resolved"

    # value expectations
    for path, spec in (case.get("expect") or {}).items():
        actual = _resolve(path, result)
        if actual is _MISSING:
            return False, f"{path} did not resolve"
        if not _compare(actual, spec):
            return False, f"{path}={actual!r} did not satisfy {spec!r}"
    return True, "ok"


def _load_cases():
    cases = []
    for fp in sorted(glob.glob(os.path.join(_CASES_DIR, "*.jsonl"))):
        with open(fp, encoding="utf-8") as fh:
            for ln in fh:
                ln = ln.strip()
                if ln:
                    cases.append(json.loads(ln))
    return cases


def run_all():
    """Run every case; return a list of result dicts (used by observability.py too)."""
    out = []
    for c in _load_cases():
        passed, detail = _grade(c)
        out.append(
            {
                "id": c["id"],
                "tier": c.get("tier", "?"),
                "prompt": c.get("prompt", "?"),
                "skill": c.get("skill", ""),
                "source": c.get("source", ""),
                "passed": passed,
                "detail": detail,
            }
        )
    return out


def _write_results(results):
    os.makedirs(_RESULTS_DIR, exist_ok=True)
    n = len(results)
    npass = sum(1 for r in results if r["passed"])
    today = datetime.date.today().isoformat()
    lines = [
        "# Eval results",
        "",
        f"_Generated {today} by `evals/runner.py` against the live `centerline_mcp` logic._",
        "",
        f"**{npass}/{n} cases passed.**",
        "",
        "Grading is deterministic: each case calls the real tool/guard and checks source-grounded",
        'expectations. "Accuracy" is a clean number only here (T1/T2 ground truth); generative quality',
        "(T4) is rubric + edit-rate, reported separately — never a fabricated single %.",
        "",
        "| Case | Tier | Prompt | Result | Detail |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        mark = "✅ PASS" if r["passed"] else "❌ FAIL"
        lines.append(f"| `{r['id']}` | {r['tier']} | {r['prompt']} | {mark} | {r['detail']} |")
    path = os.path.join(_RESULTS_DIR, "latest.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path, npass, n


if __name__ == "__main__":
    results = run_all()
    for r in results:
        print(("PASS " if r["passed"] else "FAIL "), f'[{r["tier"]}] {r["id"]}: {r["detail"]}')
    path, npass, n = _write_results(results)
    print(f"\n{npass}/{n} passed — wrote {os.path.relpath(path, _REPO)}")
    sys.exit(0 if npass == n else 1)
