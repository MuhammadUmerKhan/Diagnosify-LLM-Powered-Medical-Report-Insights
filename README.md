# **🩺 Diagnosify: AI-Powered Medical Report Insights 🌟**

## 📖 Overview
**Diagnosify** is a user-friendly Streamlit app that makes medical reports easy to understand for everyone! 🩺 Built for a hackathon, it uses advanced AI to extract, analyze, and explain test results from reports (PDF, PNG, JPEG) 📄. With a vibrant dark theme 🎨, it offers clear insights, summaries, and a smart chatbot to answer your health questions in a supportive way 😊. Plus, it now evaluates chatbot responses for accuracy with RAGAS metrics 📈! Whether you’re checking test results or diving into chat details, Diagnosify is here to help! 🚀

![](https://img.freepik.com/premium-vector/medical-check-list-health-analysis-research-report-illustration-flat-cartoon-design_101884-86.jpg)

### 🎯 Goals
- **Extract**: Pull text from reports using OCR 📝.
- **Analyze**: Categorize and explain results with AI 🧠.
- **Summarize**: Provide simple summaries with health tips 📋.
- **Chat**: Answer questions about your report with a friendly AI chatbot 🤗.
- **Share**: Download a PDF summary to share with your doctor 📥.
- **Evaluate**: Assess chatbot accuracy with RAGAS for reliable insights 📈.

### ✨ Features
- **Multi-Format Support**: Upload PDFs, PNGs, or JPEGs 📄🖼️.
- **AI Insights**: Groq LLM explains results in patient-friendly language 🌟.
- **Color-Coded Results**: Shows Normal ✅, Borderline ⚠️, or Critical 🚨 statuses.
- **RAG Chatbot**: A domain-specific chatbot answers questions based only on your uploaded PDFs, using Retrieval-Augmented Generation (RAG) for accurate, context-aware replies 💬.
- **PDF Export**: Save a professional PDF summary of your results 📄.
- **RAGAS Evaluation**: Evaluates chatbot responses for accuracy with faithfulness scores 📊, ensuring trustworthy answers displayed on a dedicated page ⚖️.
- **Cool UI**: Dark theme with neon green text, gold headings, and magenta buttons 🎨.

## 🛠️ Tech Stack
- **Frontend**: Streamlit for an interactive web interface 🌐.
- **Backend**: Python for all processing 🐍.
- **AI/LLM**: Groq LLM (`meta-llama/llama-4-scout-17b-16e-instruct`) via `langchain-groq` 🤖.
- **OCR**: `PyPDF2` for PDFs, `opencv-python` & `pytesseract` (optional for images) 📝.
- **Data**: `pandas` for tables, `langchain` for AI processing 📊.
- **RAG**: `FAISS` and `sentence-transformers` for chatbot’s document search 🔍.
- **PDFs**: `reportlab` for generating summaries 📄.
- **RAGAS**: `ragas` for evaluating chatbot accuracy 📈.
- **Database**: `pymongo` for storing chat history in MongoDB Atlas 🗃️.
- **Config**: `python-dotenv` for secure API key management 🔐.

## 📂 Project Structure
```
MedicalReportAnalyzer/
├── logs/ 📋           # Stores log files (e.g., chatbot.log) for debugging 🐞
│   └── app.log    # Logs app activity and errors
├── tmp/ ⏳            # Temporary storage for uploaded files during processing
├── scripts/ 🛠️           # Core logic and utility modules
│   ├── config.py ⚙️  # Loads API keys, sets temp folder, and MongoDB URI
│   ├── logger.py 🐞  # Configures logging to logs/chatbot.log
│   ├── ocr.py 📝     # Extracts text from PDFs using PyPDF2 (image support commented)
│   ├── preprocess.py 🔍 # Preprocesses PDFs for text extraction
│   ├── nlp.py 🧠     # Structures extracted text into JSON data
│   ├── categorize.py ✅ # Categorizes results (Normal, Borderline, Critical)
│   ├── table_formatter.py 📊 # Formats results for display in tables
│   ├── explain.py 📘 # Generates simple explanations for medical terms
│   ├── summary.py 📋  # Creates bullet-point summaries and recommendations
│   ├── pdf_generator.py 📄 # Generates downloadable PDF summaries
│   ├── streaming.py 💻 # Streams real-time chatbot responses
│   ├── utils.py 🧰   # Helper functions (LLM setup, chat history, CSS)
│   ├── ragas_evaluator.py 📈 # Evaluates chatbot accuracy with RAGAS and stores chat history in MongoDB
│   └── README.md 📚  # Documentation for the src/ folder
├── pages/ 📑         # Streamlit multi-page interface
│   ├── 🧐_Analyze.py 🩺 # Displays analyzed report results and PDF download
│   ├── 🤖_Assistant.py 💬 # RAG chatbot for interactive report questions
│   └── ⚖️_RAGAS_Evaluation.py 📊 # Shows chat history and RAGAS faithfulness metrics
├── 🏠_Home.py 🌐     # Main entry point for uploading and processing reports
├── .env 🔐           # Environment variables (API keys, MongoDB credentials)
├── requirements.txt 📋 # List of Python dependencies
└── README.md 📖      # Main project documentation (this file)
```

## 📑 Pages
- **🏠 Home.py**: Upload reports (PDF, PNG, JPEG) 📤, process them with OCR and AI 🧠, and see a project overview. Results are saved for other pages to use 🔄.
- **🧐 Analyze.py**: Shows patient info 👤, test results in a table 📊, explanations 📘, summaries 📋, and a PDF download button 📥.
- **🤖 Assistant.py**: A friendly chatbot 🤗 that answers questions about your PDF reports, using RAG to stay accurate and relevant 💬. Enable RAGAS evaluation in the sidebar for accuracy checks 📈.
- **⚖️_RAGAS_Evaluation.py**: Displays a detailed evaluation of chatbot responses 📊, showing questions, answers, contexts, and faithfulness scores per user. Ensures the AI’s reliability by analyzing how well answers match the report context ⚖️.

## 🤖 Domain-Specific RAG Chatbot
The **Assistant** page features a domain-specific Retrieval-Augmented Generation (RAG) chatbot, designed to answer questions about your uploaded PDF medical reports 📄. Here’s how it works:
- **PDF-Only**: Only processes PDFs from the Home page’s uploads 📤.
- **Text Extraction**: Uses `PyPDF2` to extract text, splits it into chunks (1000 characters, 200 overlap) for efficient processing 🔍.
- **Vector Search**: `FAISS` and `sentence-transformers` create a vector store to find relevant report sections 🗂️.
- **Smart Answers**: The Groq LLM generates answers based only on your report’s content, avoiding guesses 🤖. It uses a custom prompt to be cheerful for normal results 🎉, hopeful for concerns 💪, and clear when data is missing 🙏.
- **Conversational**: Remembers chat history for follow-up questions 💬, with responses streamed in real-time ⚡.
- **RAGAS Evaluation**: Optionally evaluates responses for accuracy 📈, storing results in MongoDB Atlas for review on the RAGAS Evaluation page ⚖️.
- **Example**: Ask “What does my glucose level mean?” and get a clear, report-specific answer like “Your glucose is 140 mg/dL, which is a bit high ⚠️, suggesting possible prediabetes. Let’s discuss next steps with your doctor! 💪”

### 📊 What We Evaluate with RAGAS
- **Faithfulness Score**: Measures how well the chatbot’s answers align with the report’s context 📏. A score of 1.0 means perfect accuracy, while lower scores indicate deviations or hallucinations.
- **Why We Evaluate**: Ensures the chatbot provides reliable, report-based answers rather than fabricating information 🛡️. This builds trust and supports informed health decisions 🤝.

## 🚀 Getting Started
### Prerequisites
- **Python**: 3.12+ 🐍
- **Groq API Key**: Get one from [GroqCloud](https://console.groq.com/keys) 🔑
- **OpenAI API Key**: Required for RAGAS evaluation, get it from [OpenAI](https://platform.openai.com/api-keys) 🔐
- **MongoDB Atlas**: Set up a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) 🗃️
- **Optional (for PNG/JPEG)**: Install Tesseract OCR (`sudo apt-get install tesseract-ocr` on Ubuntu, `brew install tesseract` on macOS, or add to PATH on Windows) 🖼️

### Installation
1. **Clone the Project** (if using Git):
   ```bash
   git clone https://github.com/MuhammadUmerKhan/Diagnosify-LLM-Powered-Medical-Report-Insights
   cd Diagnosify-LLM-Powered-Medical-Report-Insights
   ```
2. **Set Up Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Key packages:
   ```
   streamlit==1.31.1
   langchain==0.2.0
   langchain-community==0.2.0
   langchain-groq==0.2.0
   langchain-text-splitters==0.2.0
   sentence-transformers==2.7.0
   faiss-cpu==1.8.0
   pypdf2==3.0.1
   reportlab==4.0.9
   python-dotenv==1.0.0
   pandas==2.2.0
   ragas==0.1.8
   pymongo==4.6.3
   opencv-python==4.9.0  # Optional for images
   pytesseract==0.3.10   # Optional for images
   ```
4. **Set API Key and MongoDB**:
   Create a `.env` file:
   ```bash
   GROQ_API_KEY=your-groq-api-key-here
   MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
   MODEL_TEMPERATURE=0.3
   OPENAI_API_KEY=your-openai-api-key-here
   MONGO_USER=your_mongo_user
   MONGO_PASSWORD=your_mongo_password
   MONGO_CLUSTER=cluster0.<random>.mongodb.net
   MONGO_DB=diagnosify
   ```

### Running the App
1. **Start Streamlit**:
   ```bash
   streamlit run 🏠_Home.py
   ```
2. **Access**: Open `http://localhost:8501` in your browser 🌐.
3. **Use the App**:
   - **Home 🏠**: Upload a report 📤 and wait for processing (see status in sidebar ⏳).
   - **Analyze 🧐**: View results, explanations, and download a PDF 📥.
   - **Assistant 🤖**: Ask questions about your PDF report (e.g., “Is my cholesterol okay?”) 💬, enable RAGAS in the sidebar for evaluation 📈.
   - **RAGAS Evaluation ⚖️**: Review chat history and faithfulness scores to verify accuracy 📊.

## 💻 Development Notes
- **UI Style**: Dark theme with neon green text, gold headings, and magenta buttons. Edit CSS in each page’s `st.markdown` for customization 🎨.
- **RAG Tuning**: Adjust `chunk_size` (1000) or `search_kwargs` (`k=2`, `fetch_k=4`) in `🤖_Assistant.py` for better chatbot performance 🔍.
- **Image Support**: Uncomment code in `src/ocr.py` and `src/preprocess.py` for PNG/JPEG processing (requires `opencv-python`, `pytesseract`) 🖼️.
- **Logs**: Check `logs/chatbot.log` for debugging 🐞.
- **RAGAS Tuning**: Modify `evaluate_rag_metrics` in `src/ragas_evaluator.py` to add more metrics (e.g., `answer_relevancy`) for deeper evaluation 📈.
- **Testing**: Add unit tests for `src/` modules and end-to-end tests with sample reports ✅.

## 🐞 Known Issues
- **Image Support**: PNG/JPEG processing is disabled by default (commented in `ocr.py`, `preprocess.py`). Enable it after installing Tesseract and OpenCV 🖼️.
- **Pydantic**: Use `pydantic==1.10.13` if `langchain` raises serialization errors:
   ```bash
   pip install pydantic==1.10.13
   ```
- **Temporary Files**: The `tmp/` folder is cleaned after processing, but ensure disk space is monitored ⏳.
- **RAGAS Dependency**: Ensure OpenAI API key is valid, as RAGAS requires it for evaluation 🔐.

## 🤝 Contributing
Want to help make Diagnosify better? 🙌
1. Fork the repo.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push: `git push origin feature/your-feature`.
5. Submit a pull request with details.

**Ideas**:
- Support more file formats (e.g., DOCX) 📜.
- Improve RAG with advanced retrieval techniques 🔍.
- Add accessibility features (e.g., screen reader support) ♿.
- Enhance RAGAS with additional metrics (e.g., coherence) 📈.
- Write tests for reliability ✅.

## 🌐 Live Demo
Check it out: [Diagnosify Demo](https://smit-hackathon-ai-medical-report-analyzer.streamlit.app/) 🚀

## 📧 Contact
Questions or ideas? Reach out to **Muhammad Umer Khan** at [muhammadumerk546@gmail.com] or [LinkedIn](https://www.linkedin.com/in/muhammad-umer-khan-61729b260/) 🙋‍♂️.

## 🙌 Acknowledgments
- **Groq**: For the powerful LLM API 🤖.
- **Streamlit**: For an awesome UI framework 🌐.
- **OpenAI**: For RAGAS evaluation support 📈.
- **MongoDB Atlas**: For chat history storage 🗃️.
- **Hackathon Team**: For inspiring this project! 🏆