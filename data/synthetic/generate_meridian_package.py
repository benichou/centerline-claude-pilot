"""Generate the synthetic Meridian Fabrication covenant-package PDFs (Phase 3).

Fictional documents for the Centerline Claude pilot. They ENCODE facts already in the supplied data:
  - Meridian Fabrication LLC — precision contract manufacturer, Columbus, OH; CFO David Kwan; personal guaranty
    of David and Michelle Kwan; Centerline $8.5M facility (term + revolver), SOFR + 2.75%, maturing March 2027.
  - Real story: automotive-OEM softness drove revenue DOWN ~13% and EBITDA margin from ~14% to ~12%; the
    aerospace contract is the DELAYED recovery (PO still outstanding); revolver climbed toward 85%; elevated
    60–90 day A/R from two automotive customers on extended terms.
Staged on purpose (the demo beats):
  - covenant certificate CLAIMS DSCR 1.23 / leverage 3.76 (compliant) via a $2.0M EBITDA add-back bridge,
    while the attached unadjusted financials RECOMPUTE to DSCR 1.03 / leverage 4.50 (breach);
  - the certificate is SIGNED by David Kwan (with date); the management representation letter is UNSIGNED;
  - AR-aging customer names are withheld; the total ties to balance-sheet A/R;
  - a guarantor PERSONAL financial statement (David & Michelle Kwan) is included so §2.1 refuses it on intake.
Genuinely-outstanding items (aerospace PO, AR customer names, updated 12-month projections — the memo's
Feb-14 list) are NOT generated, so the completeness check fires.

Run:  uv run python data/synthetic/generate_meridian_package.py
"""

import os

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle

_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meridian-package")
_NAVY = colors.HexColor("#1F3A5F")
_STEEL = colors.HexColor("#5B7895")
_RED = colors.HexColor("#B23A3A")
_GREY = colors.HexColor("#6B7280")
_LIGHT = colors.HexColor("#EEF2F6")
_ADDR = "2750 Fabrication Drive · Columbus, OH 43204"


def _register_signature():
    """Register a cursive font for the handwritten signature; fall back gracefully."""
    for path, idx in [
        ("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 0),
        ("/System/Library/Fonts/Supplemental/Brush Script.ttf", None),
        ("/System/Library/Fonts/Supplemental/Apple Chancery.ttf", None),
    ]:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(
                    TTFont("Signature", path) if idx is None else TTFont("Signature", path, subfontIndex=idx)
                )
                return "Signature"
            except Exception:
                continue
    return "Helvetica-Oblique"


_SIG = _register_signature()

_styles = getSampleStyleSheet()
_H = ParagraphStyle("h", parent=_styles["Title"], fontSize=16, spaceAfter=2, textColor=_NAVY, alignment=0)
_SUB = ParagraphStyle("sub", parent=_styles["Normal"], fontSize=8.5, textColor=_GREY)
_BODY = ParagraphStyle("body", parent=_styles["Normal"], fontSize=9.3, leading=12.5)
_SMALL = ParagraphStyle("small", parent=_styles["Normal"], fontSize=7.6, textColor=_GREY, leading=10)
_SECT = ParagraphStyle("sect", parent=_styles["Heading2"], fontSize=10.5, spaceBefore=10, spaceAfter=3, textColor=_NAVY)
_SIGSTYLE = ParagraphStyle(
    "sig", parent=_styles["Normal"], fontName=_SIG, fontSize=26, leading=28, textColor=colors.HexColor("#13233a")
)


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(_LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(54, 40, LETTER[0] - 54, 40)
    canvas.setFillColor(_GREY)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(54, 31, "Meridian Fabrication LLC — Confidential")
    canvas.drawCentredString(LETTER[0] / 2, 31, "Prepared for Centerline Bank, N.A. — internal credit use only")
    canvas.drawRightString(LETTER[0] - 54, 31, f"Page {doc.page}")
    canvas.setFont("Helvetica", 5.8)
    canvas.drawString(
        54,
        22,
        "Submitted under the Credit Agreement dated March 31, 2022 (as amended), maturing March 31, 2027. "
        "Management-prepared and unaudited unless otherwise noted; subject to the lender's independent verification.",
    )
    canvas.restoreState()


def _doc(path, title):
    d = BaseDocTemplate(
        path, pagesize=LETTER, topMargin=50, bottomMargin=52, leftMargin=54, rightMargin=54, title=title
    )
    frame = Frame(d.leftMargin, d.bottomMargin, d.width, d.height, id="f")
    d.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=_footer)])
    return d


def _logo():
    dr = Drawing(40, 40)
    dr.add(Rect(0, 2, 38, 36, rx=4, ry=4, fillColor=_NAVY, strokeColor=None))
    dr.add(Rect(7, 9, 6, 22, fillColor=colors.white, strokeColor=None))
    dr.add(Rect(16, 9, 6, 22, fillColor=_STEEL, strokeColor=None))
    dr.add(Rect(25, 9, 6, 22, fillColor=colors.white, strokeColor=None))
    return dr


def _letterhead(subtitle):
    head = Table(
        [
            [
                _logo(),
                Paragraph(
                    "<b>MERIDIAN FABRICATION LLC</b><br/>"
                    f"<font size=7 color='#6B7280'>Precision Contract Manufacturing — Automotive &amp; "
                    f"Aerospace Components · {_ADDR} · EIN on file</font>",
                    _BODY,
                ),
            ]
        ],
        colWidths=[0.7 * inch, 5.6 * inch],
    )
    head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (1, 0), (1, 0), 8)]))
    return [head, Spacer(1, 4), Paragraph(subtitle, _SUB), Spacer(1, 8)]


def _money(n):
    return f"${n:,.0f}"


def _table(rows, col_widths, header=None, right_cols=(), bold_rows=(), total_rows=()):
    data = ([header] if header else []) + rows
    t = Table(data, colWidths=col_widths)
    style = [
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, _LIGHT]),
    ]
    if header:
        style += [
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 0), (-1, 0), _NAVY),
            ("TOPPADDING", (0, 0), (-1, 0), 4),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ]
    off = 1 if header else 0
    for c in right_cols:
        style.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    for r in bold_rows:
        style.append(("FONT", (0, r + off), (-1, r + off), "Helvetica-Bold", 8.6))
    for r in total_rows:
        style += [
            ("LINEABOVE", (0, r + off), (-1, r + off), 0.7, _NAVY),
            ("FONT", (0, r + off), (-1, r + off), "Helvetica-Bold", 8.8),
        ]
    t.setStyle(TableStyle(style))
    return t


def _bar(values, labels, title, color=_NAVY, width=320, height=150):
    dr = Drawing(width, height)
    dr.add(String(0, height - 10, title, fontName="Helvetica-Bold", fontSize=9, fillColor=_NAVY))
    bc = VerticalBarChart()
    bc.x, bc.y, bc.width, bc.height = 36, 22, width - 60, height - 48
    bc.data = [values]
    bc.categoryAxis.categoryNames = labels
    bc.categoryAxis.labels.fontSize = 7
    bc.valueAxis.valueMin = 0
    bc.valueAxis.labels.fontSize = 7
    bc.bars[0].fillColor = color
    bc.barWidth = 9
    dr.add(bc)
    return dr


def _pie(values, labels, title, width=210, height=150):
    dr = Drawing(width, height)
    dr.add(String(0, height - 10, title, fontName="Helvetica-Bold", fontSize=9, fillColor=_NAVY))
    p = Pie()
    p.x, p.y, p.width, p.height = 60, 18, 100, 100
    p.data = values
    p.labels = labels
    p.slices.fontSize = 6.5
    palette = [_NAVY, _STEEL, colors.HexColor("#9DB4C8"), colors.HexColor("#C8D6E2")]
    for i in range(len(values)):
        p.slices[i].fillColor = palette[i % len(palette)]
    dr.add(p)
    return dr


def _trend(series, floor, labels, title, width=340, height=160):
    dr = Drawing(width, height)
    dr.add(String(0, height - 10, title, fontName="Helvetica-Bold", fontSize=9, fillColor=_NAVY))
    lc = HorizontalLineChart()
    lc.x, lc.y, lc.width, lc.height = 36, 24, width - 60, height - 52
    lc.data = [series, [floor] * len(series)]
    lc.categoryAxis.categoryNames = labels
    lc.categoryAxis.labels.fontSize = 7
    lc.valueAxis.valueMin = 0.9
    lc.valueAxis.valueMax = 1.6
    lc.valueAxis.labels.fontSize = 7
    lc.lines[0].strokeColor = _NAVY
    lc.lines[0].strokeWidth = 2
    lc.lines[1].strokeColor = _RED
    lc.lines[1].strokeWidth = 1
    dr.add(lc)
    dr.add(String(width - 70, 30, "covenant floor 1.20", fontName="Helvetica", fontSize=6.5, fillColor=_RED))
    return dr


# ------------------------------------------------------------------ covenant compliance certificate (2 pages)
def covenant_certificate():
    d = _doc(os.path.join(_OUT, "meridian_covenant_compliance_certificate_Q1-2025.pdf"), "Compliance Certificate")
    el = _letterhead("COVENANT COMPLIANCE CERTIFICATE — fiscal quarter ended March 31, 2025")
    el += [
        Paragraph("COVENANT COMPLIANCE CERTIFICATE", _H),
        Paragraph(
            "Delivered pursuant to Section 6.02(a) of the Credit Agreement dated March 31, 2022 (as amended by "
            "the First Amendment dated November 8, 2024) between Meridian Fabrication LLC (the “Borrower”) and "
            "Centerline Bank, N.A., as lender. Facility: $8.5M senior secured (term loan plus revolving line), "
            "SOFR + 2.75%, maturing March 31, 2027.",
            _BODY,
        ),
        Spacer(1, 6),
        Paragraph(
            "The undersigned, the Chief Financial Officer of the Borrower, solely in such capacity and not "
            "personally, hereby certifies on behalf of the Borrower that: (a) the financial statements delivered "
            "herewith fairly present in all material respects the financial condition of the Borrower; (b) no "
            "Default or Event of Default has occurred and is continuing; and (c) the financial covenant "
            "calculations set forth below are true and correct as of the Calculation Date.",
            _BODY,
        ),
        Paragraph("Section A — Financial covenant summary", _SECT),
        _table(
            [
                ["6.10(a) Minimum DSCR", "≥ 1.20x", "1.23x", "0.03x", "In compliance"],
                ["6.10(b) Maximum Total Net Leverage", "≤ 4.00x", "3.76x", "0.24x", "In compliance"],
                ["6.10(c) Minimum Liquidity", "≥ $2,000k", "$2,310k", "$310k", "In compliance"],
                ["6.10(d) Maximum Capital Expenditures (FY)", "≤ $4,500k", "$3,180k", "$1,320k", "In compliance"],
            ],
            [2.5 * inch, 1.0 * inch, 0.9 * inch, 0.9 * inch, 1.1 * inch],
            header=["Covenant (§)", "Required", "Certified", "Headroom", "Status"],
            right_cols=(1, 2, 3),
        ),
        Spacer(1, 8),
        KeepTogether(
            [_bar([1.20, 1.23], ["Required", "Certified"], "DSCR — required vs certified (x)", width=250, height=140)]
        ),
        Paragraph("Section B — Adjusted EBITDA build (TTM) — bridge from GAAP", _SECT),
        _table(
            [
                ["Net income (GAAP)", "2,700"],
                ["  + Interest expense", "3,100"],
                ["  + Income tax", "900"],
                ["  + Depreciation & amortization", "3,400"],
                ["Reported (GAAP) EBITDA", "10,100"],
                ["  + Non-recurring legal & restructuring (§1.01 permitted)", "800"],
                ["  + Owner / management compensation normalization", "700"],
                ["  + Non-cash equity compensation", "300"],
                ["  + Pro-forma run-rate cost savings (run-rate basis)", "200"],
                ["Adjusted EBITDA (as certified)", "12,100"],
            ],
            [4.6 * inch, 1.6 * inch],
            right_cols=(1,),
            bold_rows=(4,),
            total_rows=(9,),
        ),
        Spacer(1, 6),
        Paragraph("Section C — Leverage & debt-service detail", _SECT),
        _table(
            [
                ["Revolving line of credit (drawn; $3,500 limit)", "2,975"],
                ["Current portion of long-term debt", "4,200"],
                ["Long-term debt (term loan, equipment notes & capital leases)", "38,275"],
                ["Total funded debt", "45,450"],
                ["Less: unrestricted cash", "(0)"],
                ["Total net debt", "45,450"],
                ["Total Net Leverage = Net debt / Adjusted EBITDA", "3.76x"],
                ["Cash interest paid (TTM)", "3,100"],
                ["Scheduled principal amortization (TTM)", "6,700"],
                ["Total debt service (TTM)", "9,800"],
                ["DSCR = Adjusted EBITDA / Total debt service", "1.23x"],
            ],
            [4.6 * inch, 1.6 * inch],
            right_cols=(1,),
            total_rows=(3, 9),
        ),
        Paragraph("Section D — Notes & explanation of variances", _SECT),
        Paragraph(
            "Revenue declined approximately 13% year-over-year on continued automotive-OEM order softness; two "
            "Tier-1 automotive customers moved to extended (75-day) payment terms at year-end, accounting for "
            "the majority of the 61–90 day receivables. The non-recurring legal & restructuring add-back "
            "($800k) relates to a supplier contract dispute settled in Q4 2024. Owner/management compensation "
            "normalization ($700k) adjusts above-market compensation paid to the managing members to a market "
            "rate consistent with §1.01. Revolver utilization rose to 85% of the line, primarily to fund a "
            "working-capital build; management expects the aerospace subassembly program to provide a recovery "
            "inflection as the related firm purchase order converts to shipments in the second half of 2025.",
            _BODY,
        ),
        Paragraph(
            "Capitalized terms have the meanings assigned in the Credit Agreement. EBITDA adjustments are "
            "limited to add-backs permitted under the definition of “Adjusted EBITDA” in §1.01.",
            _SMALL,
        ),
        Paragraph("Appendix A — Scheduled debt amortization (next four quarters)", _SECT),
        _table(
            [
                ["Q2 2025", "1,675", "760", "2,435", "40,800"],
                ["Q3 2025", "1,675", "740", "2,415", "39,125"],
                ["Q4 2025", "1,675", "720", "2,395", "37,450"],
                ["Q1 2026", "1,675", "700", "2,375", "35,775"],
            ],
            [1.1 * inch, 1.25 * inch, 1.1 * inch, 1.1 * inch, 1.35 * inch],
            header=["Period", "Principal", "Interest", "Total", "Ending balance"],
            right_cols=(1, 2, 3, 4),
        ),
        Spacer(1, 14),
        Paragraph(
            "IN WITNESS WHEREOF, the undersigned has executed this Certificate as of the date written below.", _BODY
        ),
        Spacer(1, 8),
        Paragraph("David Kwan", _SIGSTYLE),
        Paragraph("______________________________________", _BODY),
        Paragraph("<b>David Kwan</b> &nbsp;·&nbsp; Chief Financial Officer &nbsp;·&nbsp; Date: April 18, 2025", _BODY),
        Paragraph("Meridian Fabrication LLC &nbsp;·&nbsp; Calculation Date: March 31, 2025", _SMALL),
    ]
    d.build(el)


# --------------------------------------------------------------------- financial statements package (multi-page)
def financial_statement():
    d = _doc(os.path.join(_OUT, "meridian_financial_statement_Q1-2025.pdf"), "Financial Statements")
    el = _letterhead("FINANCIAL STATEMENTS (UNAUDITED, MANAGEMENT-PREPARED) — TTM ended March 31, 2025")
    el += [
        Paragraph("CONSOLIDATED FINANCIAL STATEMENTS", _H),
        Paragraph("Unaudited · prepared by management · USD in thousands · with comparative prior-year period", _SUB),
        Paragraph("Management discussion (summary)", _SECT),
        Paragraph(
            "Trailing-twelve-month revenue declined approximately 13% to $84.2M (from $96.5M) on continued "
            "automotive-OEM order softness; the Borrower’s two largest automotive customers ran below "
            "prior-year production volumes. EBITDA margin compressed from ~14% to ~12% ($10.1M, from $13.5M) as "
            "the fixed cost base — retained to stay ready for aerospace volume — did not scale with the revenue "
            "decline. Revolver utilization rose to 85% of the line, used to cover operating cash-flow shortfalls "
            "and a working-capital build. Management views the aerospace subassembly contract as the recovery "
            "driver, with first meaningful revenue now expected in the second half of 2025 (previously projected "
            "Q2 2024, then Q4 2024); the firm purchase order remains outstanding.",
            _BODY,
        ),
        Paragraph("Statement of Operations (trailing twelve months)", _SECT),
        _table(
            [
                ["Revenue", "84,200", "96,500"],
                ["Cost of goods sold", "(66,900)", "(74,800)"],
                ["Gross profit", "17,300", "21,700"],
                ["Selling, general & administrative", "(7,200)", "(8,190)"],
                ["EBITDA", "10,100", "13,510"],
                ["Depreciation & amortization", "(3,400)", "(3,200)"],
                ["Operating income (EBIT)", "6,700", "10,310"],
                ["Interest expense", "(3,100)", "(2,740)"],
                ["Income before taxes", "3,600", "7,570"],
                ["Income tax expense", "(900)", "(1,900)"],
                ["Net income", "2,700", "5,670"],
            ],
            [3.5 * inch, 1.45 * inch, 1.45 * inch],
            header=["($000s)", "TTM 3/31/25", "TTM 3/31/24"],
            right_cols=(1, 2),
            bold_rows=(2, 4, 6),
            total_rows=(10,),
        ),
        Spacer(1, 6),
        KeepTogether(
            [
                _trend(
                    [1.41, 1.33, 1.21, 1.10, 1.03],
                    1.20,
                    ["Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25"],
                    "DSCR trend (TTM, GAAP basis) vs covenant floor",
                    width=360,
                    height=160,
                )
            ]
        ),
        Paragraph("Balance Sheet (period end)", _SECT),
        _table(
            [
                ["Cash & equivalents", "1,500", "3,200"],
                ["Accounts receivable, net", "9,800", "8,600"],
                ["Inventory", "12,400", "10,800"],
                ["Other current assets", "1,100", "1,000"],
                ["Total current assets", "24,800", "23,600"],
                ["Property, plant & equipment, net", "41,000", "39,500"],
                ["Other assets", "2,200", "2,100"],
                ["Total assets", "68,000", "65,200"],
                ["Revolving line of credit (drawn; $3,500 limit)", "2,975", "1,800"],
                ["Current portion of long-term debt", "4,200", "3,900"],
                ["Accounts payable & accrued liabilities", "9,100", "8,500"],
                ["Total current liabilities", "16,275", "14,200"],
                ["Long-term debt (term, equipment notes & capital leases)", "38,275", "37,400"],
                ["Total liabilities", "54,550", "51,600"],
                ["Members’ equity", "13,450", "13,600"],
                ["Total funded debt (revolver + CPLTD + LTD)", "45,450", "43,100"],
            ],
            [3.5 * inch, 1.45 * inch, 1.45 * inch],
            header=["($000s)", "3/31/25", "3/31/24"],
            right_cols=(1, 2),
            bold_rows=(4, 7, 11, 13),
            total_rows=(15,),
        ),
        Spacer(1, 6),
        Paragraph("Statement of Cash Flows (TTM)", _SECT),
        _table(
            [
                ["Net income", "2,700"],
                ["Depreciation & amortization", "3,400"],
                ["Change in working capital (A/R & inventory build)", "(2,500)"],
                ["Cash from operating activities", "3,600"],
                ["Capital expenditures", "(3,180)"],
                ["Cash from investing activities", "(3,180)"],
                ["Net revolver borrowings", "1,175"],
                ["New equipment financing", "3,800"],
                ["Scheduled debt repayment", "(6,700)"],
                ["Distributions to members", "(395)"],
                ["Cash from financing activities", "(2,120)"],
                ["Net change in cash", "(1,700)"],
            ],
            [4.6 * inch, 1.6 * inch],
            right_cols=(1,),
            bold_rows=(3, 5, 10),
            total_rows=(11,),
        ),
        Spacer(1, 8),
        Paragraph("Appendix — quarterly trend (last five quarters)", _SECT),
        _table(
            [
                ["Revenue (quarter)", "22,500", "21,800", "20,900", "19,900", "19,000"],
                ["EBITDA (quarter)", "3,150", "2,900", "2,500", "2,150", "2,000"],
                ["DSCR (TTM, GAAP basis)", "1.41x", "1.33x", "1.21x", "1.10x", "1.03x"],
                ["Revolver utilization", "38%", "51%", "55%", "69%", "85%"],
            ],
            [1.7 * inch, 0.95 * inch, 0.95 * inch, 0.95 * inch, 0.95 * inch, 0.95 * inch],
            header=["($000s / ratio)", "Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25"],
            right_cols=(1, 2, 3, 4, 5),
        ),
        Paragraph("Notes to the financial statements", _SECT),
        Paragraph(
            "<b>Note 1 — Basis of presentation.</b> Unaudited; prepared by management in conformity with U.S. "
            "GAAP and excluding certain footnote disclosures required for audited statements. Comparative TTM "
            "prior-year figures are presented for trend analysis.",
            _SMALL,
        ),
        Paragraph(
            "<b>Note 2 — Debt.</b> The Centerline senior secured facility totals $8.5M — a $5.0M term loan and "
            "a $3.5M revolving line ($2.975M drawn at period end) — at SOFR + 2.75%, maturing March 2027, "
            "guaranteed by the managing members. Remaining funded debt comprises equipment term notes and "
            "capital leases on precision machining. Total funded debt was $45.45M.",
            _SMALL,
        ),
        Paragraph(
            "<b>Note 3 — Receivables.</b> A/R is stated net of a $0.4M allowance. See the accompanying "
            "accounts-receivable aging detail; one $0.1M invoice is under a quality dispute.",
            _SMALL,
        ),
        Paragraph(
            "<b>Note 4 — Revenue & customer concentration.</b> The two largest automotive customers each "
            "exceeded 10% of revenue and moved to extended 75-day terms at year-end. The aerospace subassembly "
            "program is pre-revenue; the related firm purchase order is outstanding.",
            _SMALL,
        ),
        Paragraph(
            "<b>Note 5 — Financial covenants.</b> The Credit Agreement requires a minimum DSCR of 1.20x and "
            "maximum total net leverage of 4.00x, tested quarterly. Management believes the Borrower was in "
            "compliance on an Adjusted-EBITDA basis as of the Calculation Date (see Compliance Certificate).",
            _SMALL,
        ),
        Paragraph(
            "<b>Note 6 — Related party.</b> Compensation paid to the managing members exceeded a market rate by "
            "approximately $0.7M during the period; this amount is normalized in the Adjusted-EBITDA calculation.",
            _SMALL,
        ),
        Paragraph(
            "<b>Note 7 — Commitments & contingencies.</b> A supplier contract dispute was settled in Q4 2024 "
            "($0.8M, non-recurring). The Borrower operates two facilities under operating leases expiring 2027–2030.",
            _SMALL,
        ),
        Paragraph(
            "<b>Note 8 — Liquidity & subsequent events.</b> At period end, availability under the revolving line "
            "was approximately $0.5M; management’s plans to restore liquidity center on the aerospace revenue "
            "inflection in the second half of 2025. Revolver utilization remained at ~85% subsequent to period end.",
            _SMALL,
        ),
    ]
    d.build(el)


# ------------------------------------------------------------------------------- AR aging (detail + charts)
def ar_aging():
    d = _doc(os.path.join(_OUT, "meridian_ar_aging_2025-03.pdf"), "AR Aging")
    el = _letterhead("ACCOUNTS RECEIVABLE AGING — DETAIL — as of March 31, 2025")
    el += [
        Paragraph("ACCOUNTS RECEIVABLE AGING — DETAIL", _H),
        Paragraph(
            "As of March 31, 2025 · USD in thousands · invoice-level · customer identities withheld at borrower’s request",
            _SUB,
        ),
        Spacer(1, 4),
        Table(
            [
                [
                    _bar(
                        [5200, 2100, 1300, 900, 300],
                        ["Current", "1-30", "31-60", "61-90", "90+"],
                        "Receivables by aging bucket ($000s)",
                        width=300,
                        height=150,
                    ),
                    _pie(
                        [3250, 2800, 2200, 1550],
                        ["Cust A", "Cust B", "Cust C", "Cust D"],
                        "By customer ($000s)",
                        width=210,
                        height=150,
                    ),
                ]
            ],
            colWidths=[3.2 * inch, 3.0 * inch],
        ),
        Spacer(1, 6),
        _table(
            [
                ["[WITHHELD] · INV-4471", "01/28/25", "1,900", "700", "300", "350", "—", "3,250"],
                ["[WITHHELD] · INV-4488", "01/15/25", "1,500", "600", "400", "200", "100", "2,800"],
                ["[WITHHELD] · INV-4502", "02/03/25", "1,000", "500", "350", "250", "100", "2,200"],
                ["[WITHHELD] · INV-4519", "02/22/25", "800", "300", "250", "100", "100", "1,550"],
                ["Total", "", "5,200", "2,100", "1,300", "900", "300", "9,800"],
            ],
            [1.9 * inch, 0.75 * inch, 0.7 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch, 0.5 * inch, 0.65 * inch],
            header=["Customer · Invoice", "Date", "Current", "1–30", "31–60", "61–90", "90+", "Total"],
            right_cols=(2, 3, 4, 5, 6, 7),
            total_rows=(4,),
        ),
        Spacer(1, 6),
        Paragraph(
            "Total accounts receivable: <b>$9,800k</b> (ties to balance-sheet A/R). 61–90 day balances total "
            "$900k (9.2% of A/R) and 90+ totals $300k (3.1%). Per the lender’s request, individual <b>customer "
            "identities have been withheld</b> and remain outstanding.",
            _BODY,
        ),
        Spacer(1, 8),
        Paragraph("Notes", _SECT),
        Paragraph(
            "(1) The two largest balances (customers withheld) are Tier-1 automotive customers granted extended "
            "75-day payment terms at year-end; these accounts drive the majority of the 61–90 day bucket. "
            "(2) One $100k invoice in the 90+ bucket is under a quality dispute and is not yet reserved. "
            "(3) Balances are stated before the $400k allowance for doubtful accounts recorded at the entity "
            "level. (4) Customer identities are withheld pending the Borrower’s consent and remain outstanding "
            "per the lender’s information request dated April 2, 2025.",
            _BODY,
        ),
        Spacer(1, 6),
        Paragraph("Appendix — customer concentration (identities withheld)", _SECT),
        _table(
            [
                ["Customer A — automotive Tier-1 (75-day terms)", "3,250", "33.2%"],
                ["Customer B — automotive OEM", "2,800", "28.6%"],
                ["Customer C", "2,200", "22.4%"],
                ["Customer D", "1,550", "15.8%"],
            ],
            [3.2 * inch, 1.3 * inch, 1.1 * inch],
            header=["Customer (withheld)", "Balance ($000s)", "% of A/R"],
            right_cols=(1, 2),
        ),
    ]
    d.build(el)


# ------------------------------------------------------------------- management representation letter (UNSIGNED)
def representation_letter():
    d = _doc(os.path.join(_OUT, "meridian_management_representation_letter.pdf"), "Management Representation Letter")
    el = _letterhead("MANAGEMENT REPRESENTATION LETTER — April 18, 2025")
    reps = [
        "We are responsible for the fair presentation of the financial statements in conformity with U.S. GAAP.",
        "We have made available all financial records and related data, and all minutes of meetings of the members and management.",
        "There have been no irregularities involving management or employees who have significant roles in internal control.",
        "All transactions have been recorded in the accounting records and are reflected in the financial statements.",
        "We have no knowledge of any fraud or suspected fraud affecting the entity.",
        "Receivables recorded represent valid claims and are net of an adequate allowance for doubtful accounts.",
        "Inventories are stated at the lower of cost or net realizable value.",
        "We have disclosed all liabilities, both actual and contingent, and all guarantees given to third parties.",
        "We have complied with all aspects of contractual agreements, including financial covenants, that would have a "
        "material effect on the financial statements in the event of non-compliance.",
        "We have disclosed all events subsequent to the balance sheet date that would require adjustment or disclosure.",
        "The financial statements include all required supporting schedules, including the schedule of debt and the "
        "accounts-receivable aging.",
        "We have disclosed all related-party transactions, including compensation paid to the managing members.",
        "There are no side agreements or undisclosed arrangements with customers affecting revenue recognition or the "
        "collectability of receivables.",
    ]
    el += [
        Paragraph("MANAGEMENT REPRESENTATION LETTER", _H),
        Paragraph("Centerline Bank, N.A. — Commercial Banking Division", _BODY),
        Spacer(1, 6),
        Paragraph(
            "This representation letter is provided in connection with your review of the financial statements of "
            "Meridian Fabrication LLC for the trailing twelve months ended March 31, 2025. We confirm, to the best "
            "of our knowledge and belief, the following representations:",
            _BODY,
        ),
        Spacer(1, 4),
    ]
    el += [Paragraph(f"{i + 1}.&nbsp;&nbsp;{r}", _BODY) for i, r in enumerate(reps)]
    el += [
        Spacer(1, 6),
        Paragraph(
            "Attachments referenced: (A) Compliance Certificate for the quarter ended March 31, 2025; "
            "(B) unaudited financial statements (TTM, with comparatives and notes); (C) accounts-receivable "
            "aging detail. This letter is to be executed by the Chief Financial Officer prior to release of the "
            "financial statements to the lender.",
            _SMALL,
        ),
        Spacer(1, 18),
        Paragraph("Sincerely,", _BODY),
        Spacer(1, 26),
        Paragraph("______________________________________", _BODY),
        Paragraph("<b>David Kwan</b> &nbsp;·&nbsp; Chief Financial Officer, Meridian Fabrication LLC", _BODY),
        Paragraph("Date: ______________", _BODY),
    ]
    d.build(el)


# ----------------------------------------------------------- guarantor personal financial statement (full SBA-413)
def guarantor_pfs():
    d = _doc(os.path.join(_OUT, "meridian_guarantor_personal_financial_statement.pdf"), "Personal Financial Statement")
    el = _letterhead("PERSONAL FINANCIAL STATEMENT — individual guarantors — as of March 31, 2025")
    el += [
        Paragraph("PERSONAL FINANCIAL STATEMENT", _H),
        Paragraph(
            "Individual guarantors (joint) · personal, non-business assets and liabilities · format patterned on "
            "SBA Form 413 · as of March 31, 2025",
            _SUB,
        ),
        Paragraph(
            "Names: <b>David Kwan</b> and <b>Michelle Kwan</b> (joint personal guaranty) &nbsp;·&nbsp; "
            "Residence: 18 Wexford Court, Columbus, OH 43221",
            _SMALL,
        ),
        Spacer(1, 4),
        Table(
            [
                [
                    _table(
                        [
                            ["Cash in banks & money market", _money(184_000)],
                            ["Savings / CDs", _money(96_000)],
                            ["Stocks & bonds (Sec. 3)", _money(612_000)],
                            ["Real estate owned (Sec. 4)", _money(1_350_000)],
                            ["Automobiles & personal property", _money(145_000)],
                            ["Retirement accounts (IRA/401k)", _money(870_000)],
                            ["Life insurance — cash surrender (Sec. 8)", _money(98_000)],
                            ["Total Assets", _money(3_355_000)],
                        ],
                        [1.9 * inch, 1.1 * inch],
                        header=["ASSETS", ""],
                        right_cols=(1,),
                        total_rows=(7,),
                    ),
                    _table(
                        [
                            ["Notes payable to banks (Sec. 2)", _money(52_000)],
                            ["Installment / auto", _money(38_000)],
                            ["Credit cards & revolving", _money(24_000)],
                            ["Mortgage — residence (Sec. 4)", _money(720_000)],
                            ["Mortgage — rental property", _money(310_000)],
                            ["Unpaid taxes (Sec. 6)", _money(0)],
                            ["Other liabilities (Sec. 7)", _money(15_000)],
                            ["Total Liabilities", _money(1_159_000)],
                        ],
                        [1.9 * inch, 1.1 * inch],
                        header=["LIABILITIES", ""],
                        right_cols=(1,),
                        total_rows=(7,),
                    ),
                ]
            ],
            colWidths=[3.1 * inch, 3.1 * inch],
        ),
        Spacer(1, 4),
        Paragraph("<b>Net worth (personal): $2,196,000</b>", _BODY),
        Paragraph("Section 1 — Source of income & contingent liabilities", _SECT),
        _table(
            [
                ["Salary (David Kwan)", _money(420_000), "As endorser or co-maker", _money(180_000)],
                ["Net investment / dividend income", _money(38_000), "Legal claims & judgments", _money(0)],
                ["Real estate (rental) income", _money(46_000), "Provision for federal income tax", _money(22_000)],
                ["Other income", _money(0), "Other special debt", _money(0)],
            ],
            [1.9 * inch, 1.1 * inch, 1.9 * inch, 1.1 * inch],
            right_cols=(1, 3),
            header=["Source of income (annual)", "", "Contingent liabilities", ""],
        ),
        Paragraph("Section 3 — Stocks & bonds (schedule)", _SECT),
        _table(
            [
                ["Public equities (diversified brokerage)", "412,000", "478,000"],
                ["Municipal bonds (State of Ohio)", "120,000", "134,000"],
                ["Total securities", "532,000", "612,000"],
            ],
            [3.0 * inch, 1.4 * inch, 1.4 * inch],
            header=["Security", "Cost", "Market value"],
            right_cols=(1, 2),
            total_rows=(2,),
        ),
        Paragraph("Section 4 — Real estate owned (schedule)", _SECT),
        _table(
            [
                ["Primary residence — Columbus, OH", "2013", _money(1_350_000), _money(720_000)],
                ["Rental property — Dublin, OH", "2019", _money(465_000), _money(310_000)],
            ],
            [2.6 * inch, 0.8 * inch, 1.4 * inch, 1.4 * inch],
            right_cols=(2, 3),
            header=["Property", "Acquired", "Market value", "Mortgage balance"],
        ),
        Spacer(1, 6),
        Paragraph(
            "General information: U.S. citizens; dates of birth on file; David Kwan is employed as Chief "
            "Financial Officer of Meridian Fabrication LLC; Michelle Kwan in operations. Banking relationships: "
            "Columbus Community Bank (personal checking & money market); Centerline Bank, N.A. (residence "
            "mortgage).",
            _SMALL,
        ),
        Paragraph(
            "We certify that the foregoing is true and complete as of the date stated, and authorize the lender "
            "to verify the information and to obtain consumer/credit reports in connection with our personal "
            "guaranty of the obligations of Meridian Fabrication LLC.",
            _SMALL,
        ),
        Spacer(1, 12),
        Paragraph(
            "Signature (David Kwan): ____________________  Date: ______     "
            "Signature (Michelle Kwan): ____________________  Date: ______",
            _SMALL,
        ),
        Spacer(1, 8),
        Paragraph(
            "CONFIDENTIAL — contains non-public personal financial information of individuals, furnished to the "
            "lender in connection with a personal guaranty.",
            _SMALL,
        ),
    ]
    d.build(el)


def certificate_of_insurance():
    """A misfiled document — a Certificate of Liability Insurance (ACORD-style) accidentally included in the
    package. Should classify as `other` (NOT the covenant compliance certificate) and be skipped — no extraction."""
    from reportlab.platypus import SimpleDocTemplate

    path = os.path.join(_OUT, "meridian_certificate_of_insurance.pdf")

    def coi_footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(_LIGHT)
        canvas.setLineWidth(0.5)
        canvas.line(54, 40, LETTER[0] - 54, 40)
        canvas.setFillColor(_GREY)
        canvas.setFont("Helvetica", 6.5)
        canvas.drawString(54, 30, "ACORD 25 (2016/03) — Certificate of Liability Insurance")
        canvas.drawRightString(LETTER[0] - 54, 30, f"Page {doc.page}")
        canvas.restoreState()

    d = SimpleDocTemplate(
        path,
        pagesize=LETTER,
        topMargin=50,
        bottomMargin=48,
        leftMargin=54,
        rightMargin=54,
        title="Certificate of Liability Insurance",
    )
    el = [
        Paragraph("CERTIFICATE OF LIABILITY INSURANCE", _H),
        Paragraph("Date issued: 03/15/2025", _SUB),
        Spacer(1, 4),
        Paragraph(
            "THIS CERTIFICATE IS ISSUED AS A MATTER OF INFORMATION ONLY AND CONFERS NO RIGHTS UPON THE "
            "CERTIFICATE HOLDER. THIS CERTIFICATE DOES NOT AFFIRMATIVELY OR NEGATIVELY AMEND, EXTEND OR ALTER "
            "THE COVERAGE AFFORDED BY THE POLICIES BELOW.",
            _SMALL,
        ),
        Spacer(1, 8),
        Table(
            [
                [
                    Paragraph(
                        "<b>Producer</b><br/>Buckeye Commercial Insurance Group<br/>411 Statehouse Ave, "
                        "Columbus, OH 43215<br/>(614) 555-0143 · certs@buckeyecig.com",
                        _BODY,
                    ),
                    Paragraph(
                        "<b>Insured</b><br/>Meridian Fabrication LLC<br/>2750 Fabrication Drive<br/>"
                        "Columbus, OH 43204",
                        _BODY,
                    ),
                ]
            ],
            colWidths=[3.1 * inch, 3.1 * inch],
        ),
        Spacer(1, 6),
        Paragraph("Insurers affording coverage", _SECT),
        _table(
            [
                ["A", "Hartford Fire Insurance Company", "19682"],
                ["B", "Travelers Property Casualty Co. of America", "25674"],
                ["C", "Ohio Casualty Insurance Company", "24074"],
            ],
            [0.5 * inch, 4.0 * inch, 1.4 * inch],
            header=["Insurer", "Carrier", "NAIC #"],
        ),
        Paragraph("Coverages", _SECT),
        _table(
            [
                [
                    "A",
                    "Commercial General Liability",
                    "GL-4471882",
                    "06/01/2024",
                    "06/01/2025",
                    "Each occ. $1,000,000 · Gen. agg. $2,000,000",
                ],
                [
                    "B",
                    "Automobile Liability (any auto)",
                    "BA-9920147",
                    "06/01/2024",
                    "06/01/2025",
                    "Combined single limit $1,000,000",
                ],
                [
                    "C",
                    "Umbrella / Excess Liability",
                    "UMB-330271",
                    "06/01/2024",
                    "06/01/2025",
                    "Each occurrence $5,000,000",
                ],
                [
                    "B",
                    "Workers’ Compensation & Employers’ Liability",
                    "WC-7741209",
                    "06/01/2024",
                    "06/01/2025",
                    "Statutory · E.L. each accident $1,000,000",
                ],
                [
                    "A",
                    "Property — Building & Equipment",
                    "PR-5510338",
                    "06/01/2024",
                    "06/01/2025",
                    "Blanket limit $12,000,000 · replacement cost",
                ],
            ],
            [0.45 * inch, 1.9 * inch, 1.0 * inch, 0.85 * inch, 0.85 * inch, 1.5 * inch],
            header=["Ins.", "Type of insurance", "Policy #", "Eff.", "Exp.", "Limits"],
        ),
        Spacer(1, 8),
        Paragraph("Certificate holder", _SECT),
        Paragraph(
            "Centerline Bank, N.A., its successors and/or assigns, as Lender and Loss Payee<br/>"
            "Commercial Banking Division · 200 Market Street, Hartford, CT",
            _BODY,
        ),
        Spacer(1, 10),
        Paragraph(
            "Should any of the above-described policies be cancelled before the expiration date thereof, "
            "notice will be delivered in accordance with the policy provisions. Lender is named as loss payee "
            "and additional insured per the terms of the loan and security agreement.",
            _SMALL,
        ),
        Spacer(1, 10),
        Paragraph(
            "Authorized representative: ____________________________  (Buckeye Commercial Insurance Group)", _SMALL
        ),
    ]
    d.build(el, onFirstPage=coi_footer, onLaterPages=coi_footer)


def _index():
    lines = [
        "# Meridian Fabrication LLC — Q1 2025 covenant package (SYNTHETIC)",
        "",
        "> **All documents in this folder are SYNTHETIC** — fictional samples for the Centerline Claude pilot.",
        "> They encode facts already in the supplied data (David Kwan CFO; Columbus, OH; David & Michelle Kwan",
        "> guarantors; automotive-OEM softness + delayed aerospace recovery; the breach). No real borrower.",
        "> The PDFs are unstamped so they read like real bank documents; the SYNTHETIC label lives here.",
        "",
        "## Received (in this folder)",
        "| File | Declared type | Staged condition |",
        "|---|---|---|",
        "| `meridian_covenant_compliance_certificate_Q1-2025.pdf` | covenant_compliance_certificate | SIGNED (David Kwan, CFO); certifies DSCR 1.23 / lev 3.76 via a $2.0M add-back bridge (overstated; recompute = 1.03 / 4.50 breach) |",
        "| `meridian_financial_statement_Q1-2025.pdf` | financial_statement | comparative 3-statement + DSCR-trend chart; GAAP EBITDA recomputes to DSCR 1.03 / leverage 4.50 |",
        "| `meridian_ar_aging_2025-03.pdf` | ar_aging_report | invoice-level + charts; automotive customer names WITHHELD; total $9,800k ties to balance-sheet A/R |",
        "| `meridian_management_representation_letter.pdf` | management_representation_letter | UNSIGNED (David Kwan named as signatory; signature/date blank) |",
        "| `meridian_guarantor_personal_financial_statement.pdf` | guarantor_personal_financial_statement | David & Michelle Kwan — **§2.1: refuse on intake** |",
        "| `meridian_certificate_of_insurance.pdf` | **other** | misfiled (ACORD Certificate of *Insurance*, not a covenant cert) — should classify `other` and be **skipped, not extracted** |",
        "",
        "## Required but still outstanding (NOT in this folder — completeness should flag these; the memo's Feb-14 list)",
        "- aerospace firm purchase order",
        "- accounts-receivable customer names (the 60–90 day automotive balances)",
        "- updated 12-month cash-flow projections (assumptions stated)",
    ]
    with open(os.path.join(_OUT, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    os.makedirs(_OUT, exist_ok=True)
    covenant_certificate()
    financial_statement()
    ar_aging()
    representation_letter()
    guarantor_pfs()
    certificate_of_insurance()
    _index()
    print(f"signature font: {_SIG}")
    print(f"wrote 6 PDFs + INDEX.md to {os.path.relpath(_OUT)}")


if __name__ == "__main__":
    main()
