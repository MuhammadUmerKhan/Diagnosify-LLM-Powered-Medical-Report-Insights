# 🩺 Diagnosify: AI-Powered Medical Report Insights 🌟

## 📖 Overview
**Diagnosify** is a user-friendly Streamlit app that makes medical reports easy to understand for everyone! 🩺 Built for a hackathon, it uses advanced AI to extract, analyze, and explain test results from reports (PDF, PNG, JPEG) 📄. With a vibrant dark theme, it offers clear insights, summaries, and a smart chatbot to answer your health questions in a supportive way 😊. Whether you’re checking test results or asking about your report, Diagnosify is here to help! 🚀

![](https://img.freepik.com/premium-vector/medical-check-list-health-analysis-research-report-illustration-flat-cartoon-design_101884-86.jpg)

### 🎯 Goals
- **Extract**: Pull text from reports using OCR 📝.
- **Analyze**: Categorize and explain results with AI 🧠.
- **Summarize**: Provide simple summaries with health tips 📋.
- **Chat**: Answer questions about your report with a friendly AI chatbot 🤗.
- **Share**: Download a PDF summary to share with your doctor 📥.

### ✨ Features
- **Multi-Format Support**: Upload PDFs, PNGs, or JPEGs 📄🖼️.
- **AI Insights**: Groq LLM explains results in patient-friendly language 🌟.
- **Color-Coded Results**: Shows Normal ✅, Borderline ⚠️, or Critical 🚨 statuses.
- **RAG Chatbot**: A domain-specific chatbot answers questions based only on your uploaded PDFs, using Retrieval-Augmented Generation (RAG) for accurate, context-aware replies 💬.
- **PDF Export**: Save a professional PDF summary of your results 📄.
- **Cool UI**: Dark theme with neon green text, gold headings, and magenta buttons 🎨.

## 🛠️ Tech Stack
- **Frontend**: Streamlit for an interactive web interface 🌐.
- **Backend**: Python for all processing 🐍.
- **AI/LLM**: Groq LLM (`meta-llama/llama-4-scout-17b-16e-instruct`) via `langchain-groq` 🤖.
- **OCR**: `PyPDF2` for PDFs, `opencv-python` & `pytesseract` (optional for images) 📝.
- **Data**: `pandas` for tables, `langchain` for AI processing 📊.
- **RAG**: `FAISS` and `sentence-transformers` for chatbot’s document search 🔍.
- **PDFs**: `reportlab` for generating summaries 📄.
- **Config**: `python-dotenv` for secure API key management 🔐.

## 📂 Project Structure
```
MedicalReportAnalyzer/
├── logs/ 📋           # Logs app activity (chatbot.log)
├── tmp/ ⏳            # Temporary files for processing
├── src/ 🛠️           # Core logic modules
│   ├── config.py ⚙️  # Loads API key and sets up temp folder
│   ├── logger.py 🐞  # Sets up logging
│   ├── ocr.py 📝     # Extracts text from PDFs (image support commented)
│   ├── preprocess.py 🔍 # Preprocesses PDFs for text extraction
│   ├── nlp.py 🧠     # Structures text into JSON data
│   ├── categorize.py ✅ # Adds status (Normal, Borderline, Critical)
│   ├── table_formatter.py 📊 # Formats results for tables
│   ├── explain.py 📘 # Explains results in simple language
│   ├── summary.py 📋  # Creates bullet-point summaries
│   ├── pdf_generator.py 📄 # Generates PDF summaries
│   ├── streaming.py 💻 # Streams chatbot responses
│   ├── utils.py 🧰   # Helper functions (LLM, chat history)
│   └── README.md 📚  # Src folder documentation
├── pages/ 📑         # Streamlit pages
│   ├── 🧐_Analyze.py 🩺 # Displays analysis results
│   ├── 🤖_Assistant.py 💬 # RAG chatbot for questions
├── 🏠_Home.py 🌐     # Main app entry (uploads & processes)
├── .env 🔐           # Stores GROQ_API_KEY
├── requirements.txt 📋 # Python dependencies
└── README.md 📖      # This file
```

## 📑 Pages
- **🏠 Home.py**: Upload reports (PDF, PNG, JPEG) 📤, process them with OCR and AI 🧠, and see a project overview. Results are saved for other pages to use 🔄.
- **🧐 Analyze.py**: Shows patient info 👤, test results in a table 📊, explanations 📘, summaries 📋, and a PDF download button 📥.
- **🤖 Assistant.py**: A friendly chatbot 🤗 that answers questions about your PDF reports, using RAG to stay accurate and relevant 💬.

## 🤖 Domain-Specific RAG Chatbot
The **Assistant** page features a domain-specific Retrieval-Augmented Generation (RAG) chatbot, designed to answer questions about your uploaded PDF medical reports 📄. Here’s how it works:
- **PDF-Only**: Only processes PDFs from the Home page’s uploads 📤.
- **Text Extraction**: Uses `PyPDF2` to extract text, splits it into chunks (1000 characters, 200 overlap) for efficient processing 🔍.
- **Vector Search**: `FAISS` and `sentence-transformers` create a vector store to find relevant report sections 🗂️.
- **Smart Answers**: The Groq LLM generates answers based only on your report’s content, avoiding guesses 🤖. It uses a custom prompt to be cheerful for normal results 🎉, hopeful for concerns 💪, and clear when data is missing 🙏.
- **Conversational**: Remembers chat history for follow-up questions 💬, with responses streamed in real-time ⚡.
- **Example**: Ask “What does my glucose level mean?” and get a clear, report-specific answer like “Your glucose is 140 mg/dL, which is a bit high ⚠️, suggesting possible prediabetes. Let’s discuss next steps with your doctor! 💪”

## 🚀 Getting Started
### Prerequisites
- **Python**: 3.12+ 🐍
- **Groq API Key**: Get one from [GroqCloud](https://console.groq.com/keys) 🔑
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
   opencv-python==4.9.0  # Optional for images
   pytesseract==0.3.10   # Optional for images
   ```
4. **Set API Key**:
   Create a `.env` file:
   ```bash
   echo "GROQ_API_KEY=your-api-key-here" > .env
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
   - **Assistant 🤖**: Ask questions about your PDF report (e.g., “Is my cholesterol okay?”) 💬.

## 💻 Development Notes
- **UI Style**: Dark theme with neon green text, gold headings, and magenta buttons. Edit CSS in each page’s `st.markdown` for customization 🎨.
- **RAG Tuning**: Adjust `chunk_size` (1000) or `search_kwargs` (`k=2`, `fetch_k=4`) in `🤖_Assistant.py` for better chatbot performance 🔍.
- **Image Support**: Uncomment code in `src/ocr.py` and `src/preprocess.py` for PNG/JPEG processing (requires `opencv-python`, `pytesseract`) 🖼️.
- **Logs**: Check `logs/chatbot.log` for debugging 🐞.
- **Testing**: Add unit tests for `src/` modules and end-to-end tests with sample reports ✅.

## 🐞 Known Issues
- **Image Support**: PNG/JPEG processing is disabled by default (commented in `ocr.py`, `preprocess.py`). Enable it after installing Tesseract and OpenCV 🖼️.
- **Pydantic**: Use `pydantic==1.10.13` if `langchain` raises serialization errors:
   ```bash
   pip install pydantic==1.10.13
   ```
- **Temporary Files**: The `tmp/` folder is cleaned after processing, but ensure disk space is monitored ⏳.

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
- Write tests for reliability ✅.

## 🌐 Live Demo
Check it out: [Diagnosify Demo](https://smit-hackathon-ai-medical-report-analyzer.streamlit.app/) 🚀

## 📧 Contact
Questions or ideas? Reach out to **Muhammad Umer Khan** at [muhammadumerk546@gmail.com] or [LinkedIn](https://www.linkedin.com/in/muhammad-umer-khan-61729b260/) 🙋‍♂️.

## 🙌 Acknowledgments
- **Groq**: For the powerful LLM API 🤖.
- **Streamlit**: For an awesome UI framework 🌐.
- **Hackathon Team**: For inspiring this project! 🏆
