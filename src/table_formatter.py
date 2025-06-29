import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils import configure_llm
from typing import List, Dict
from src.logger import get_logger

logger = get_logger(__name__)

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
    logger.info("🔁 Formatting results for table using LLM")

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

        response = configure_llm().invoke(messages)
        raw = response.content.strip()

        # Try to parse JSON
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list) and all(isinstance(row, dict) for row in parsed):
                logger.info(f"✅ Successfully formatted {len(parsed)} rows for table.")
                return parsed
            else:
                logger.warning("⚠️ LLM response was not a list of dictionaries.")
                return []
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed for LLM response: {str(e)}")
            return []

    except Exception as e:
        logger.exception("❌ Unexpected error during table formatting")
        return []
