"""Professional branded PDF report generator — premium redesign.

Uses ReportLab BaseDocTemplate with PageTemplate for per-page headers/footers.

Layout:
 - Cover page: dark gradient panel, candidate scores, branding
 - Per-page header: purple strip with logo + page number
 - Coloured section banners for clear visual hierarchy
 - Score bar cards (ATS + JD Match)
 - Skill chip groups (detected / matched / missing / roles)
 - AI Review + JD Analysis as styled body text
 - Interview Questions as numbered cards per category
 - Footer strip on every page
"""
import re
import html
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak, KeepTogether,
)
from reportlab.platypus.flowables import Flowable


# ── Page dimensions ──────────────────────────────────────────────────────────
W, H      = A4            # 210 × 297 mm
LM = RM   = 18 * mm
TM        = 24 * mm       # top margin (below header strip)
BM        = 18 * mm
HEADER_H  = 14 * mm
FOOTER_H  = 10 * mm

# ── Brand palette ────────────────────────────────────────────────────────────
C_PRIMARY   = colors.HexColor("#7C3AED")
C_SECONDARY = colors.HexColor("#4F46E5")
C_ACCENT    = colors.HexColor("#A78BFA")
C_TEAL      = colors.HexColor("#0EA5E9")
C_SUCCESS   = colors.HexColor("#10B981")
C_DANGER    = colors.HexColor("#EF4444")
C_AMBER     = colors.HexColor("#F59E0B")
C_DARK      = colors.HexColor("#0F172A")
C_DARK2     = colors.HexColor("#1E293B")
C_MUTED     = colors.HexColor("#64748B")
C_LIGHT     = colors.HexColor("#F1F5F9")
C_WHITE     = colors.white
C_BORDER    = colors.HexColor("#E2E8F0")
C_CHIP_BG   = colors.HexColor("#312E81")   # deep indigo for chips
C_SECTION   = colors.HexColor("#EDE9FE")   # light lavender section bg


# ── Style sheet ──────────────────────────────────────────────────────────────
def _build_styles():
    base = getSampleStyleSheet()
    return {
        # Cover page hero text
        "CoverTitle": ParagraphStyle(
            "CoverTitle", parent=base["Title"],
            fontName="Helvetica-Bold", fontSize=30,
            textColor=C_WHITE, alignment=TA_CENTER, spaceAfter=6,
        ),
        "CoverSub": ParagraphStyle(
            "CoverSub", parent=base["Normal"],
            fontName="Helvetica", fontSize=13,
            textColor=C_ACCENT, alignment=TA_CENTER, spaceAfter=4,
        ),
        "CoverMeta": ParagraphStyle(
            "CoverMeta", parent=base["Normal"],
            fontName="Helvetica", fontSize=9,
            textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=0,
        ),
        # Score display
        "ScoreBig": ParagraphStyle(
            "ScoreBig", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=42, leading=48,
            alignment=TA_CENTER, spaceAfter=0,
        ),
        "ScoreTagline": ParagraphStyle(
            "ScoreTagline", parent=base["Normal"],
            fontName="Helvetica", fontSize=9, leading=12,
            textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=0,
        ),

        # Section banner text
        "SectionBanner": ParagraphStyle(
            "SectionBanner", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=12,
            textColor=C_WHITE, alignment=TA_LEFT, spaceAfter=0,
        ),

        # Body text
        "Body": ParagraphStyle(
            "Body", parent=base["BodyText"],
            fontName="Helvetica", fontSize=10,
            textColor=C_DARK2, leading=16, spaceAfter=3,
        ),
        "BodyBold": ParagraphStyle(
            "BodyBold", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=10,
            textColor=C_DARK2, spaceAfter=2,
        ),
        "BodyMuted": ParagraphStyle(
            "BodyMuted", parent=base["Normal"],
            fontName="Helvetica", fontSize=9,
            textColor=C_MUTED, spaceAfter=2,
        ),

        # Score label
        "ScoreLabel": ParagraphStyle(
            "ScoreLabel", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=10,
            textColor=C_DARK2, spaceAfter=1,
        ),
        "ScoreNum": ParagraphStyle(
            "ScoreNum", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=22,
            textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=0,
        ),

        # Question item
        "QNum": ParagraphStyle(
            "QNum", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=10,
            textColor=C_PRIMARY, spaceAfter=0,
        ),
        "QText": ParagraphStyle(
            "QText", parent=base["Normal"],
            fontName="Helvetica", fontSize=10,
            textColor=C_DARK2, leading=15, spaceAfter=0,
        ),

        # Footer/Header
        "HdrLeft": ParagraphStyle(
            "HdrLeft", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=9,
            textColor=C_WHITE,
        ),
        "HdrRight": ParagraphStyle(
            "HdrRight", parent=base["Normal"],
            fontName="Helvetica", fontSize=8,
            textColor=C_ACCENT, alignment=TA_RIGHT,
        ),
        "FooterText": ParagraphStyle(
            "FooterText", parent=base["Normal"],
            fontName="Helvetica", fontSize=8,
            textColor=C_MUTED, alignment=TA_CENTER,
        ),
    }


# ── Per-page canvas callback ──────────────────────────────────────────────────
def _on_page(canvas, doc):
    """Draw the header strip and footer on every page except the cover."""
    canvas.saveState()
    page_num = doc.page

    if page_num == 1:
        # Cover page — no header strip
        canvas.restoreState()
        return

    # Header strip
    canvas.setFillColor(C_PRIMARY)
    canvas.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)

    # Logo text left
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(C_WHITE)
    canvas.drawString(LM, H - HEADER_H + 4 * mm, "AI Resume Analyzer Pro")

    # Page number right
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_ACCENT)
    canvas.drawRightString(W - RM, H - HEADER_H + 4 * mm, f"Page {page_num}")

    # Footer
    canvas.setFillColor(C_BORDER)
    canvas.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(C_MUTED)
    canvas.drawCentredString(
        W / 2, FOOTER_H / 2 - 1 * mm,
        "Generated by AI Resume Analyzer Pro  ·  Powered by Groq LLM  ·  Confidential"
    )

    canvas.restoreState()


# ── Helper: section banner ────────────────────────────────────────────────────
def _section_banner(title: str, icon: str = "▸", color=None, styles=None) -> Table:
    """Coloured banner row used as a section header."""
    color = color or C_PRIMARY
    s = styles
    banner_para = Paragraph(f"{icon}  {title}", s["SectionBanner"])
    t = Table([[banner_para]], colWidths=[W - LM - RM])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), color),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t


# ── Helper: score card ────────────────────────────────────────────────────────
def _score_card(label: str, score: int, bar_color, styles) -> Table:
    """A rounded card with label, large score number, and progress bar."""
    s = styles
    pct       = max(1, min(100, score))
    bar_w     = (W - LM - RM - 24) / 2   # half the content width for side-by-side

    # Progress bar as a two-cell table
    filled_w = bar_w * pct / 100
    empty_w  = bar_w - filled_w
    bar = Table(
        [["", ""]],
        colWidths=[filled_w, max(0.5, empty_w)],
        rowHeights=[5 * mm],
    )
    bar.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0), bar_color),
        ("BACKGROUND",    (1, 0), (1, 0), C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("ROUNDEDCORNERS", [3]),
    ]))

    inner = Table(
        [
            [Paragraph(label, s["ScoreLabel"])],
            [Paragraph(f"{score}%", s["ScoreNum"])],
            [bar],
        ],
        colWidths=[bar_w],
    )
    inner.setStyle(TableStyle([
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))

    card = Table([[inner]], colWidths=[bar_w + 24])
    card.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_SECTION),
        ("BOX",           (0, 0), (-1, -1), 1, C_ACCENT),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return card


# ── Helper: skill chips ───────────────────────────────────────────────────────
def _skill_chips(skills: list, chip_color: colors.Color, text_color=None, story=None, styles=None):
    """Render skills as coloured pill badges, 4 per row."""
    if not skills:
        return
    text_color = text_color or C_WHITE
    s          = styles

    chip_style = ParagraphStyle(
        "chip", fontName="Helvetica-Bold", fontSize=8,
        textColor=text_color, alignment=TA_CENTER,
    )

    chips = [Paragraph(html.escape(skill), chip_style) for skill in skills]
    COLS  = 4
    rows  = []
    for i in range(0, len(chips), COLS):
        row = chips[i:i + COLS]
        # Pad to COLS so TableStyle applies evenly
        while len(row) < COLS:
            row.append(Paragraph("", chip_style))
        rows.append(row)

    col_w = (W - LM - RM) / COLS
    t = Table(rows, colWidths=[col_w] * COLS)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), chip_color),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [chip_color]),
        ("GRID",          (0, 0), (-1, -1), 0.5, C_WHITE),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(t)
    story.append(Spacer(1, 3 * mm))


# ── Helper: markdown cleaner ─────────────────────────────────────────────────
def _clean_md(text: str) -> str:
    """Convert markdown to minimal ReportLab-safe XML."""
    text = html.escape(text)
    text = text.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    text = text.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = re.sub(r"^[-*•]\s+", "• ", text)
    return text.strip()


# ── Helper: render markdown body ─────────────────────────────────────────────
def _render_body(text: str, story: list, styles: dict):
    """Parse multi-line markdown text into styled Paragraph elements."""
    s = styles
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 1.5 * mm))
            continue
        # Detect list items
        if re.match(r"^[-*•]\s+", stripped):
            cleaned = re.sub(r"^[-*•]\s+", "", stripped)
            story.append(Paragraph(f"<bullet>&bull;</bullet> {_clean_md(cleaned)}", s["Body"]))
        # Numbered list items
        elif re.match(r"^\d+\.\s+", stripped):
            story.append(Paragraph(_clean_md(stripped), s["Body"]))
        # Sub-headers (bold lines)
        elif stripped.startswith("##"):
            banner_text = stripped.lstrip("#").strip()
            story.append(Spacer(1, 2 * mm))
            story.append(Paragraph(f"<b>{html.escape(banner_text)}</b>", s["BodyBold"]))
            story.append(HRFlowable(width="100%", color=C_ACCENT, thickness=0.5))
        else:
            story.append(Paragraph(_clean_md(stripped), s["Body"]))


# ── Helper: interview question cards ─────────────────────────────────────────
def _render_questions(text: str, story: list, styles: dict):
    """Render interview questions with category banners and numbered rows."""
    s = styles
    CATEGORY_COLORS = {
        "Easy":       C_SUCCESS,
        "Medium":     C_AMBER,
        "Hard":       C_DANGER,
        "Technical":  C_SECONDARY,
        "Behavioral": C_TEAL,
        "HR":         C_PRIMARY,
    }

    current_cat = None
    q_num       = 0

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        # Category header  ## Easy Questions
        if stripped.startswith("##"):
            cat_text = stripped.lstrip("#").strip()
            # Identify colour
            cat_color = C_PRIMARY
            for key, col in CATEGORY_COLORS.items():
                if key.lower() in cat_text.lower():
                    cat_color = col
                    break
            story.append(Spacer(1, 3 * mm))
            story.append(_section_banner(cat_text, icon="◆", color=cat_color, styles=s))
            story.append(Spacer(1, 2 * mm))
            current_cat = cat_text
            q_num = 0
            continue

        # Numbered question
        m = re.match(r"^(\d+)\.\s+(.+)", stripped)
        if m:
            q_num_raw, q_text = m.group(1), m.group(2)
            row = Table(
                [[
                    Paragraph(f"{q_num_raw}.", s["QNum"]),
                    Paragraph(_clean_md(q_text), s["QText"]),
                ]],
                colWidths=[10 * mm, W - LM - RM - 10 * mm],
            )
            row.setStyle(TableStyle([
                ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING",    (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING",   (0, 0), (0, 0),   0),
                ("LEFTPADDING",   (1, 0), (1, 0),   4),
            ]))
            story.append(row)
        elif stripped:
            story.append(Paragraph(_clean_md(stripped), s["Body"]))


# ── Main generator ────────────────────────────────────────────────────────────
def generate_report(
    filename: str,
    resume_score: int,
    match_score: int,
    ai_review: str,
    jd_review: str,
    skills: list | None = None,
    matched: list | None = None,
    missing: list | None = None,
    roles: list | None = None,
    interview_questions: str = "",
) -> None:
    """Build and save the premium branded PDF report."""
    skills   = skills   or []
    matched  = matched  or []
    missing  = missing  or []
    roles    = roles    or []

    s = _build_styles()

    # ── Document ──────────────────────────────────────────────────────────────
    frame       = Frame(LM, BM + FOOTER_H, W - LM - RM, H - TM - BM - FOOTER_H - HEADER_H)
    cover_frame = Frame(LM, BM, W - LM - RM, H - 2 * BM)

    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=0, rightMargin=0,
        topMargin=0, bottomMargin=0,
    )
    doc.addPageTemplates([
        PageTemplate(id="Cover",  frames=[cover_frame], onPage=_on_page),
        PageTemplate(id="Normal", frames=[frame],       onPage=_on_page),
    ])

    story = []
    CW    = W - 2 * LM   # usable content width

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    now_str = datetime.now().strftime("%B %d, %Y")

    # 1. Purple brand bar
    brand_bar = Table(
        [[Paragraph("AI Resume Analyzer Pro", s["CoverTitle"])]],
        colWidths=[CW],
    )
    brand_bar.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_PRIMARY),
        ("TOPPADDING",    (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
    ]))
    story.append(brand_bar)
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Career Intelligence Report", s["CoverSub"]))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph(now_str, s["CoverMeta"]))
    story.append(Spacer(1, 10 * mm))
    story.append(HRFlowable(width="100%", color=C_BORDER, thickness=0.8))
    story.append(Spacer(1, 10 * mm))

    # 2. Score columns: LABEL on top, big number, thin coloured rule below
    half = (CW - 10 * mm) / 2

    def _score_col(label, score, accent):
        """Vertical block: label → large % number → coloured accent rule."""
        hex_str = accent.hexval()[:7]
        rule = Table([[""]], colWidths=[half * 0.5], rowHeights=[3 * mm])
        rule.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), accent),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ]))
        col = Table(
            [
                [Paragraph(label, s["ScoreTagline"])],
                [Paragraph(f'<font color="{hex_str}"><b>{score}%</b></font>', s["ScoreBig"])],
                [rule],
            ],
            colWidths=[half],
        )
        col.setStyle(TableStyle([
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        return col

    scores_tbl = Table(
        [[_score_col("ATS Resume Score", resume_score, C_PRIMARY),
          Spacer(10 * mm, 1),
          _score_col("JD Match Score",   match_score,  C_SUCCESS)]],
        colWidths=[half, 10 * mm, half],
    )
    scores_tbl.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    story.append(scores_tbl)
    story.append(Spacer(1, 12 * mm))

    # ── 5. Thin rule + 4-stat summary (text only, no background)
    story.append(HRFlowable(width="100%", color=C_BORDER, thickness=0.8))
    story.append(Spacer(1, 6 * mm))

    stat_style = ParagraphStyle(
        "stat", fontName="Helvetica", fontSize=9, textColor=C_MUTED, alignment=TA_CENTER,
    )
    stat_bold = ParagraphStyle(
        "statb", fontName="Helvetica-Bold", fontSize=13, textColor=C_DARK2, alignment=TA_CENTER,
    )
    stat_data = [
        ("Skills Detected", len(skills)),
        ("Matched",         len(matched)),
        ("Missing",         len(missing)),
        ("Suggested Roles", len(roles)),
    ]
    stat_cols = []
    for lbl, val in stat_data:
        stat_cols.append(Table(
            [[Paragraph(str(val), stat_bold)], [Paragraph(lbl, stat_style)]],
            colWidths=[CW / 4],
        ))
    stat_row = Table([stat_cols], colWidths=[CW / 4] * 4)
    stat_row.setStyle(TableStyle([
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    story.append(stat_row)
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=C_BORDER, thickness=0.8))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "Powered by Groq LLM  •  AI Resume Analyzer Pro  •  Confidential",
        s["CoverMeta"],
    ))

    # Switch to Normal template for remaining pages
    from reportlab.platypus import NextPageTemplate
    story.append(NextPageTemplate("Normal"))
    story.append(PageBreak())

    # ── SKILLS SECTION ────────────────────────────────────────────────────────
    if skills:
        story.append(KeepTogether([
            _section_banner("Detected Skills", "◈", C_PRIMARY, s),
            Spacer(1, 3 * mm),
        ]))
        _skill_chips(skills, C_CHIP_BG, C_WHITE, story, s)

    if matched or missing:
        story.append(KeepTogether([
            _section_banner("Skill Match Analysis", "◈", C_SECONDARY, s),
            Spacer(1, 3 * mm),
        ]))
        if matched:
            story.append(Paragraph("<b>Matched Skills</b>", s["BodyBold"]))
            story.append(Spacer(1, 2 * mm))
            _skill_chips(matched, C_SUCCESS, C_WHITE, story, s)
        if missing:
            story.append(Paragraph("<b>Missing Skills</b>", s["BodyBold"]))
            story.append(Spacer(1, 2 * mm))
            _skill_chips(missing, C_DANGER, C_WHITE, story, s)

    if roles:
        story.append(KeepTogether([
            _section_banner("Recommended Roles", "◈", C_TEAL, s),
            Spacer(1, 3 * mm),
        ]))
        _skill_chips(roles, C_SECONDARY, C_WHITE, story, s)

    # ── AI RESUME REVIEW ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(_section_banner("AI Resume Review", "▸", C_PRIMARY, s))
    story.append(Spacer(1, 4 * mm))
    _render_body(ai_review, story, s)

    # ── JD COMPARISON ─────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(_section_banner("Resume vs Job Description", "▸", C_SECONDARY, s))
    story.append(Spacer(1, 4 * mm))
    _render_body(jd_review, story, s)

    # ── INTERVIEW QUESTIONS ────────────────────────────────────────────────────
    if interview_questions:
        story.append(PageBreak())
        story.append(_section_banner("Interview Preparation Guide", "▸", C_DARK, s))
        story.append(Spacer(1, 4 * mm))
        _render_questions(interview_questions, story, s)

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story)