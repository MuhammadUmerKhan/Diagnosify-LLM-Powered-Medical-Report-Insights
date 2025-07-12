# 📂 Scripts Folder - AI Medical Report Analyzer 🩺

Welcome to the `scripts` folder! This is the heart of the **AI Medical Report Analyzer**, a tool that makes medical reports easy to understand by turning complex data into clear, patient-friendly insights. These scripts handle everything from reading PDF reports to generating summaries and powering a chatbot. Let’s dive in! 🚀

## 🎯 What Does This Folder Do?

The scripts in this folder work together to:
- 📜 **Read** PDF medical reports and extract text.
- 🧠 **Analyze** the data using AI to structure, categorize, and explain results.
- 📊 **Display** results in tables and create downloadable PDF summaries.
- 💬 **Answer** user questions about their reports through a friendly chatbot.
- ⚙️ **Support** the app with utilities like logging and AI model setup.

## 📂 Files in This Folder

Here’s a quick look at each script and its role:

- **`ocr.py`** 📄  
  Extracts text from PDF medical reports using PyPDF2. It’s the first step to get raw data from your uploaded files.

- **`utils.py`** 🛠️  
  Contains helper functions like setting up the AI model, styling PDF tables, and managing chat history for the Streamlit app. It’s the toolbox for the project!

- **`streaming.py`** 📡  
  Powers real-time chat updates by streaming AI responses to the user interface. Makes the chatbot feel lively and responsive! 😊

- **`pdf_generator.py`** 📑  
  Creates downloadable PDF summaries with patient info, test results, explanations, and recommendations. Perfect for sharing with doctors!

- **`processing.py`** 🧪  
  The brain of the app! It structures report data, categorizes results (e.g., Normal, Critical), explains them in simple language, and generates bullet-point summaries.

- **`config.py`** ⚙️  
  Sets up the app’s settings, like the AI model’s API key, logging, and temporary file storage. Keeps everything organized and running smoothly.

## 🚀 How It Works

1. **Upload a Report** 📤  
   Upload a PDF report through the Streamlit app. `ocr.py` extracts the text.

2. **Process the Data** 🧠  
   `processing.py` uses AI (via Groq LLM) to:
   - Structure the text into data (e.g., test names, values).
   - Categorize results (Normal, Borderline, Critical).
   - Explain results in simple words.
   - Summarize key findings and next steps.

3. **Display Results** 📊  
   The app shows patient details, test results, and explanations. `utils.py` helps style the interface and manage chats.

4. **Generate Summaries** 📑  
   `pdf_generator.py` creates a neat PDF with all the details, ready to download.

5. **Chat with the Bot** 💬  
   `streaming.py` powers a chatbot (in `assistant.py`) that answers your questions about the report in real-time.

## 🛠️ Key Features

- **User-Friendly**: Explanations are simple and clear, perfect for non-medical folks! 😊
- **AI-Powered**: Uses Groq LLM for smart data processing and answers.
- **Interactive**: Real-time chat and downloadable PDFs make it easy to use.
- **Reliable**: Strong error handling ensures the app doesn’t crash.

## 📋 Requirements

To run these scripts, you’ll need:
- **Python 3.8+** 🐍
- **Libraries**: Install via `requirements.txt` (includes Streamlit, PyPDF2, LangChain, ReportLab, etc.)
- **Groq API Key**: Set it in a `.env` file for AI features (see `config.py`).

## 🌟 How to Use

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**:
   Create a `.env` file with:
   ```bash
   GROQ_API_KEY=your_api_key_here
   MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
   MODEL_TEMPERATURE=0.3
   ```

3. **Run the App**:
   Start the Streamlit app with:
   ```bash
   streamlit run home.py
   ```

4. **Upload & Explore**:
   - Upload a PDF report on the Home page.
   - Check results on the Analyze page.
   - Ask questions via the Assistant page.

## 🛡️ Notes

- **PDF Only**: Currently, only PDF reports are supported (image support is commented out for future use).
- **Logging**: Errors and progress are logged in `logs/app.log` for debugging.
- **Temporary Files**: Stored in `tmp/` and cleaned up after use.

## 👥 Contributor

Developed with ❤️ by [Muhammad Umer Khan](https://www.linkedin.com/in/muhammad-umer-khan-61729b260/) for a hackathon project! 🚀