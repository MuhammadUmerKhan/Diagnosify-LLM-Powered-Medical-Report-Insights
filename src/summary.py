from langchain_core.messages import SystemMessage, HumanMessage
from src.utils import configure_llm
from src.logger import get_logger
# import nlp, explain, categorize, preprocess, table_formatter

logger = get_logger(__name__)


def generate_summary_bullet_points(explanations: str) -> str:
    """
    Given a full explanation block (from explain.py), generate:
    - Summary of key findings
    - Possible risks/conditions with likelihood
    - Specific recommendations and next steps

    All returned in plain text bullet points.
    """
    logger.info("Generating summary bullet points from explanations")

    try:
        prompt = f"""
        You are a compassionate and professional medical assistant.

        You will receive a set of detailed medical explanations (already written in patient-friendly language).
        Your task is to generate the following — using **bullet points** only:

        - 🔍 **Summary**: 3–5 concise points highlighting what was found in the medical report.
        - ⚠️ **Risks/Conditions**: List potential health risks or conditions with likelihood (High, Possible, Low), based on the explanations.
        - ✅ **Actions/Recommendations**: Provide 2–5 very specific next steps, lifestyle tips, or suggestions (e.g., "Consult a cardiologist", "Reduce sugar intake", "Schedule follow-up in 1 month").

        Do NOT repeat the full explanations.
        Do NOT return any JSON or formatting instructions — just clean, readable bullet points grouped into the 3 sections above.

        Medical Explanations:
        {explanations}
        """

        messages = [
            SystemMessage(content="You are a compassionate and professional medical assistant."),
            HumanMessage(content=prompt)
        ]

        response = configure_llm().invoke(messages)
        return response.content.strip()

    except Exception as e:
        logger.error(f"❌ Error generating bullet summary: {str(e)}")
        return "Unable to generate summary due to an error."

# if __name__ == "__main__":
#     sample_text = """
#         Patient Name: John Doe
#         Age: 45
#         Date: 2025-05-20

#         Lab Results:
#         - Glucose: 140 mg/dL (70-110)
#         - Cholesterol: 250 mg/dL (125-200)
#         - Hemoglobin: 13.5 g/dL (13.0-17.0)
#         - WBC Count: 12000 /µL (4500-11000)
#         - Platelets: 180000 /µL (150000-450000)
#     """
    
#     pdf_path = os.path.join("..", "assets", "sample_report.pdf")
#     text = preprocess.extract_text_from_pdf(pdf_path=pdf_path)
#     print(text)
    
#     structure = nlp.structure_data(text)
#     print(structure)
    
#     categorized = categorize.categorize_results(structure)
#     print(categorize)

#     print("\n=== Patient-Friendly Explanations ===\n")
#     explanations = explain.explain_results_batch(categorized)
#     print(explanations)
    
#     table_format = table_formatter.format_results_for_table(categorized)
#     print(table_format)
    
#     summary_bullets = generate_summary_bullet_points(explanations)
#     print(summary_bullets)