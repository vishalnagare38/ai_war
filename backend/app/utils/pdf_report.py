from io import BytesIO
from typing import Any, Dict, List, Tuple

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from xml.sax.saxutils import escape


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, tuple):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def _add_heading(elements, text, styles):
    elements.append(Paragraph(escape(text), styles["Heading2"]))
    elements.append(Spacer(1, 8))


def _add_bullets(elements, items, body_style):
    for item in items:
        elements.append(Paragraph(f"&bull; {escape(item)}", body_style))
        elements.append(Spacer(1, 4))


def _add_paragraph(elements, text, body_style):
    if not text:
        return
    elements.append(Paragraph(escape(str(text)), body_style))
    elements.append(Spacer(1, 8))


def _risk_badge_text(value: str) -> str:
    level = str(value).lower()
    if level == "high":
        return "HIGH"
    if level == "medium":
        return "MEDIUM"
    if level == "low":
        return "LOW"
    return str(value).upper()


def _timing_rows(agent_timings: Dict[str, float]) -> List[List[str]]:
    preferred_order = [
        "Product Agent",
        "Engineering Agent",
        "Finance Agent",
        "Risk Agent",
        "ML Scorer",
        "Consensus Engine",
        "Coordinator Agent",
    ]
    rows: List[List[str]] = []
    used = set()

    for agent in preferred_order:
        if agent in agent_timings:
            rows.append([agent, f"{float(agent_timings[agent]):.2f} s"])
            used.add(agent)

    for agent, duration in agent_timings.items():
        if agent not in used:
            rows.append([agent, f"{float(duration):.2f} s"])

    return rows


def build_pdf_bytes(report: Dict[str, Any]) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CenterTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=20,
            leading=24,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallCenter",
            parent=styles["BodyText"],
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontSize=9,
            leading=11,
            spaceAfter=10,
        )
    )
    body_style = styles["BodyText"]
    body_style.leading = 14

    elements = []

    meeting_title = report.get("meeting_title") or "Meeting War Room Report"
    meeting_id = report.get("meeting_id")
    created_at = report.get("created_at")
    version = report.get("version", "1.0")

    elements.append(Paragraph("Meeting War Room", styles["CenterTitle"]))
    elements.append(Paragraph(escape(str(meeting_title)), styles["SmallCenter"]))
    if meeting_id:
        elements.append(Paragraph(f"Meeting ID: {escape(str(meeting_id))}", styles["SmallCenter"]))
    if created_at:
        elements.append(Paragraph(f"Generated: {escape(str(created_at))}", styles["SmallCenter"]))
    elements.append(Paragraph(f"Version: {escape(str(version))}", styles["SmallCenter"]))
    elements.append(Spacer(1, 8))

    metrics = [
        ["Overall Risk", _risk_badge_text(str(report.get("overall_risk_level", "low")))],
        ["ML Risk", f"{float(report.get('ml_risk_probability', 0.0)) * 100:.1f}%"],
        ["Risk Label", _risk_badge_text(str(report.get("ml_risk_label", "low")))],
        ["Consensus", f"{float(report.get('consensus_score', 0.0)) * 100:.0f}%"],
        ["Agreement", str(report.get("agent_agreement", "low")).upper()],
        ["Meeting Health", f"{int(report.get('meeting_health_score', 0))}/100"],
        ["Health Label", str(report.get("meeting_health_label", "unknown")).upper()],
        ["Processing Time", f"{float(report.get('processing_time_seconds', 0.0)):.2f} s"],
    ]

    table = Table(metrics, colWidths=[2.2 * inch, 3.8 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 14))

    _add_heading(elements, "Executive Summary", styles)
    _add_paragraph(elements, report.get("executive_summary", ""), body_style)

    _add_heading(elements, "Final Decision", styles)
    _add_paragraph(elements, report.get("final_decision", ""), body_style)

    _add_heading(elements, "Consensus Explanation", styles)
    _add_paragraph(elements, report.get("consensus_reason", ""), body_style)

    _add_heading(elements, "Consensus Factors", styles)
    _add_bullets(elements, _as_list(report.get("consensus_factors", [])), body_style)

    _add_heading(elements, "Priority Actions", styles)
    _add_bullets(elements, _as_list(report.get("priority_actions", [])), body_style)

    _add_heading(elements, "Product Risks", styles)
    _add_bullets(elements, _as_list(report.get("risks", [])), body_style)

    _add_heading(elements, "Product Recommendations", styles)
    _add_bullets(elements, _as_list(report.get("recommendations", [])), body_style)

    _add_heading(elements, "Engineering Insights", styles)
    _add_bullets(elements, _as_list(report.get("engineering_insights", [])), body_style)

    _add_heading(elements, "Engineering Risks", styles)
    _add_bullets(elements, _as_list(report.get("engineering_risks", [])), body_style)

    _add_heading(elements, "Engineering Recommendations", styles)
    _add_bullets(elements, _as_list(report.get("engineering_recommendations", [])), body_style)

    _add_heading(elements, "Finance Insights", styles)
    _add_bullets(elements, _as_list(report.get("finance_insights", [])), body_style)

    _add_heading(elements, "Finance Risks", styles)
    _add_bullets(elements, _as_list(report.get("finance_risks", [])), body_style)

    _add_heading(elements, "Finance Recommendations", styles)
    _add_bullets(elements, _as_list(report.get("finance_recommendations", [])), body_style)

    _add_heading(elements, "Risk Insights", styles)
    _add_bullets(elements, _as_list(report.get("risk_insights", [])), body_style)

    _add_heading(elements, "Risk Recommendations", styles)
    _add_bullets(elements, _as_list(report.get("risk_recommendations", [])), body_style)

    _add_heading(elements, "Agent Execution Timeline", styles)
    timings = report.get("agent_timings", {}) or {}
    timing_rows = _timing_rows(timings)

    if timing_rows:
        timing_table = Table([["Agent", "Runtime"]] + timing_rows, colWidths=[3.2 * inch, 2.8 * inch])
        timing_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.black),
                    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(timing_table)
    else:
        _add_paragraph(elements, "No timing data available.", body_style)

    _add_heading(elements, "Coordinator Notes", styles)
    _add_bullets(elements, _as_list(report.get("coordinator_notes", [])), body_style)

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes