import logging
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import llm, GROQ_API_KEY
import json
from typing import List, Dict

load_dotenv()

# Set up logging
os.makedirs(os.path.join("logs"), exist_ok=True)  # 📂 Creates a 'logs' directory if it doesn't exist
logging.basicConfig(  # ⚙️ Configures the logging system with specified settings
    level=logging.INFO,  # 📏 Sets logging level to INFO to capture informational messages and above
    format="%(asctime)s [%(levelname)s] %(message)s",  # 📝 Defines log message format: timestamp, level, and message
    handlers=[  # 📤 Specifies where logs are sent
        logging.FileHandler(os.path.join("logs", "app.log")),  # 📜 Logs to a file named 'logging.log' in the 'logs' directory
        logging.StreamHandler()  # 🖥️ Also logs to the console (standard output)
    ]
)

def structure_data(text: str) -> List[Dict]:
    """
    Use Groq LLM to extract all explicitly mentioned test result information from medical report text.
    Returns a list of dictionaries with all fields found in the report.
    """
    logging.info("Extracting structured data using LLM.")
    try:
        # Define prompt for LLM
        messages = [
            SystemMessage(content="You are a medical data extraction assistant."),
            HumanMessage(content=f"""
                You are a medical data extraction expert.

                Given the following medical report, extract all explicitly mentioned information related to test results and return it as a **valid JSON array** of dictionaries. Each dictionary should represent a test result or relevant metadata (e.g., patient information) as found in the text.

                **Important Instructions:**
                - Include **only** fields that are explicitly mentioned in the report (e.g., test name, value, unit, normal range, patient name, age, date, etc.).
                - Do **not** guess, hallucinate, or add fields not present in the text.
                - Do **not** perform any calculations or inferences (e.g., do not compute status or categorize values).
                - Each dictionary should contain key-value pairs for the fields explicitly stated in the report.
                - Your response must be a **JSON array of dictionaries**.
                - Return **only** the JSON array — no explanations, no markdown, no code formatting, no comments.

                Medical Report:
                {text}
                """)
        ]

        response = llm.invoke(messages)
        logging.info("✅ Response received from Groq.")
        
        # Parse JSON response
        try:
            results = json.loads(response.content.strip())
            if not isinstance(results, list):
                logging.warning("LLM returned non-list response")
                return []
            logging.info(f"Extracted {len(results)} results from LLM response")
            return results
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse LLM response as JSON: {str(e)}")
            return []
    except Exception as e:
        logging.exception(f"LLM structuring failed: {str(e)}")
        return []


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
#     result = structure_data(sample_text)
#     print(result)
