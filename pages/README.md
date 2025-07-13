# 📄 Pages README 🌟

## 📖 Overview
The **AI Medical Report Analyzer** 🩺 is a Streamlit app that helps patients understand medical reports by processing, analyzing, and explaining test results in a friendly way. The app has four main pages: **Home** 🏠, **Analyze** 🧐, **Assistant** 🤖, and **RAGAS Evaluation** ⚖️. These pages work together to upload reports, process data, display results, answer questions, and evaluate chat accuracy, all powered by the `src/` folder’s AI and processing modules. Built with a vibrant, dark-themed UI, it’s intuitive and supportive 😊.

## 📑 Pages
Here’s what each page does:

- **🏠 Home.py**  
  - **What it does**: The starting point where users upload medical reports (PDF, PNG, JPEG) 📤 and the app processes them using OCR and AI 🧠. It extracts text, structures data, categorizes results, generates explanations, and creates summaries, storing everything in `st.session_state` for other pages.
  - **Key Features**: File upload, real-time processing status in the sidebar ⏳, project overview, tech stack, workflow, and team info. After processing, users are prompted to visit the Analyze or Assistant pages 🚀.
  - **Sidebar**: Upload widget, processing status (✅ or ❌), and LLM settings ⚙️.

- **🧐 Analyze.py**  
  - **What it does**: Displays the analyzed results from the Home page in a clear, organized way 📊. Shows patient info, test results with color-coded statuses (Normal ✅, Borderline ⚠️, Critical 🚨), detailed explanations, a summary with recommendations, and a downloadable PDF report 📄.
  - **Key Features**: Interactive tables, expandable patient details, and a button to generate/save a PDF summary 💾. If no data is processed, it prompts users to upload on the Home page.
  - **Sidebar**: Overview of the page’s display-focused role and LLM settings ⚙️.

- **🤖 Assistant.py**  
  - **What it does**: A friendly AI chatbot 🤗 that answers questions about uploaded PDF reports using Retrieval-Augmented Generation (RAG). It provides accurate, context-aware responses with a supportive tone, adjusting based on report findings (cheerful for normal 🎉, hopeful for concerns 💪).
  - **Key Features**: Chat interface with conversational history, emoji-rich responses, and PDF-only processing. It uses AI to fetch relevant report details for precise answers 🔎.
  - **Sidebar**: Chatbot overview and LLM settings ⚙️.

- **⚖️_RAGAS_Evaluation.py**  
  - **What it does**: Displays a detailed evaluation of the AI chatbot’s responses using RAGAS (Retrieval-Augmented Generation Assessment) metrics 📈. It shows user-specific chat history, including questions, answers, contexts, and faithfulness scores, ensuring the chatbot’s accuracy and reliability.
  - **Key Features**: Interactive DataFrame with chat history, filtered by `user_id`, and real-time updates from the Assistant page. If no chats exist, it prompts users to start a session on the Assistant page 😊.
  - **Sidebar**: Overview of the page’s evaluation role and navigation guidance to the Assistant page ⚙️.

## 🚀 Usage
1. **Run the app**: Use `streamlit run 🏠_Home.py` to start the app 🌐.
2. **Upload reports**: On the Home page, upload medical reports (PDF, PNG, JPEG) via the sidebar 📤.
3. **Process reports**: Home processes the first uploaded file, showing status (e.g., “✅ Report processed successfully!”) ⏳.
4. **View results**: Go to the Analyze page to see patient info, test results, explanations, and download a PDF report 🧐.
5. **Ask questions**: Use the Assistant page to chat with the AI about PDF reports, getting clear, friendly answers 🤖.
6. **Evaluate chats**: Visit the RAGAS Evaluation page to review chat history and RAGAS metrics for accuracy ⚖️.
7. **Dependencies**: Ensure `src/` folder modules and `requirements.txt` packages are installed (e.g., `streamlit`, `langchain`, `pypdf2`, `reportlab`, `ragas`, `pymongo`).

## 💡 Notes
- **File Support**: Home and Analyze support PDF, PNG, JPEG; Assistant supports only PDF 📄.
- **Session State**: Results and chat data are stored in `st.session_state` to share across pages. New uploads on Home clear old results to avoid confusion 🔄.
- **UI Style**: Dark theme with neon green text, gold headings, and magenta buttons for a vibrant, user-friendly look ✨.
- **Image Processing**: PNG/JPEG support requires uncommenting code in `src/ocr.py` and `src/preprocess.py` and installing `opencv-python` and `pytesseract` 🖼️.
- **Logs**: Debug logs are saved in `logs/chatbot.log` via `src/logger.py` 🐞.
- **RAGAS Evaluation**: Requires an OpenAI API key for metrics and a MongoDB Atlas connection for storing chat history ⚙️.

## 👨‍💻 Developer
Created by **Muhammad Umer Khan** for a hackathon 🎉. Reach out on [LinkedIn](https://www.linkedin.com/in/muhammad-umer-khan-61729b260/) for questions or feedback! 🙌