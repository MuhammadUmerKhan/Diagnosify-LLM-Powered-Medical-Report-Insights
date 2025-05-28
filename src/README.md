# Diagnosify – AI-Powered Medical Insight Engine - `src` Folder Documentation

## Overview

The `src` folder is the core package of the **AI Medical Report Analyzer**, a project developed for a hackathon by Muhammad Umer Khan. This application leverages AI to extract, categorize, and explain medical test results, providing patient-friendly insights through a web interface built with Streamlit and powered by Groq LLM. The `src` folder contains the modular components responsible for the application's backend logic.

## Folder Structure

- `__init__.py`: Marks the `src` directory as a Python package, allowing imports of its modules.
- `chatbot.py`: Implements the interactive chatbot for answering user queries about medical reports.
- `ocr.py`: Handles text extraction from images and PDFs using OCR (Optical Character Recognition).
- `nlp.py`: Structures raw text into meaningful data using natural language processing techniques.
- `categorize.py`: Categorizes medical test results into statuses like Normal, Borderline, or Critical.
- `table_formatter.py`: Formats categorized data into a table structure for display.
- `explain.py`: Generates patient-friendly explanations for medical test results using Groq LLM.
- `summary.py`: Creates concise summaries, risks, and recommendations based on test result explanations.
- `pdf_generator.py`: Generates downloadable PDF summaries of the analyzed medical reports.

## File Details

### `__init__.py`
- **Purpose**: An empty file that designates the `src` directory as a Python package, enabling imports like `from src.chatbot import MedicalChatbot`.
- **Usage**: No direct interaction; it’s automatically used by Python for package initialization.

### `chatbot.py`
- **Purpose**: Implements the `MedicalChatbot` class, which provides an interactive chat interface for users to ask questions about their medical reports.
- **Key Features**:
  - Uses Retrieval-Augmented Generation (RAG) with FAISS for context-aware responses.
  - Streams responses in real-time using Groq LLM.
  - Manages chat history and displays messages in a user-friendly UI.
- **Dependencies**:
  - `langchain_groq`, `langchain_community`, `langchain`, `streamlit`.
  - Internal: `src.ocr` for text extraction.

### `ocr.py`
- **Purpose**: Extracts text from medical report files (PDFs, PNGs, JPEGs) using OCR.
- **Key Features**:
  - Supports multiple file formats.
  - Uses `pytesseract` for image-based text extraction and `PyPDFLoader` for PDFs.
- **Dependencies**:
  - `opencv-python`, `pytesseract`, `langchain_community.document_loaders`.

### `nlp.py`
- **Purpose**: Processes raw text extracted by `ocr.py` and structures it into a usable format (e.g., key-value pairs for test results).
- **Key Features**:
  - Extracts relevant medical data using natural language processing techniques.
- **Dependencies**:
  - Likely depends on NLP libraries (specific dependencies would depend on implementation).

### `categorize.py`
- **Purpose**: Categorizes structured medical data into statuses (e.g., Normal, Borderline, Critical) based on predefined ranges or rules.
- **Key Features**:
  - Assigns color-coded statuses for easy interpretation.
- **Dependencies**:
  - None explicitly mentioned; operates on structured data from `nlp.py`.

### `table_formatter.py`
- **Purpose**: Converts categorized data into a tabular format for display in the Streamlit UI.
- **Key Features**:
  - Prepares data for `pandas` DataFrame rendering.
- **Dependencies**:
  - `pandas`.

### `explain.py`
- **Purpose**: Generates detailed, patient-friendly explanations for medical test results using Groq LLM.
- **Key Features**:
  - Batch processes test results to provide comprehensive explanations.
- **Dependencies**:
  - `langchain_groq`.

### `summary.py`
- **Purpose**: Creates concise bullet-point summaries, including risks and recommendations, based on explanations.
- **Key Features**:
  - Formats summaries for easy reading in the UI.
- **Dependencies**:
  - Likely depends on `explain.py` output.

### `pdf_generator.py`
- **Purpose**: Generates downloadable PDF summaries of the analyzed medical reports.
- **Key Features**:
  - Uses `reportlab` to create formatted PDF documents.
- **Dependencies**:
  - `reportlab`.

## Setup and Usage

### Prerequisites
- **Python**: 3.12 or higher.
- **Dependencies**: Install the required packages using the `requirements.txt` from the project root:
  ```bash
  pip install -r requirements.txt
  ```
  Key dependencies include:
  - `streamlit==1.31.1`
  - `opencv-python==4.9.0`
  - `pytesseract==0.3.10`
  - `pdfplumber==0.10.4`
  - `reportlab==4.0.9`
  - `langchain-groq==0.2.0`
  - `python-dotenv==1.0.0`
  - `pandas==2.2.0`
  - `sentence-transformers==2.7.0`
  - `faiss-cpu==1.8.0`
  - `langchain-community==0.2.0`
  - `langchain-text-splitters==0.2.0`
  - `langchain==0.2.0`

- **API Key**: A Groq API key is required for LLM functionality. Set it in a `.env` file in the project root or as an environment variable:
  ```bash
  export GROQ_API_KEY="your-api-key-here"
  ```

### Running the Application
1. **Navigate to the Project Root**:
   ```bash
   cd /path/to/AI-Medical-Report-Analyzer-Assistant
   ```
2. **Activate Virtual Environment** (if using one):
   ```bash
   source /path/to/env/bin/activate
   ```
3. **Run the App**:
   ```bash
   streamlit run app.py
   ```
4. **Access the App**:
   - Open your browser and go to `http://localhost:8501`.
   - Use the sidebar to upload a medical report (PDF, PNG, or JPEG).
   - Navigate to the "Chatbot" tab to interact with the `MedicalChatbot` or the "Analyze" tab to see detailed analysis.

## Development Notes

- **Modularity**: Each file in `src` is designed to handle a specific task, making the codebase modular and easy to maintain.
- **Error Handling**: Ensure proper error handling in each module, especially in `ocr.py` and `chatbot.py`, to handle malformed inputs or API failures.
- **Extending Functionality**:
  - Add new modules to `src` as needed (e.g., for additional analysis or visualization).
  - Update `__init__.py` if you need to expose new modules for import.
- **Testing**:
  - Test each module independently to ensure it works as expected.
  - Example: Test `ocr.py` with sample PDFs and images to verify text extraction accuracy.

## Known Issues

- **Chatbot Input Positioning**: Ensure the `st.chat_input` in `chatbot.py` is correctly placed at the bottom of the UI (fixed in recent updates).
- **Dependency Conflicts**: If using Pydantic with `langchain`, ensure version `1.10.13` to avoid serialization issues (`pip install pydantic==1.10.13`).
- **File Cleanup**: Temporary files created in `process_file` (in `chatbot.py`) are deleted, but ensure no file handle leaks occur during high load.

## Contributing

This project was developed for a hackathon by Muhammad Umer Khan. Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## Contact

For questions or feedback, reach out to Muhammad Umer Khan at [your-email@example.com].

---