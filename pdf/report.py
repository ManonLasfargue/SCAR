# pdf/report.py
# ======================================================
# SCAR – PDF REPORT GENERATION
# This module generates the final PDF report using ReportLab.
# It assembles textual analysis, charts, and tables into a
# structured and printable academic-style document.
# ======================================================


# ===================== IMPORTS =====================
# Core ReportLab components for document construction
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

# Styling and layout utilities
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor, black
from reportlab.lib.units import cm

# Chart components for vector graphics
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing

# Standard utilities
from io import BytesIO
import os


# =========================================================
# STYLES
# =========================================================
# Define a consistent set of paragraph styles used throughout the PDF.
# These styles ensure visual coherence and academic readability.

styles = getSampleStyleSheet()

# Main section titles (numbered sections)
SECTION = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    textColor=HexColor("#1b5e20"),
    spaceBefore=18,
    spaceAfter=10
)

# Main body text
BODY = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    spaceAfter=8
)

# Figure captions
CAPTION = ParagraphStyle(
    "Caption",
    parent=styles["Normal"],
    fontSize=9,
    textColor=HexColor("#555555"),
    alignment=TA_CENTER,
    spaceAfter=14
)


# =========================================================
# COVER PAGE
# =========================================================
# Draws the cover image on the first page of the document.
# The cover is purely visual and contains no text flowables.

def cover_page(canvas, doc):
    canvas.saveState()

    # Path to the cover image
    homepage = os.path.join("static", "homepage.png")

    # Draw the image only if it exists
    if os.path.exists(homepage):
        canvas.drawImage(
            homepage,
            0,
            0,
            width=A4[0],
            height=A4[1],
            preserveAspectRatio=True,
            mask="auto"
        )

    canvas.restoreState()


# =========================================================
# FOOTER
# =========================================================
# Footer displayed on all pages except the cover.
# Shows project name and page number.

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        A4[0] - 2 * cm,
        1.2 * cm,
        f"SCAR – Carbon Footprint Assessment · Page {doc.page}"
    )
    canvas.restoreState()


# =========================================================
# CHARTS
# =========================================================
# Functions creating vector-based charts embedded in the PDF.
# These charts are based on baseline emission categories only.


def bar_chart(data):
    """
    Create a vertical bar chart showing absolute emissions by category.
    `data` is a dictionary: {category: emissions}.
    """
    d = Drawing(400, 200)
    chart = VerticalBarChart()

    # Position and size of the chart within the drawing
    chart.x = 40
    chart.y = 40
    chart.width = 320
    chart.height = 120

    # Single data series
    chart.data = [list(data.values())]

    # Category labels on the x-axis
    chart.categoryAxis.categoryNames = list(data.keys())

    # Force baseline to start at zero
    chart.valueAxis.valueMin = 0

    # Bar color (SCAR green)
    chart.bars[0].fillColor = HexColor("#2e7d32")

    d.add(chart)
    return d


def pie_chart(data):
    """
    Create a pie chart showing relative emission shares by category.
    """
    d = Drawing(300, 200)
    pie = Pie()

    # Center position
    pie.x = 150
    pie.y = 100

    # Data and labels
    pie.data = list(data.values())
    pie.labels = list(data.keys())

    # Thin outline for readability
    pie.slices.strokeWidth = 0.5

    d.add(pie)
    return d


# =========================================================
# MAIN PDF GENERATION FUNCTION
# =========================================================
# This function assembles the full SCAR report and returns
# a PDF buffer ready to be sent to the user.

def generate_scar_pdf(
    totals,
    reductions,
    baseline_profile,
    dominant_post,
    dominant_share,
    utility,
    emissions,
):
    # In-memory buffer (no temporary file written on disk)
    buffer = BytesIO()

    # PDF document layout configuration
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # List of flowable elements composing the document
    story = []

    # =====================================================
    # PAGE BREAK AFTER COVER
    # =====================================================
    # The first page is the cover; content starts on page 2.
    story.append(PageBreak())

    # =====================================================
    # 1. PURPOSE AND SCOPE
    # =====================================================
    story.append(Paragraph("1. Purpose and scope of the assessment", SECTION))
    story.append(Paragraph(
        "This report presents a carbon footprint assessment of a research project using "
        "the SCAR (Scientific Carbon Assessment for Research) framework.",
        BODY
    ))

    # =====================================================
    # 2. BASELINE FOOTPRINT
    # =====================================================
    story.append(Paragraph("2. Baseline carbon footprint", SECTION))
    story.append(Paragraph(
        f"The total estimated carbon footprint of the project amounts to "
        f"<b>{totals['baseline']} kgCO₂e</b>.",
        BODY
    ))
    story.append(Paragraph(
        f"The dominant emission source is <b>{dominant_post}</b>, "
        f"representing approximately <b>{dominant_share}%</b> of total emissions.",
        BODY
    ))

    # Baseline charts
    story.append(bar_chart(emissions))
    story.append(Paragraph(
        "Figure 1 – Absolute greenhouse gas emissions by category (kgCO₂e).",
        CAPTION
    ))

    story.append(pie_chart(emissions))
    story.append(Paragraph(
        "Figure 2 – Relative contribution of each emission category to the total footprint.",
        CAPTION
    ))

    # =====================================================
    # 3. SCENARIOS
    # =====================================================
    story.append(Paragraph("3. Exploratory scenarios and margins of action", SECTION))
    story.append(Paragraph(
        "Scenarios in SCAR are counterfactual analytical tools. Each scenario modifies "
        "a single category of emissions while all other activities remain unchanged.",
        BODY
    ))

    # =====================================================
    # SCENARIO TABLE (INTERPRETATIVE, ALIGNED WITH HTML)
    # =====================================================
    # Paragraphs are used inside cells to ensure proper text wrapping.

    table_data = [
        [
            Paragraph("<b>Scenario</b>", BODY),
            Paragraph("<b>Targeted emission category</b>", BODY),
            Paragraph("<b>Assumption applied</b>", BODY),
            Paragraph("<b>Resulting project emissions (kgCO₂e)</b>", BODY),
            Paragraph("<b>Relative change vs baseline</b>", BODY),
        ],
        [
            "Baseline",
            "—",
            Paragraph("Observed research practices", BODY),
            totals["baseline"],
            "—",
        ],
        [
            "Modal substitution",
            "Mobility",
            Paragraph("Shift to lower-carbon transport modes", BODY),
            totals["modal"],
            f"−{reductions['modal']}%",
        ],
        [
            "Digital sobriety",
            "Digital infrastructure",
            Paragraph("Reduced computing and storage intensity", BODY),
            totals["digital"],
            f"{reductions['digital']}%",
        ],
        [
            "Utility-aware scenario",
            Paragraph("Mobility (weighted by usefulness)", BODY),
            Paragraph("Emissions adjusted proportionally to mission utility", BODY),
            totals["utility"],
            f"−{reductions['utility']}%",
        ],
    ]

    table = Table(
        table_data,
        colWidths=[3.5*cm, 3.5*cm, 7*cm, 3.5*cm, 3.5*cm],
        repeatRows=1,
        hAlign="CENTER"
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#f1f5f2")),
        ("GRID", (0, 0), (-1, -1), 0.5, black),
        ("ALIGN", (3, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    # Prevent the table from being split awkwardly across pages
    story.append(KeepTogether(table))
    story.append(Spacer(1, 12))

    # Explanatory note for correct interpretation
    story.append(Paragraph(
        "Resulting emissions represent the aggregate footprint of the project under each scenario, "
        "assuming that only the targeted emission category is modified while all other activities "
        "remain unchanged. A zero relative change therefore indicates that the targeted category "
        "does not structurally drive the project’s baseline footprint.",
        BODY
    ))

    # =====================================================
    # 4. LIMITS AND INTENDED USE
    # =====================================================
    story.append(Paragraph("4. Limits and intended use", SECTION))
    story.append(Paragraph(
        "Results produced by SCAR should be interpreted as orders of magnitude rather than "
        "precise measurements. SCAR is intended as a reflexive tool, not a compliance instrument.",
        BODY
    ))

    # Build the PDF document
    doc.build(
        story,
        onFirstPage=cover_page,
        onLaterPages=footer
    )

    # Reset buffer cursor before returning
    buffer.seek(0)
    return buffer
