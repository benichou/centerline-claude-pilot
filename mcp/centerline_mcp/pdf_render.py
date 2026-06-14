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


def render_pdf(text, title=None, output_path=None, timestamp=True, charts=None):
    """Render `text` (markdown) to a PDF. Returns {ok, path, bytes}. `output_path` is repo-relative
    (resolved on the host) or absolute; defaults under reports/pdf/. By default a UTC timestamp is appended
    to the filename so each save is a unique, chronologically-sortable file (set timestamp=False to write
    the exact name). The text is rendered verbatim — pass the finalized output from screen_and_finalize so
    the banner + reliability footer are preserved. `title` is used only when the body does not already begin
    with its own H1 (otherwise the title would print twice).

    `charts` (optional) renders STYLISH trend charts after the body — a list of
    {title, type: 'line'|'bar', labels: [...], series: [...], threshold?: float}. e.g. the Meridian DSCR
    trend (type 'line', threshold 1.20) or the engagement gaps (type 'bar'). Fed the deterministic series
    from get_loan_performance / detect_deterioration_signals."""
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.linecharts import HorizontalLineChart
    from reportlab.graphics.shapes import Drawing, String
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

    # --- Centerline Bank letterhead (commercial-bank convention: logo + name LEFT, descriptor RIGHT) ---
    _NAVY = colors.HexColor("#1f3a5f")
    _GOLD = colors.HexColor("#b8860b")
    _GREY = colors.HexColor("#5b6b7f")
    _RULE = colors.HexColor("#9bb0c9")

    def _letterhead(c, d):
        """Draw the Centerline Bank letterhead + footer on every page (vector — no image asset)."""
        c.saveState()
        w, h = d.pagesize
        left, right, topy = d.leftMargin, w - d.rightMargin, h - 0.5 * inch
        # mark: a navy rounded square with a white 'center line' through it + two gold rules (the wordplay)
        sz = 26
        mx, my = left, topy - sz + 4
        c.setFillColor(_NAVY)
        c.roundRect(mx, my, sz, sz, 4, fill=1, stroke=0)
        c.setStrokeColor(colors.white)
        c.setLineWidth(2)
        c.line(mx + 4, my + sz / 2, mx + sz - 4, my + sz / 2)
        c.setStrokeColor(_GOLD)
        c.setLineWidth(1)
        c.line(mx + 8, my + sz / 2 + 5, mx + sz - 8, my + sz / 2 + 5)
        c.line(mx + 8, my + sz / 2 - 5, mx + sz - 8, my + sz / 2 - 5)
        # wordmark
        tx = mx + sz + 10
        c.setFillColor(_NAVY)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(tx, topy - 9, "CENTERLINE BANK")
        c.setFillColor(_GREY)
        c.setFont("Helvetica", 7.5)
        c.drawString(tx, topy - 19, "COMMERCIAL BANKING")
        # right-aligned descriptor (honest: this is a synthetic pilot, not a real institution)
        c.drawRightString(right, topy - 9, "Relationship Management")
        c.drawRightString(right, topy - 19, "Synthetic pilot - not a real institution")
        # header rule
        c.setStrokeColor(_NAVY)
        c.setLineWidth(1.2)
        c.line(left, topy - 30, right, topy - 30)
        # footer rule + page number + confidentiality line
        c.setStrokeColor(_RULE)
        c.setLineWidth(0.5)
        c.line(left, 0.62 * inch, right, 0.62 * inch)
        c.setFillColor(_GREY)
        c.setFont("Helvetica", 7)
        c.drawString(left, 0.46 * inch, "Centerline Bank · Commercial Banking · CONFIDENTIAL (synthetic pilot data)")
        c.drawRightString(right, 0.46 * inch, "Page %d" % d.page)
        c.restoreState()

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

    # --- trend charts (optional) — reportlab.graphics line/bar, appended after the body ---
    def _chart_flowable(spec):
        d = Drawing(460, 168)
        d.add(String(0, 154, str(spec.get("title", "")), fontName="Helvetica-Bold", fontSize=9.5, fillColor=_NAVY))
        labels = [str(x) for x in (spec.get("labels") or [])]
        series = [v for v in (spec.get("series") or [])]
        if spec.get("type") == "bar":
            bc = VerticalBarChart()
            bc.x, bc.y, bc.width, bc.height = 30, 22, 410, 118
            bc.data = [series]
            bc.categoryAxis.categoryNames = labels
            bc.categoryAxis.labels.fontSize = 7
            bc.valueAxis.valueMin = 0
            bc.bars[0].fillColor = _NAVY
            d.add(bc)
        else:  # line (optional threshold rendered as a dashed second line)
            lc = HorizontalLineChart()
            lc.x, lc.y, lc.width, lc.height = 35, 24, 405, 116
            threshold = spec.get("threshold")
            lc.data = [series] + ([[threshold] * len(series)] if threshold is not None else [])
            lc.categoryAxis.categoryNames = labels
            lc.categoryAxis.labels.fontSize = 5
            lc.categoryAxis.labels.angle = 30
            lc.categoryAxis.labels.boxAnchor = "ne"
            lc.valueAxis.labels.fontSize = 6
            lc.lines[0].strokeColor = _NAVY
            lc.lines[0].strokeWidth = 1.5
            if threshold is not None:
                lc.lines[1].strokeColor = _GOLD
                lc.lines[1].strokeDashArray = [3, 2]
            vals = [v for v in series if isinstance(v, (int, float))] + (
                [threshold] if isinstance(threshold, (int, float)) else []
            )
            if vals:
                lo, hi = min(vals), max(vals)
                pad = (hi - lo) * 0.15 or (abs(hi) * 0.1 or 0.1)
                lc.valueAxis.valueMin, lc.valueAxis.valueMax = lo - pad, hi + pad
            d.add(lc)
        return d

    for spec in charts or []:
        try:
            flow.append(Spacer(1, 10))
            flow.append(_chart_flowable(spec))
        except Exception:  # noqa: BLE001 — a chart must never break the readout
            pass

    target = output_path or "reports/pdf/artifact.pdf"
    abspath = _resolve(_stamped(target) if timestamp else target)
    os.makedirs(os.path.dirname(abspath), exist_ok=True)
    doc = SimpleDocTemplate(
        abspath,
        pagesize=LETTER,
        title=title or "Centerline Bank artifact",
        author="Centerline Bank - Commercial Banking",
        topMargin=1.15 * inch,  # room for the letterhead
        bottomMargin=0.85 * inch,  # room for the footer
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
    )
    # Only prepend the title if the body doesn't already lead with its own H1 (else the title prints twice).
    if title and not _leading_h1(text):
        flow.insert(0, Spacer(1, 2))
        flow.insert(0, Paragraph(_inline(title), h1))
    doc.build(flow, onFirstPage=_letterhead, onLaterPages=_letterhead)
    size = os.path.getsize(abspath)
    return {
        "ok": True,
        "path": os.path.relpath(abspath, _REPO) if abspath.startswith(_REPO) else abspath,
        "bytes": size,
        "note": "PDF of the SCREENED artifact (banner + reliability footer preserved). The markdown is unchanged.",
    }
