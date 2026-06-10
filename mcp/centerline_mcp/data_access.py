"""Read-only access to the operational corpus in data/ (the ONLY thing served)."""
import csv
import os
from pathlib import Path


def data_dir():
    env = os.environ.get("CENTERLINE_DATA_DIR")
    if env:
        return Path(env)
    # this file: mcp/centerline_mcp/data_access.py  ->  repo_root/data
    return Path(__file__).resolve().parents[2] / "data"


def _read_csv(name):
    path = data_dir() / "structured" / name
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def portfolio():
    return _read_csv("portfolio_reference.csv")


def loan_performance():
    return _read_csv("loan_performance_monthly.csv")


def activity_log():
    return _read_csv("rm_activity_log.csv")


def _norm(s):
    return (s or "").strip().lower()


def match_borrower(name, rows, field="borrower_name"):
    """Match on exact name, first-token equality, or substring (borrower names share
    no first token, so first-token match is reliable here)."""
    n = _norm(name)
    if not n:
        return []
    nt = n.split()[0]
    out = []
    for r in rows:
        rv = _norm(r.get(field))
        if rv == n or (rv and rv.split()[0] == nt) or n in rv:
            out.append(r)
    return out


def list_borrowers():
    return [r["borrower_name"] for r in portfolio()]


def memo_path_for(borrower):
    """Locate an input relationship memo for a borrower under data/memos/<type>/."""
    d = data_dir() / "memos"
    if not d.exists():
        return None
    first = _norm(borrower).split()[0] if borrower else ""
    for p in d.rglob("*.md"):
        if first and first in p.stem.lower():
            return p
    return None


def emails_for(borrower):
    """Read the email thread (markdown) for a borrower under data/emails/, by first-token match."""
    d = data_dir() / "emails"
    if not d.exists():
        return None
    first = _norm(borrower).split()[0] if borrower else ""
    for p in sorted(d.glob("*.md")):
        if first and first in p.stem.lower():
            return p.read_text(encoding="utf-8")
    return None
