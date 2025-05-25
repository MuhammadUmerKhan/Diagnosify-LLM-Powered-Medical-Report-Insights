import logging
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from typing import Dict, List
from src.config import llm, GROQ_API_KEY
import os, json
from dotenv import load_dotenv
# import nlp, categorize

load_dotenv()

os.makedirs(os.path.join("logs"), exist_ok=True)  # 📂 Creates a 'logs' directory if it doesn't exist
logging.basicConfig(  # ⚙️ Configures the logging system with specified settings
    level=logging.INFO,  # 📏 Sets logging level to INFO to capture informational messages and above
    format="%(asctime)s [%(levelname)s] %(message)s",  # 📝 Defines log message format: timestamp, level, and message
    handlers=[  # 📤 Specifies where logs are sent
        logging.FileHandler(os.path.join("logs", "app.log")),  # 📜 Logs to a file named 'logging.log' in the 'logs' directory
        logging.StreamHandler()  # 🖥️ Also logs to the console (standard output)
    ]
)

def explain_results_batch(results: List[Dict]) -> str:
    """
    Send all categorized results to the LLM and request detailed explanations
    for each one in a single response.
    """
    logging.info("Generating batch explanations for all categorized test results.")

    try:
        input_data = json.dumps(results, indent=2)

        prompt = f"""
        You are a professional medical explanation assistant.

        You will receive a list of medical test results in dictionary format. Each dictionary may include:
        - test_name
        - value
        - unit
        - normal_range
        - status
        - additional metadata

        Your job is to clearly and patiently explain **each test result** to a non-technical patient. For **each test**, give a separate explanation that includes:
        - What the test measures.
        - The patient's value and what it means.
        - The given status (Normal, Borderline, Critical, Unknown) and why it was assigned.
        - If needed, what the patient should do next.

        Use simple language.
        Only use provided data. Do not assume, infer, or invent missing details.

        Return a clearly separated explanation **for each test** — label them clearly with the test name.

        Input:
        {input_data}
        """

        messages = [
            SystemMessage(content="You are a professional medical explanation assistant."),
            HumanMessage(content=prompt)
        ]

        response = llm.invoke(messages)
        explanation = response.content.strip()
        logging.info("✅ Batch explanations received.")
        return explanation

    except Exception as e:
        logging.error(f"❌ Error generating batch explanation: {str(e)}")
        return "Unable to generate explanations due to an error."


# Main script execution
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

#     structure = nlp.structure_data(sample_text)
#     categorized = categorize.categorize_results(structure)

#     print("\n=== Patient-Friendly Explanations ===\n")
#     explanations = explain_results_batch(categorized)
#     print(explanations)
