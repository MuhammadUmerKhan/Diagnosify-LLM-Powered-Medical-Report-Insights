from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from typing import List, Dict
import logging, os
from io import BytesIO

os.makedirs(os.path.join("logs"), exist_ok=True)  # 📂 Creates a 'logs' directory if it doesn't exist
logging.basicConfig(  # ⚙️ Configures the logging system with specified settings
    level=logging.INFO,  # 📏 Sets logging level to INFO to capture informational messages and above
    format="%(asctime)s [%(levelname)s] %(message)s",  # 📝 Defines log message format: timestamp, level, and message
    handlers=[  # 📤 Specifies where logs are sent
        logging.FileHandler(os.path.join("logs", "app.log")),  # 📜 Logs to a file named 'logging.log' in the 'logs' directory
        logging.StreamHandler()  # 🖥️ Also logs to the console (standard output)
    ]
)

def generate_pdf_summary(
    results: List[Dict],
    explanations: str,
    summary_bullets: str,
    output_path: str = None
) -> bytes:
    """Generate a PDF summary of the results, explanations, and summary bullet points and return as bytes."""
    logging.info("Generating PDF summary in memory")
    buffer = BytesIO()
    try:
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph("Medical Report Summary", styles["Title"]))
        story.append(Spacer(1, 12))
        
        # Metadata
        metadata = [r for r in results if "test_name" not in r]
        if metadata:
            story.append(Paragraph("<b>Patient Information</b>", styles["Heading2"]))
            for item in metadata:
                # Format metadata into a more readable structure with line breaks
                fields = "<br/>".join(f"<b>{key}:</b> {value}" for key, value in item.items())
                story.append(Paragraph(fields, styles["Normal"]))
            story.append(Spacer(1, 12))
        
        # Test Results
        test_results = [r for r in results if "test_name" in r]
        if test_results:
            story.append(Paragraph("<b>Test Results</b>", styles["Heading2"]))
            for result in test_results:
                # Format test results with proper structure
                test_name = result.get('test_name', 'Unknown')
                fields = "<br/>".join(f"<b>{key}:</b> {value}" if key != 'test_name' else "" for key, value in result.items())
                story.append(Paragraph(f"<b>Test:</b> {test_name}<br/>{fields}", styles["Normal"]))
                story.append(Spacer(1, 6))  # Small space between test results
            story.append(Spacer(1, 12))
        
        # Explanations
        if explanations:
            story.append(Paragraph("<b>Explanations</b>", styles["Heading2"]))
            # Clean up explanations text and format it
            cleaned_explanations = explanations.replace("\n", " ").replace("  ", " ")  # Normalize spaces
            cleaned_explanations = cleaned_explanations.replace("**", "<b>").replace("**", "</b>")  # Convert markdown bold to HTML
            cleaned_explanations = cleaned_explanations.replace(" - ", "<br/>• ")  # Convert bullet points
            # Split into paragraphs where there are double spaces or logical breaks
            paragraphs = cleaned_explanations.split("Your value is")
            formatted_explanations = "<br/><br/>".join(paragraphs)
            story.append(Paragraph(f"<p>{formatted_explanations}</p>", styles["Normal"]))
            story.append(Spacer(1, 12))
        
        # Summary, Risks, and Actions
        if summary_bullets:
            story.append(Paragraph("<b>Summary and Recommendations</b>", styles["Heading2"]))
            # Clean up summary bullets and format them
            cleaned_summary = summary_bullets.replace("\n", " ").replace("  ", " ")  # Normalize spaces
            cleaned_summary = cleaned_summary.replace("**Summary:**", "<b>Summary:</b>")
            cleaned_summary = cleaned_summary.replace("**Risks/Conditions:**", "<b>Risks/Conditions:</b>")
            cleaned_summary = cleaned_summary.replace("**Actions/Recommendations:**", "<b>Actions/Recommendations:</b>")
            cleaned_summary = cleaned_summary.replace("* ", "<br/>• ")  # Convert bullet points
            story.append(Paragraph(f"<p>{cleaned_summary}</p>", styles["Normal"]))
        
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        logging.info("PDF summary generated successfully")
        return pdf_bytes
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        raise