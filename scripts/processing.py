import json
from scripts.utils import configure_llm, create_llm_prompt
from scripts.config import get_logger
from typing import List, Dict

logger = get_logger(__name__)

def process_medical_report(text: str) -> tuple[List[Dict], str, str]:
    """
    Process medical report text through structuring, categorization, explanation, and summary.
    Returns structured results, explanations, and summary bullet points.
    """
    logger.info("Processing medical report")

    # Step 1: Structure data
    results = structure_data(text)
    if not results:
        logger.error("Failed to structure data")
        return [], "Unable to process report due to structuring error.", ""

    # Step 2: Categorize results
    categorized = categorize_results(results)
    if not categorized:
        logger.warning("No categorized results returned, using original results")
        categorized = results

    # Step 3: Format for table
    table_results = format_results_for_table(categorized)

    # Step 4: Generate explanations
    explanations = explain_results_batch(table_results)
    if not explanations or "error" in explanations.lower():
        logger.error("Failed to generate explanations")
        explanations = "Unable to generate explanations due to an error."

    # Step 5: Generate summary
    summary_bullets = generate_summary_bullet_points(explanations)
    if not summary_bullets or "error" in summary_bullets.lower():
        logger.error("Failed to generate summary")
        summary_bullets = "Unable to generate summary due to an error."

    logger.info("Medical report processing completed")
    return table_results, explanations, summary_bullets

def structure_data(text: str) -> List[Dict]:
    """Extract structured data from medical report text using LLM."""
    logger.info("Extracting structured data")
    try:
        # messages = [
        #     SystemMessage(content="You are a medical data extraction assistant."),
        #     HumanMessage(content=f"""
        #         Extract all explicitly mentioned information from the medical report below as a JSON array of dictionaries.
        #         Include only fields explicitly stated (e.g., test_name, value, unit, normal_range, patient_name, age, date).
        #         Do not guess or add fields. Return only the JSON array.

        #         Medical Report:
        #         {text}
        #     """)
        # ]
        messages = create_llm_prompt(system_role="You are a medical data extraction assistant.",
                                     task_instructions="""
                Given the following medical report, extract all explicitly mentioned information related to test results and return it as a **valid JSON array** of dictionaries. Each dictionary should represent a test result or relevant metadata (e.g., patient information) as found in the text.

                **Important Instructions:**
                - Include **only** fields that are explicitly mentioned in the report (e.g., test name, value, unit, normal range, patient name, age, date, etc.).
                - Do **not** guess, hallucinate, or add fields not present in the text.
                - Do **not** perform any calculations or inferences (e.g., do not compute status or categorize values).
                - Each dictionary should contain key-value pairs for the fields explicitly stated in the report.
                - Your response must be a **JSON array of dictionaries**.
                - Return **only** the JSON array — no explanations, no markdown, no code formatting, no comments.
                                     """, input_data=text)
        response = configure_llm().invoke(messages)
        results = json.loads(response.content.strip())
        if not isinstance(results, list):
            logger.warning("LLM returned non-list response")
            return []
        logger.info(f"Extracted {len(results)} results")
        return results
    except Exception as e:
        logger.error(f"Structuring failed: {str(e)}")
        return []

def categorize_results(results: List[Dict]) -> List[Dict]:
    """Categorize medical report data, adding 'status' field where applicable."""
    logger.info("Categorizing results")
    try:
        results_text = json.dumps(results, indent=2)
        # messages = [
        #     SystemMessage(content="You are an expert medical data categorizer."),
        #     HumanMessage(content=f"""
        #         Categorize the medical report data below, assigning 'status' ('Critical', 'Borderline', 'Normal', 'Unknown')
        #         to test result entries based on provided data. Do not add status to non-test entries (e.g., patient_name, age).
        #         Do not guess or perform calculations. Return only the JSON array.

        #         Input:
        #         {results_text}
        #     """)
        # ]
        messages = create_llm_prompt(system_role="You are an expert medical data categorizer.",
                                     task_instructions="""
                Given the following list of dictionaries containing medical report data (e.g., test results, patient metadata, or other fields), analyze each entry and assign a 'status' field with one of the values: 'Critical', 'Borderline', 'Normal', or 'Unknown'. Categorize based solely on the provided data, using your medical expertise to interpret the values and context. The data can contain any fields (e.g., test names, values, ranges, units, patient info, or others), and you should not assume specific fields are present.

                **Important Instructions:**
                - For entries likely representing test results (e.g., containing fields like test_name, value, or similar), assign a status based on the provided data:
                - Use 'Normal' if the data indicates a value within typical medical norms (e.g., based on a range or medical context).
                - Use 'Borderline' if the data suggests a value slightly outside typical norms.
                - Use 'Critical' if the data indicates a value significantly outside typical norms.
                - Use 'Unknown' if insufficient data is provided to determine status (e.g., missing values or context).
                - For non-test entries (e.g., patient_name, age, date), do not add a 'status' field unless the data directly informs a medical categorization (e.g., age indicating risk).
                - Do **not** perform numerical calculations or assume specific fields (e.g., value, normal_range) are present.
                - Do **not** guess or hallucinate information not provided in the input.
                - Return the original list of dictionaries, updated with a 'status' field where applicable, as a JSON array.
                - Return **only** the JSON array — no explanations, no markdown, no code formatting, no comments.
                                     """, input_data=results_text)
        response = configure_llm().invoke(messages)
        categorized = json.loads(response.content.strip())
        if not isinstance(categorized, list):
            logger.warning("Non-list response for categorization")
            return results
        logger.info(f"Categorized {len(categorized)} results")
        return categorized
    except Exception as e:
        logger.error(f"Categorization failed: {str(e)}")
        return results

def format_results_for_table(results: List[Dict]) -> List[Dict]:
    """Format test results for table display."""
    logger.info("Formatting results for table")
    try:
        input_data = json.dumps(results, indent=2)
        # messages = [
        #     SystemMessage(content="You are a medical data assistant."),
        #     HumanMessage(content=f"""
        #         Extract only test result entries from the input below and format them into dictionaries with:
        #         test_name, value, unit, normal_range, status. Use 'Unknown' for missing fields, '' for inapplicable.
        #         Return only a JSON array of test dictionaries.

        #         Input:
        #         {input_data}
        #     """)
        # ]
        messages = create_llm_prompt(system_role="You are a medical data assistant.",
                                     task_instructions="""
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
                                     """, input_data=input_data)
        response = configure_llm().invoke(messages)
        parsed = json.loads(response.content.strip())
        if isinstance(parsed, list) and all(isinstance(row, dict) for row in parsed):
            logger.info(f"Formatted {len(parsed)} rows for table")
            return parsed
        logger.warning("Invalid table format response")
        return []
    except Exception as e:
        logger.error(f"Table formatting failed: {str(e)}")
        return []

def explain_results_batch(results: List[Dict]) -> str:
    """Generate patient-friendly explanations for test results."""
    logger.info("Generating explanations")
    try:
        input_data = json.dumps(results, indent=2)
        # messages = [
        #     SystemMessage(content="You are a professional medical explanation assistant."),
        #     HumanMessage(content=f"""
        #         Explain each test result in the input below for a non-technical patient. For each test, include:
        #         - What it measures
        #         - The patient's value and its meaning
        #         - The status (Normal, Borderline, Critical, Unknown) and why
        #         - Next steps if needed
        #         Use simple language, separate explanations by test name, and return plain text.

        #         Input:
        #         {input_data}
        #     """)
        # ]
        messages = create_llm_prompt(system_role="You are a professional medical explanation assistant.",
                                     task_instructions="""
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
                                     """, input_data=input_data)
        response = configure_llm().invoke(messages)
        explanation = response.content.strip()
        logger.info("Explanations generated")
        return explanation
    except Exception as e:
        logger.error(f"Explanation generation failed: {str(e)}")
        return "Unable to generate explanations due to an error."

def generate_summary_bullet_points(explanations: str) -> str:
    """Generate summary bullet points from explanations."""
    logger.info("Generating summary bullet points")
    try:
        # messages = [
        #     SystemMessage(content="You are a compassionate medical assistant."),
        #     HumanMessage(content=f"""
        #         From the medical explanations below, generate:
        #         - 🔍 **Summary**: 3–5 concise points of key findings
        #         - ⚠️ **Risks/Conditions**: Potential risks with likelihood (High, Possible, Low)
        #         - ✅ **Actions/Recommendations**: 2–5 specific next steps
        #         Return only plain text bullet points grouped into these sections.

        #         Explanations:
        #         {explanations}
        #     """)
        # ]
        messages = create_llm_prompt(system_role="You are a compassionate medical assistant.",
                                     task_instructions="""
        You are a compassionate and professional medical assistant.

        You will receive a set of detailed medical explanations (already written in patient-friendly language).
        Your task is to generate the following — using **bullet points** only:

        - 🔍 **Summary**: 3–5 concise points highlighting what was found in the medical report.
        - ⚠️ **Risks/Conditions**: List potential health risks or conditions with likelihood (High, Possible, Low), based on the explanations.
        - ✅ **Actions/Recommendations**: Provide 2–5 very specific next steps, lifestyle tips, or suggestions (e.g., "Consult a cardiologist", "Reduce sugar intake", "Schedule follow-up in 1 month").

        Do NOT repeat the full explanations.
        Do NOT return any JSON or formatting instructions — just clean, readable bullet points grouped into the 3 sections above.

                                     """, input_data=explanations)
        response = configure_llm().invoke(messages)
        return response.content.strip()
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        return "Unable to generate summary due to an error."