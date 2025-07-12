import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from typing import List, Dict
from scripts.utils import get_default_table_style
from scripts.config import get_logger

logger = get_logger(__name__)

@st.cache_data(show_spinner=False)
def generate_pdf_summary(results: List[Dict], explanations: str, summary_bullets: str, output_path: str = None) -> bytes:
    """Generate a PDF summary of medical test results."""
    if not isinstance(results, list) or not results:
        logger.error("Invalid input: results must be a non-empty list of dictionaries")
        raise ValueError("Invalid results input")
    if not isinstance(explanations, str) or not isinstance(summary_bullets, str):
        logger.error("Invalid input: explanations and summary_bullets must be strings")
        raise ValueError("Invalid explanations or summary_bullets input")
    logger.info("Generating improved PDF summary")
    buffer = BytesIO()
    try:
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='List', leftIndent=20, fontSize=10, spaceAfter=6))
        story = []

        # Title
        story.append(Paragraph("🩺 Medical Report Summary", styles["Title"]))
        story.append(Spacer(1, 12))

        # Process metadata and test results in one loop
        metadata = []
        test_results = []
        for item in results:
            if "test_name" in item:
                test_results.append(item)
            else:
                metadata.append(item)

        # Metadata
        if metadata:
            story.append(Paragraph("👤 Patient Information", styles["Heading2"]))
            for item in metadata:
                for key, value in item.items():
                    story.append(Paragraph(f"<b>{key.capitalize()}</b>: {value}", styles["Normal"]))
            story.append(Spacer(1, 12))

        # Test Results
        if test_results:
            story.append(Paragraph("🧪 Test Results", styles["Heading2"]))
            data = [["Test Name", "Value", "Unit", "Normal Range", "Status"]]
            for res in test_results:
                data.append([
                    res.get("test_name", "Unknown"),
                    res.get("value", "Unknown"),
                    res.get("unit", "Unknown"),
                    res.get("normal_range", ""),
                    res.get("status", "Unknown")
                ])
            table = Table(data, hAlign='LEFT', colWidths=[130, 70, 70, 130, 80])
            table.setStyle(get_default_table_style())
            story.append(table)
            story.append(Spacer(1, 12))

        # Explanations
        if explanations:
            story.append(Paragraph("🧾 Explanation", styles["Heading2"]))
            explanation_clean = explanations.replace("\n", " ").strip()
            story.append(Paragraph(explanation_clean, styles["Normal"]))
            story.append(Spacer(1, 12))

        # Summary and Recommendations
        if summary_bullets:
            story.append(Paragraph("📌 Summary and Recommendations", styles["Heading2"]))
            try:
                import re
                sections = {
                    "Summary": re.search(r"\*\*Summary:\*\*(.*?)(?=\*\*|$)", summary_bullets, re.DOTALL),
                    "Risks/Conditions": re.search(r"\*\*Risks/Conditions:\*\*(.*?)(?=\*\*|$)", summary_bullets, re.DOTALL),
                    "Actions/Recommendations": re.search(r"\*\*Actions/Recommendations:\*\*(.*)", summary_bullets, re.DOTALL)
                }
                for section, match in sections.items():
                    if match:
                        story.append(Paragraph(f"📋 <b>{section}:</b>", styles["Normal"]))
                        lines = match.group(1).strip().split("*")
                        items = [ListItem(Paragraph(line.strip(), styles["List"])) for line in lines if line.strip()]
                        story.append(ListFlowable(items, bulletType='bullet'))
                        story.append(Spacer(1, 6))
            except Exception as e:
                logger.warning(f"Failed to parse summary bullet points: {str(e)}. Falling back to plain text.")
                story.append(Paragraph(summary_bullets.replace("\n", " "), styles["Normal"]))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        logger.info("Improved PDF summary generated successfully")
        return pdf_bytes

    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise