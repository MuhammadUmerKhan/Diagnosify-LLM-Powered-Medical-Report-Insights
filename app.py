import streamlit as st
import os
import tempfile
import logging
import pandas as pd
from src.ocr import extract_text
from src.nlp import structure_data
from src.categorize import categorize_results
from src.table_formatter import format_results_for_table
from src.explain import explain_results_batch
from src.summary import generate_summary_bullet_points
from src.pdf_generator import generate_pdf_summary
from src.chatbot import MedicalChatbot

logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with vibrant colors and dark black background
st.markdown("""
<style>
.stApp { 
    color: #00ff99; /* Neon green for main text */
    background: #000000; /* Solid dark black background */
    font-family: 'Arial', sans-serif;
}
.card { 
    background: linear-gradient(135deg, #1c2526, #2e2e2e); /* Dark gradient for cards */
    border-radius: 15px; 
    padding: 20px; 
    margin-bottom: 20px; 
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7); 
    transition: transform 0.3s, box-shadow 0.3s; 
    border: 2px solid #00e5ff; /* Cyan border */
}
.card:hover { 
    transform: translateY(-10px); 
    box-shadow: 0 15px 35px rgba(0, 229, 255, 0.9); /* Enhanced cyan glow */
}
.stButton>button { 
    background: #ff00ff; /* Magenta buttons */
    color: #ffd700; /* Gold text on buttons */
    border-radius: 10px; 
    padding: 12px 24px; 
    border: none; 
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.8); /* Magenta glow */
    transition: all 0.3s ease; 
    font-size: 16px; 
    font-weight: bold;
}
.stButton>button:hover { 
    background: #cc00cc; /* Darker magenta on hover */
    box-shadow: 0 0 25px rgba(255, 0, 255, 1); 
    transform: scale(1.1); 
    color: #ffffff; /* White text on hover */
}
h1, h2, h3 { 
    color: #ffd700; /* Gold for headings */
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8); /* Gold glow */
    font-family: 'Arial', sans-serif; 
}
.warning { color: #ff5252; font-weight: bold; }
.critical { color: #ff5252; font-weight: bold; }
.borderline { color: #ffca28; font-weight: bold; }
.normal { color: #00ff99; font-weight: bold; }
.stDataFrame { background: #1c2526; border-radius: 10px; padding: 10px; }
.dataframe th { background: #ff00ff !important; color: #ffd700 !important; font-weight: bold !important; }
.dataframe tr:nth-child(even) { background: #2e2e2e; }
.dataframe tr:nth-child(odd) { background: #1c2526; }
.dataframe td { color: #00ff99; }
.bullet-point { 
    margin-left: 20px; 
    color: #00e5ff; /* Cyan bullet points */
    font-size: 16px; 
    line-height: 1.6; 
}
/* Custom Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
    background: #2e2e2e; /* Darker tab background */
    border-radius: 10px;
    padding: 5px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #1c2526;
    color: #00ff99;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #ff00ff;
    color: #ffd700;
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.8);
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: #cc00cc;
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
    color: #ffffff;
}
/* Chat Styling */
.chat-message { 
    padding: 10px; 
    margin-bottom: 10px; 
    border-radius: 10px; 
}
.chat-message.user { background: #ff00ff; color: #ffd700; }
.chat-message.bot { background: #2e2e2e; color: #00ff99; }
.stSidebar { 
    background: #1c2526; 
    color: #00e5ff; 
}
.stSidebar h3 { color: #ffd700; }
.stSidebar p { color: #00ff99; }
</style>
""", unsafe_allow_html=True)

# Sidebar content (visible on all tabs)
st.sidebar.title("📋 About the Project 🌐")
st.sidebar.markdown("""
<p style='color:#00ff99'><b>AI Medical Report Analyzer</b> 🎯</p>
<p style='color:#00e5ff'>Crafted for the Hackathon by <b><a href="https://www.linkedin.com/in/muhammad-umer-khan-61729b260/">Muhammad Umer Khan</a></b> 💻<br>
This app harnesses cutting-edge AI to extract, categorize, and explain medical test results, delivering clear, patient-friendly insights! ✨🚪<br>
<b>Powered by Groq LLM and Streamlit</b> ⚡</p>
""", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color:#00e5ff'>", unsafe_allow_html=True)

# Single file uploader in sidebar
st.sidebar.subheader("📤 Upload Medical Report 🌡️")
uploaded_files = st.sidebar.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True, key="global_uploader")

# Tabs navigation
tab1, tab2, tab3 = st.tabs(["🏠 Home", "🩺 Analyze", "💬 Chatbot"])

# Home Tab
with tab1:
    st.title("🏠 Welcome to AI Medical Report Analyzer 🌟")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:#ffd700'>Project Overview 🎯</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style='color:#00ff99'>The AI Medical Report Analyzer is a cutting-edge application designed to simplify the interpretation of medical reports. Built for the Hackathon, it leverages advanced AI to extract, categorize, and explain test results, providing clear and patient-friendly insights.</p>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#ffd700'>Tech Stack 💻</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class='bullet-point'>
            🌟 <b>Streamlit</b>: For building the interactive web interface.<br>
            🌟 <b>Groq LLM</b>: Powers natural language processing and explanation generation.<br>
            🌟 <b>OpenCV & Pytesseract</b>: For OCR to extract text from images and PDFs.<br>
            🌟 <b>Pandas</b>: For data manipulation and table formatting.<br>
            🌟 <b>ReportLab</b>: For generating PDF summaries.<br>
            🌟 <b>Python</b>: The core programming language.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#ffd700'>Workflow 🔄</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class='bullet-point'>
            🌟 <b>Upload</b>: Users upload a medical report (PDF, PNG, or JPEG).<br>
            🌟 <b>OCR Extraction</b>: Text is extracted using OCR technology.<br>
            🌟 <b>NLP Structuring</b>: Data is structured and categorized using NLP.<br>
            🌟 <b>Analysis</b>: Test results are analyzed and explained by Groq LLM.<br>
            🌟 <b>Summary</b>: A concise summary with risks and recommendations is generated.<br>
            🌟 <b>PDF Export</b>: Users can download a detailed PDF report.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#ffd700'>Features ✨</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class='bullet-point'>
            🌟 <b>OCR Support</b>: Handles multiple file formats (PDF, PNG, JPEG).<br>
            🌟 <b>AI Insights</b>: Provides detailed explanations of test results.<br>
            🌟 <b>Customizable Output</b>: Color-coded statuses and downloadable PDFs.<br>
            🌟 <b>User-Friendly</b>: Intuitive interface with patient-friendly language.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#ffd700'>Team 👥</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style='color:#00ff99'>Developed by <b><a href="https://www.linkedin.com/in/muhammad-umer-khan-61729b260/">Muhammad Umer Khan</a></b> with dedication and innovation for the Hackathon! 🚀</p>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#ffd700'>Get Started 🎉</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Analyze Tab
with tab2:
    st.title("🩺✨ AI-Powered Medical Report Analyzer 🌟")
    st.markdown("<p style='color:#00ff99; font-size: 18px;'>Your uploaded medical report will be analyzed here! 🚀🎉</p>", unsafe_allow_html=True)

    # Processing Status in sidebar
    st.sidebar.subheader("⏳ Processing Status")
    status_placeholder = st.sidebar.empty()

    if uploaded_files:
        with st.spinner("🔄 Analyzing your report... 🕒"):
            try:
                # Use the first file for analysis (single file mode for simplicity)
                if len(uploaded_files) > 1:
                    st.warning("⚠️ Using only the first uploaded file for analysis.")
                uploaded_file = uploaded_files[0]
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name

                # Step 1: OCR
                raw_text = extract_text(tmp_file_path)
                if not raw_text:
                    st.warning("⚠️ No text extracted from the file.")
                    raise ValueError("Text extraction failed")

                # Step 2: NLP Structuring
                structured_data = structure_data(raw_text)
                if not structured_data:
                    st.warning("⚠️ No structured data extracted.")
                    raise ValueError("Data structuring failed")

                # Step 3: Categorization
                categorized_data = categorize_results(structured_data)
                if not categorized_data:
                    st.warning("⚠️ No categorized data generated.")
                    raise ValueError("Categorization failed")

                # Filter test results and metadata
                test_results = [r for r in categorized_data if "test_name" in r or "Test" in r]
                metadata = [r for r in categorized_data if "test_name" not in r and "Test" not in r]

                # Display metadata in a card
                if metadata:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("<h3 style='color:#ffd700'>👤 Patient Information 📋</h3>", unsafe_allow_html=True)
                    with st.expander("👁️‍🗨️ View Details"):
                        for item in metadata:
                            fields = "<br>".join(f"<b style='color:#ffd700'>{k}</b>: <span style='color:#00ff99'>{v}</span>" for k, v in item.items() if v)
                            st.markdown(fields, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Step 5: Format Table and Explanations
                if test_results:
                    table_data = format_results_for_table(test_results)
                    if table_data:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown("<h3 style='color:#ffd700'>🧪 Test Results 📊</h3>", unsafe_allow_html=True)
                        df = pd.DataFrame(table_data)
                        def color_status(val):
                            if val == "Critical":
                                return 'color: #ff5252; font-weight: bold'
                            elif val == "Borderline":
                                return 'color: #ffca28; font-weight: bold'
                            elif val == "Normal":
                                return 'color: #00ff99; font-weight: bold'
                            return 'color: #00ff99'
                        styled_df = df.style.map(color_status, subset=['status'])
                        st.dataframe(styled_df, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown("<h3 style='color:#ffd700'>📘 Explanations 💡</h3>", unsafe_allow_html=True)
                        explanation = explain_results_batch(test_results)
                        if explanation and explanation != "Unable to generate explanations due to an error.":
                            formatted_explanation = explanation.replace("**", "<b style='color:#ffd700'>").replace("**", "</b>")
                            formatted_explanation = formatted_explanation.replace("Critical", "🚨 <span class='critical'>Critical</span>").replace("Borderline", "⚠️ <span class='borderline'>Borderline</span>").replace("Normal", "✅ <span class='normal'>Normal</span>")
                            st.markdown(formatted_explanation, unsafe_allow_html=True)
                        else:
                            st.markdown('<p class="warning">⚠️ No explanations generated.</p>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="warning">⚠️ No test data found to display.</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="warning">⚠️ No test results found.</p>', unsafe_allow_html=True)

                # Step 7: Summary, Risks, Actions with consistent bullet points
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h3 style='color:#ffd700'>📝 Summary & Recommendations 🌿</h3>", unsafe_allow_html=True)
                if explanation and test_results:
                    summary_bullets = generate_summary_bullet_points(explanation)
                    if summary_bullets and summary_bullets != "Unable to generate summary due to an error.":
                        formatted_summary = summary_bullets.replace("**Summary:**", "<b style='color:#ffd700'>✨ Summary:</b>")
                        formatted_summary = formatted_summary.replace("**Risks/Conditions:**", "<b style='color:#ffd700'>🚨 Risks/Conditions:</b>")
                        formatted_summary = formatted_summary.replace("**Actions/Recommendations:**", "<b style='color:#ffd700'>✅ Actions/Recommendations:</b>")
                        formatted_summary = formatted_summary.replace("* ", "🌟 ").replace("\n", "<br>")
                        st.markdown(f"<div class='bullet-point'>{formatted_summary}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="warning">⚠️ No summary generated.</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="warning">⚠️ No explanations available for summary.</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Step 8: Generate PDF Summary
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h3 style='color:#ffd700'>📄 Download Summary 📥</h3>", unsafe_allow_html=True)
                if test_results and explanation:
                    if st.button("📄 Generate PDF Summary 🌟"):
                        pdf_bytes = generate_pdf_summary(categorized_data, explanation, summary_bullets)
                        st.download_button(
                            label="💾 Save PDF Report 🎯",
                            data=pdf_bytes,
                            file_name="medical_summary.pdf",
                            mime="application/pdf"
                        )
                st.markdown('</div>', unsafe_allow_html=True)

                # Clean up
                os.unlink(tmp_file_path)
                logger.info(f"Temporary file deleted: {tmp_file_path}")
                status_placeholder.markdown("<p style='color:#00ff99'>✅ Report processed successfully! 🎉</p>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<p class="warning">❌ Error: {str(e)}</p>', unsafe_allow_html=True)
                logger.error(f"Error processing file: {str(e)}")
                status_placeholder.markdown("<p style='color:#ff5252'>❌ Processing failed! ⚠️</p>", unsafe_allow_html=True)
    else:
        st.info("📢 Please upload a medical report using the sidebar to start analyzing! 🚀")

# Chatbot Tab
with tab3:
    st.session_state["current_page"] = "chatbot"
    chatbot_obj = MedicalChatbot(uploaded_files)  # Pass uploaded files to chatbot
    chatbot_obj.main()