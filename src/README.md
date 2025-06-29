# 📂 src/ Folder README 🌟

## 📖 Overview
The `src/` folder contains the core Python modules for the **AI Medical Report Analyzer** 🩺, a Streamlit app that processes medical reports (PDF, PNG, JPEG) to extract, categorize, and explain test results using AI. These modules handle tasks like text extraction, data processing, AI-driven analysis, and PDF generation, making the app user-friendly and powerful 🚀.

## 📑 Files in src/
Here’s a quick look at each file and what it does:

- **📄 config.py**: Sets up the app’s configuration, loading the Groq API key and creating a temporary folder (`tmp/`) for file processing. It ensures everything runs smoothly ⚙️.
- **📜 logger.py**: Configures logging to track app activity (e.g., errors, successes) in a `chatbot.log` file for debugging 🐞.
- **🖼️ ocr.py**: Extracts text from PDFs using `PyPDF2` (image support for PNG/JPEG is commented out). It’s the first step in processing reports 📝.
- **🖌️ preprocess.py**: Extracts text from PDFs with `PyPDF2` (image preprocessing code is commented out). It prepares files for analysis 🔍.
- **🧠 nlp.py**: Uses the Groq LLM to structure raw text into a JSON array of dictionaries, capturing test results and metadata clearly 🗂️.
- **✅ categorize.py**: Adds a `status` field (e.g., Normal, Borderline, Critical) to test results using the Groq LLM, helping identify health concerns 🚨.
- **📊 table_formatter.py**: Formats test results into a table-ready structure (test_name, value, unit, normal_range, status) for display in Streamlit 📈.
- **📘 explain.py**: Generates patient-friendly explanations for each test result using the Groq LLM, making complex data easy to understand 😊.
- **📋 summary.py**: Creates a concise summary with key findings, risks, and recommendations as bullet points, based on explanations ✍️.
- **💻 streaming.py**: Streams LLM responses in real-time to the Streamlit UI, keeping the chatbot interactive and responsive ⚡.
- **🛠️ utils.py**: Provides helper functions like LLM/embedding configuration, chat history management, and message display for the app’s core features 🧰.

## 🚀 Usage
The `src/` modules are used by the main app files (`🏠_Home.py`, `🧐_Analyze.py`, `🤖_Assistant.py`):
- **🏠 Home**: Processes uploaded reports using `ocr`, `preprocess`, `nlp`, `categorize`, `explain`, `summary`, and `pdf_generator`.
- **🧐 Analyze**: Displays processed results using `table_formatter` and `pdf_generator`.
- **🤖 Assistant**: Uses `ocr`, `preprocess`, `utils`, and the Groq LLM for a chatbot that answers questions about PDFs.

To use these modules:
1. Ensure dependencies are installed (see below).
2. Place the `src/` folder in the project root alongside main app files.
3. Set up a `.env` file with `GROQ_API_KEY=your_grok_api_key`.
4. Run the app: `streamlit run 🏠_Home.py`.

## 📦 Requirements
Install these Python packages (listed in `requirements.txt`):
- `streamlit`: For the web interface 🌐.
- `langchain`, `langchain-community`, `langchain-groq`, `langchain-openai`: For AI and LLM integration 🤖.
- `sentence-transformers`, `faiss-cpu`: For text embeddings and vector search 🔎.
- `pypdf2`, `reportlab`: For PDF processing 📄.
- `python-dotenv`: For environment variables ⚙️.
- `opencv-python`, `pytesseract` (optional, for image support if uncommented) 🖼️.

Run `pip install -r requirements.txt` to set up the environment.

## 💡 Notes
- The `ocr.py` and `preprocess.py` files have commented-out image processing code (for PNG/JPEG). Uncomment and ensure `opencv-python` and `pytesseract` are installed if you want to process images.
- All modules use the `logger` for debugging, storing logs in `logs/chatbot.log`.
- The Groq LLM powers `nlp`, `categorize`, `explain`, and `summary` for accurate, patient-friendly results 😊.

## 👨‍💻 Developer
Built by **Muhammad Umer Khan** for a hackathon 🎉. Connect on [LinkedIn](https://www.linkedin.com/in/muhammad-umer-khan-61729b260/) for questions or feedback! 🙌