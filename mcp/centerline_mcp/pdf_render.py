"""render_pdf — turn a SCREENED artifact (markdown) into a credit-file-grade PDF.

Runs host-side (the MCP server is spawned on the Mac in both Code and Cowork), so the same renderer
produces the same PDF on both surfaces. It renders the text it is GIVEN — i.e. the `finalized_text`
returned by `screen_and_finalize`, which already carries the reliability footer and the §4.3 review tag —
so the DRAFT / "Requires RM review" banner and the footer are preserved in the PDF. The markdown artifact
is unchanged and still renders inline; the PDF is an ADDITIONAL output.

Deliberately a SMALL markdown subset — enough for our artifacts: H1/H2/H3 headings, paragraphs,
**bold** / *italic*, `- `/`* ` bullets, `1. ` numbered lists, GFM pipe tables (the covenant table), and
`---` rules. No external converter / system libs (reportlab only) — portable on the bridged host.
"""

import datetime
import html
import os
import re

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _resolve(path):
    return path if os.path.isabs(path) else os.path.join(_REPO, path)


def _stamped(path):
    """Append a UTC timestamp before the extension so every save is a unique file (no overwrites) and the
    files sort chronologically — e.g. reports/pdf/intake.pdf -> reports/pdf/intake_20260613T153012Z.pdf."""
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root, ext = os.path.splitext(path)
    return f"{root}_{stamp}{ext or '.pdf'}"


def _inline(text):
    """Escape HTML, then re-introduce reportlab's <b>/<i> for **bold** / *italic*. Source tags like
    `[financial_statement: ebitda_gaap]` are literal text and survive the escape untouched."""
    out = html.escape(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", out)
    return out


def _leading_h1(text):
    """True if the first non-empty line of the markdown is an H1 (`# ...`). When it is, that heading IS the
    title — so render_pdf must NOT also prepend the `title` arg, or the document title prints twice."""
    for ln in (text or "").splitlines():
        s = ln.strip()
        if s:
            return s.startswith("# ")
    return False


def _is_table_sep(line):
    s = line.strip()
    return bool(s) and set(s) <= set("|:- ") and "-" in s


def _split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def render_pdf(text, title=None, output_path=None, timestamp=True):
    """Render `text` (markdown) to a PDF. Returns {ok, path, bytes}. `output_path` is repo-relative
    (resolved on the host) or absolute; defaults under reports/pdf/. By default a UTC timestamp is appended
    to the filename so each save is a unique, chronologically-sortable file (set timestamp=False to write
    the exact name). The text is rendered verbatim — pass the finalized output from screen_and_finalize so
    the banner + reliability footer are preserved. `title` is used only when the body does not already begin
    with its own H1 (otherwise the title would print twice)."""
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        HRFlowable,
        ListFlowable,
        ListItem,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9.5, leading=13, alignment=TA_LEFT)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, leading=19, spaceBefore=4, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12.5, leading=16, spaceBefore=8, spaceAfter=4)
    h3 = ParagraphStyle("h3", parent=ss["Heading3"], fontSize=11, leading=14, spaceBefore=6, spaceAfter=3)
    cell = ParagraphStyle("cell", parent=body, fontSize=8.5, leading=11)
    cell_h = ParagraphStyle("cellh", parent=cell, textColor=colors.white)

    lines = (text or "").replace("\r\n", "\n").split("\n")
    flow = []
    i, n = 0, len(lines)

    def flush_para(buf):
        if buf:
            flow.append(Paragraph(_inline(" ".join(buf)), body))
            buf.clear()

    para = []
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # GFM pipe table: a row line followed by a separator line.
        if stripped.startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            flush_para(para)
            header = _split_row(stripped)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i].strip()))
                i += 1
            data = [[Paragraph(_inline(c), cell_h) for c in header]] + [
                [Paragraph(_inline(c), cell) for c in r] for r in rows
            ]
            tbl = Table(data, repeatRows=1, hAlign="LEFT")
            tbl.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9bb0c9")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f7")]),
                    ]
                )
            )
            flow.extend([tbl, Spacer(1, 6)])
            continue

        if not stripped:
            flush_para(para)
        elif stripped.startswith("### "):
            flush_para(para)
            flow.append(Paragraph(_inline(stripped[4:]), h3))
        elif stripped.startswith("## "):
            flush_para(para)
            flow.append(Paragraph(_inline(stripped[3:]), h2))
        elif stripped.startswith("# "):
            flush_para(para)
            flow.append(Paragraph(_inline(stripped[2:]), h1))
        elif set(stripped) <= set("-*_") and len(stripped) >= 3:
            flush_para(para)
            flow.append(
                HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#9bb0c9"), spaceBefore=4, spaceAfter=4)
            )
        elif re.match(r"^([-*]|\d+\.)\s+", stripped):
            flush_para(para)
            items, ordered = [], bool(re.match(r"^\d+\.\s+", stripped))
            while i < n and re.match(r"^([-*]|\d+\.)\s+", lines[i].strip()):
                item_text = re.sub(r"^([-*]|\d+\.)\s+", "", lines[i].strip())
                items.append(ListItem(Paragraph(_inline(item_text), body), leftIndent=12))
                i += 1
            flow.append(ListFlowable(items, bulletType="1" if ordered else "bullet", leftIndent=14))
            continue
        else:
            para.append(stripped)
        i += 1
    flush_para(para)

    target = output_path or "reports/pdf/artifact.pdf"
    abspath = _resolve(_stamped(target) if timestamp else target)
    os.makedirs(os.path.dirname(abspath), exist_ok=True)
    doc = SimpleDocTemplate(
        abspath,
        pagesize=LETTER,
        title=title or "Centerline artifact",
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
    )
    # Only prepend the title if the body doesn't already lead with its own H1 (else the title prints twice).
    if title and not _leading_h1(text):
        flow.insert(0, Spacer(1, 2))
        flow.insert(0, Paragraph(_inline(title), h1))
    doc.build(flow)
    size = os.path.getsize(abspath)
    return {
        "ok": True,
        "path": os.path.relpath(abspath, _REPO) if abspath.startswith(_REPO) else abspath,
        "bytes": size,
        "note": "PDF of the SCREENED artifact (banner + reliability footer preserved). The markdown is unchanged.",
    }
