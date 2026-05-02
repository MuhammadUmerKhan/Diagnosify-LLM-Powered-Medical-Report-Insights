import streamlit as st, os, tempfile
from scripts.ocr import extract_text
from scripts.processing import  \
        (structure_data, categorize_results, format_results_for_table, explain_results_batch, generate_summary_bullet_points)
from scripts.utils import configure_llm, apply_custom_css
from scripts.config import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Medical Report Analyzer", page_icon="🩺", layout="wide")

apply_custom_css()

st.sidebar.subheader("🏠 Home Page Overview")
st.sidebar.markdown("""
<p style='color:#00ff99'>This page analyzes medical reports. Check results on the Analyze tab or ask questions on the Assistant tab.</p>
""", unsafe_allow_html=True)

st.sidebar.subheader("📤 Upload Medical Reports 🌡️")
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
uploaded_files = st.sidebar.file_uploader('Upload reports', type=["pdf"], accept_multiple_files=True, key="global_uploader", label_visibility="collapsed")
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    # Clear previous analysis results when new files are uploaded
    for key in ["metadata", "test_results", "explanation", "summary_bullets", "categorized_data"]:
        if key in st.session_state:
            del st.session_state[key]

configure_llm()
st.sidebar.subheader("⏳ Processing Status")
status_placeholder = st.sidebar.empty()

st.header("🏠 AI Medical Report Analyzer 🌟")
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#ffd700'>Project Overview 🎯</h2>", unsafe_allow_html=True)
st.markdown("""
<p style='color:#00ff99'>The AI Medical Report Analyzer simplifies medical report interpretation using advanced AI to extract, categorize, and explain test results in patient-friendly language.</p>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#ffd700'>Tech Stack 💻</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='bullet-point'>
    🌟 <b>Streamlit</b>: Interactive web interface.<br>
    🌟 <b>Groq LLM</b>: NLP and explanation generation.<br>
    🌟 <b>OpenCV & Pytesseract</b>: OCR for text extraction.<br>
    🌟 <b>Pandas</b>: Data manipulation and tables.<br>
    🌟 <b>ReportLab</b>: PDF summaries.<br>
    🌟 <b>Python</b>: Core language.
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#ffd700'>Workflow 🔄</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='bullet-point'>
    🌟 <b>Upload</b>: Upload medical reports (PDF, PNG, JPEG) in the sidebar.<br>
    🌟 <b>OCR Extraction</b>: Extract text using OCR.<br>
    🌟 <b>NLP Structuring</b>: Structure data with NLP.<br>
    🌟 <b>Analysis</b>: Analyze and explain results with Groq LLM.<br>
    🌟 <b>Summary</b>: Generate concise summaries with risks.<br>
    🌟 <b>PDF Export</b>: Download detailed PDF reports from the Analyze tab.
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#ffd700'>Features ✨</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='bullet-point'>
    🌟 <b>OCR Support</b>: Handles PDF, PNG, JPEG.<br>
    🌟 <b>AI Insights</b>: Detailed result explanations.<br>
    🌟 <b>Customizable Output</b>: Color-coded statuses and PDFs.<br>
    🌟 <b>User-Friendly</b>: Intuitive, patient-friendly interface.
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#ffd700'>Team 👥</h2>", unsafe_allow_html=True)
st.markdown("""
<p style='color:#00ff99'>Developed by <b><a href="https://www.linkedin.com/in/muhammad-umer-khan-61729b260/">Muhammad Umer Khan</a></b> for the Hackathon! 🚀</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Process uploaded files
if uploaded_files:
    with st.spinner("🔄 Analyzing your report... 🕒"):
        try:
            if len(uploaded_files) > 1:
                st.warning("⚠️ Using only the first uploaded file for analysis.")
            uploaded_file = uploaded_files[0]
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            raw_text = extract_text(tmp_file_path)
            if not raw_text:
                st.warning("⚠️ No text extracted from the file.")
                raise ValueError("Text extraction failed")

            structured_data = structure_data(raw_text)
            if not structured_data:
                st.warning("⚠️ No structured data extracted.")
                raise ValueError("Data structuring failed")

            categorized_data = categorize_results(structured_data)
            if not categorized_data:
                st.warning("⚠️ No categorized data generated.")
                raise ValueError("Categorization failed")

            # Use dedicated formatter for table results
            test_results = format_results_for_table(categorized_data)
            
            # Extract metadata (non-test entries)
            # Metadata is usually what's NOT in the formatted test results
            test_names_in_table = {r.get("test_name") for r in test_results}
            metadata = [r for r in categorized_data if r.get("test_name") not in test_names_in_table and "Test" not in str(r.keys())]
            
            explanation = explain_results_batch(test_results) if test_results else None
            summary_bullets = generate_summary_bullet_points(explanation) if explanation and test_results else None

            # Store results in session state
            st.session_state.metadata = metadata
            st.session_state.test_results = test_results
            st.session_state.explanation = explanation
            st.session_state.summary_bullets = summary_bullets
            st.session_state.categorized_data = categorized_data

            os.unlink(tmp_file_path)
            logger.info(f"✅ Temporary file deleted: {tmp_file_path}")
            status_placeholder.markdown("<p style='color:#00ff99'>✅ Report processed successfully!</p>", unsafe_allow_html=True)
            st.info("✅ Analysis complete! Please navigate to the Analyze tab to view detailed results or the Assistant tab to ask questions about your report.")
        except Exception as e:
            st.markdown(f'<p class="warning">❌ Error: {str(e)}</p>', unsafe_allow_html=True)
            logger.error(f"❌ Error processing file: {str(e)}")
            status_placeholder.markdown("<p style='color:#ff5252'>❌ Processing failed! ⚠️</p>", unsafe_allow_html=True)
else:
    st.sidebar.info("📢 Please upload a medical report using the sidebar to start analyzing! 🚀")