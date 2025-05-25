import logging
import os
import json
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import llm, GROQ_API_KEY
from typing import List, Dict

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

def format_results_for_table(results: List[Dict]) -> List[Dict]:
    """
    Formats medical test results into a consistent table-ready structure using LLM.

    Returns a list of dictionaries with the following columns:
    - test_name
    - value
    - unit
    - normal_range
    - status
    """
    logging.info("🔁 Formatting results for table using LLM")

    try:
        # Serialize results
        input_data = json.dumps(results, indent=2)

        # Prompt
        prompt = f"""
            You are a medical data assistant.

            Given the following list of mixed medical report entries (some may be test results, others may be metadata), extract only **test result entries** and format them into dictionaries with the following columns:

            - test_name
            - value
            - unit
            - normal_range
            - status

            **Instructions:**
            - Ignore non-test metadata (like name, age, date).
            - Map fields (e.g., 'test' → 'test_name', etc.) as needed.
            - Use 'Unknown' for missing fields.
            - Use '' (empty string) for inapplicable fields.
            - Return **only** a JSON array of test dictionaries. No text, no markdown, no code formatting.

            Input:
            {input_data}
        """

        messages = [
            SystemMessage(content="You are a medical data assistant."),
            HumanMessage(content=prompt)
        ]

        response = llm.invoke(messages)
        raw = response.content.strip()

        # Try to parse JSON
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list) and all(isinstance(row, dict) for row in parsed):
                logging.info(f"✅ Successfully formatted {len(parsed)} rows for table.")
                return parsed
            else:
                logging.warning("⚠️ LLM response was not a list of dictionaries.")
                return []
        except json.JSONDecodeError as e:
            logging.error(f"❌ JSON parsing failed for LLM response: {str(e)}")
            return []

    except Exception as e:
        logging.exception("❌ Unexpected error during table formatting")
        return []
