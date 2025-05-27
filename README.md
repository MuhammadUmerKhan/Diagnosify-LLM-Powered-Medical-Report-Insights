# 🩺 AI Medical Report Analyzer 🌟

## 📋 Overview

The **AI Medical Report Analyzer** is a cutting-edge application designed to simplify the interpretation of medical reports for patients. Built as part of a hackathon by **Muhammad Umer Khan**, this project leverages advanced AI technologies to extract, categorize, and explain medical test results, delivering clear, patient-friendly insights through an intuitive web interface. The app supports multiple file formats (PDFs, PNGs, JPEGs) and provides detailed analysis, summaries, and an interactive chatbot for answering health-related queries.

<img src="https://r2.erweima.ai/i/1nyAf1TvSzqEczv-3hXPVA.png" height="800" alt="Project Banner">

### 🎯 Key Objectives
- **Extract**: Automatically extract text from medical reports using OCR. 📄
- **Analyze**: Categorize and explain test results with AI-driven insights. 🧠
- **Summarize**: Provide concise summaries with risks and recommendations. 📝
- **Interact**: Offer an AI-powered chatbot for users to ask questions about their reports. 💬
- **Export**: Generate downloadable PDF summaries for easy sharing. 📥

### ✨ Features
- **Multi-Format Support**: Handles PDFs, PNGs, and JPEGs for versatile report uploads. 🖼️
- **AI-Driven Insights**: Uses Groq LLM to provide detailed, patient-friendly explanations. 🤖
- **Color-Coded Results**: Categorizes test results as Normal ✅, Borderline ⚠️, or Critical 🚨.
- **Interactive Chatbot**: Allows users to ask questions about their medical reports in real-time. 💬
- **PDF Export**: Generates professional PDF summaries for offline use. 📄
- **User-Friendly UI**: Built with Streamlit for an intuitive and visually appealing interface. 🌟

## 🛠️ Tech Stack

- **Frontend**: Streamlit 🌐
- **Backend**: Python 🐍
- **AI/LLM**: Groq LLM (via `langchain-groq`) 🤖
- **OCR**: OpenCV, Pytesseract, PyPDFLoader 📄
- **Data Processing**: Pandas, LangChain 📊
- **PDF Generation**: ReportLab 📥
- **Vector Store**: FAISS for Retrieval-Augmented Generation (RAG) 🔍
- **Environment Management**: `python-dotenv` for API key handling 🔐

## 📂 Project Structure

```
AI-Medical-Report-Analyzer-Assistant/ 🌍
│
│
├── logs/ 📋                   # Directory for log files (auto-generated)
│   └── app.log 📝             # Log file for application events
├── tmp/ ⏳                    # Temporary directory for file processing (auto-generated)
├── src/ 🛠️                    # Core logic package
│   ├── __init__.py 📦         # Marks src as a Python package
│   ├── chatbot.py 💬          # Interactive chatbot for user queries
│   ├── ocr.py 📷              # Text extraction from images/PDFs using OCR
│   ├── nlp.py 🧩              # Structures raw text into usable data
│   ├── categorize.py 🔍       # Categorizes test results (Normal, Borderline, Critical)
│   ├── table_formatter.py 📊  # Formats data into tables for display
│   ├── explain.py 📖          # Generates explanations using Groq LLM
│   ├── summary.py 📑          # Creates summaries with risks and recommendations
│   ├── pdf_generator.py 📄    # Generates downloadable PDF summaries
│   └── README.md 📚           # Documentation for the src package
│
├── app.py 🌐                  # Main application entry point (Streamlit UI)
│
├── requirements.txt 📋        # List of Python dependencies
│
├── .env 🔐                    # Environment variables (e.g., GROQ_API_KEY)
│
└── README.md 📖               # Project-level documentation (this file)
```

### 📜 File Descriptions
- **`app.py`**: The main entry point of the application, orchestrating the Streamlit UI with three tabs: Home 🏠, Analyze 🩺, and Chatbot 💬.
- **`src/`**: Contains modular components for the backend logic. See [src/README.md](src/README.md) for detailed documentation.
- **`requirements.txt`**: Lists all required Python packages for the project.
- **`.env`**: Stores sensitive information like the Groq API key (not tracked in version control).
- **`logs/app.log`**: Logs application events for debugging and monitoring.
- **`tmp/`**: Temporary directory for storing uploaded files during processing.

## 🚀 Getting Started

### Prerequisites
- **Python**: Version 3.12 or higher 🐍
- **Groq API Key**: Obtain a key from [GroqCloud](https://console.groq.com/keys) to use the LLM 🔑
- **System Dependencies** (for OCR):
  - On Ubuntu: `sudo apt-get install tesseract-ocr libtesseract-dev`
  - On macOS: `brew install tesseract`
  - On Windows: Install Tesseract OCR and add it to your PATH

### Installation
1. **Clone the Repository** (if applicable):
   ```bash
   git clone https://github.com/MuhammadUmerKhan/SMIT-Hackathon-AI-Medical-Report-Analyzer
   cd AI-Medical-Report-Analyzer-Assistant
   ```
2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` includes:
   ```
   streamlit==1.31.1
   opencv-python==4.9.0
   pytesseract==0.3.10
   pdfplumber==0.10.4
   reportlab==4.0.9
   langchain-groq==0.2.0
   python-dotenv==1.0.0
   pandas==2.2.0
   sentence-transformers==2.7.0
   faiss-cpu==1.8.0
   langchain-community==0.2.0
   langchain-text-splitters==0.2.0
   langchain==0.2.0
   ```
4. **Set Up the API Key**:
   Create a `.env` file in the project root and add your Groq API key:
   ```bash
   echo "GROQ_API_KEY=your-api-key-here" > .env
   ```
   Alternatively, set it as an environment variable:
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

### Running the Application
1. **Start the Streamlit Server**:
   ```bash
   streamlit run app.py
   ```
2. **Access the App**:
   - Open your browser and navigate to `http://localhost:8501`.
   - You’ll see the app with three tabs: Home 🏠, Analyze 🩺, and Chatbot 💬.

### Usage Guide
1. **Upload a Medical Report**:
   - Use the sidebar to upload a medical report (PDF, PNG, or JPEG). 📤
   - The app supports multiple file uploads, but the Analyze tab processes only the first file.
2. **Explore the Tabs**:
   - **Home 🏠**: Learn about the project, its features, and tech stack.
   - **Analyze 🩺**: View extracted patient info, test results, explanations, and a downloadable PDF summary.
   - **Chatbot 💬**: Interact with an AI chatbot to ask questions about your report (e.g., "What does my HBA1C mean?").
3. **Download Summary**:
   - In the Analyze tab, click "Generate PDF Summary" to download a PDF of your report analysis. 📥

## 💻 Development Notes

### Key Components
- **Streamlit UI**: The `app.py` file orchestrates the UI with three tabs, leveraging Streamlit’s `st.tabs` for navigation.
- **Modular Backend**: The `src` package separates concerns (e.g., OCR, NLP, chatbot) for maintainability. See [src/README.md](src/README.md) for details.
- **Chatbot with RAG**: The chatbot uses FAISS and LangChain for Retrieval-Augmented Generation, ensuring context-aware responses.

### Customization
- **Styling**: The UI is styled with custom CSS in `app.py`, using a dark theme with cyan-blue accents. Modify the CSS in the `st.markdown` block to change the look and feel. 🎨
- **LLM Model**: The chatbot uses `meta-llama/llama-4-scout-17b-16e-instruct`. Update the model in `chatbot.py` (`configure_llm`) to experiment with other Groq models.
- **Chunking**: The `RecursiveCharacterTextSplitter` in `chatbot.py` uses a chunk size of 1000. Adjust this for better retrieval performance if needed.

### Testing
- **Unit Tests**: Add tests for each `src` module (e.g., test `ocr.py` with sample files, test `explain.py` with mock data).
- **End-to-End Testing**: Test the full pipeline by uploading a sample medical report and verifying the output in all tabs.

## 🐞 Known Issues

- **Chatbot Input Positioning**: Ensure the `st.chat_input` in `chatbot.py` is fixed at the bottom (addressed in recent updates).
- **Pydantic Compatibility**: If using Pydantic with `langchain`, ensure version `1.10.13` to avoid serialization errors:
  ```bash
  pip install pydantic==1.10.13
  ```
- **Temporary Files**: The `tmp/` directory stores temporary files during processing. Ensure cleanup is robust to avoid disk space issues.

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request with a detailed description of your changes.

## 🎯 Live Demo:
- [Click here](https://smit-hackathon-ai-medical-report-analyzer.streamlit.app/)

### Contribution Ideas
- Add support for more file formats (e.g., DOCX). 📜
- Enhance the chatbot with more advanced RAG techniques. 🔍
- Improve UI accessibility (e.g., keyboard navigation, screen reader support). ♿
- Add unit tests for better code reliability. ✅

## 📧 Contact

For questions, feedback, or collaboration, reach out to Muhammad Umer Khan at [muhammadumerk546@gmail.com].

## 🙌 Acknowledgments

- **Groq**: For providing the LLM API that powers the AI explanations and chatbot. 🌟
- **Streamlit**: For the amazing framework that made the UI development seamless. 🌐
- **Hackathon Organizers**: For the opportunity to build this project! 🏆

---
