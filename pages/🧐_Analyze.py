import streamlit as st
import pandas as pd
from src.table_formatter import format_results_for_table
from src.pdf_generator import generate_pdf_summary
from src.utils import configure_llm
from src.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Medical Report Analyzer", page_icon="🩺", layout="wide")

# Custom CSS
st.markdown("""
<style>
.stApp { 
    color: #00ff99; 
    background: #000000; 
    font-family: 'Arial', sans-serif;
}
.card { 
    background: linear-gradient(135deg, #1c2526, #2e2e2e); 
    border-radius: 15px; 
    padding: 20px; 
    margin-bottom: 20px; 
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7); 
    border: 2px solid #00e5ff;
}
.stButton>button { 
    background: #ff00ff; 
    color: #ffd700; 
    border-radius: 10px; 
    padding: 12px 24px; 
    border: none; 
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.8); 
    font-size: 16px; 
    font-weight: bold;
}
.stButton>button:hover { 
    background: #cc00cc; 
    box-shadow: 0 0 25px rgba(255, 0, 255, 1); 
    transform: scale(1.1); 
    color: #ffffff;
}
h1, h2, h3 { 
    color: #ffd700; 
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
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
    color: #00e5ff; 
    font-size: 16px; 
    line-height: 1.6;
}
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
.stSelectbox label { color: #ffd700; }
.stSelectbox div[data-baseweb="select"] { background: #2e2e2e; color: #00ff99; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Sidebar content
st.sidebar.title("🧐 Analyze Page Overview")
st.sidebar.markdown("""
<p style='color:#00ff99'>This page displays the analyzed results of your medical report, processed on the Home page. View patient information, test results with color-coded statuses, detailed explanations, and a summary with recommendations. Download a PDF report for easy sharing.</p>
""", unsafe_allow_html=True)

# st.sidebar.subheader("📤 Analysis Settings")
configure_llm()

st.header("🩺 AI-Powered Medical Report Analyzer 🌟")
st.markdown("<p style='color:#00ff99; font-size: 18px;'>View your analyzed medical report results here! 🚀</p>", unsafe_allow_html=True)

# Retrieve processed data from session state
metadata = st.session_state.get("metadata", [])
test_results = st.session_state.get("test_results", [])
explanation = st.session_state.get("explanation", None)
summary_bullets = st.session_state.get("summary_bullets", None)
categorized_data = st.session_state.get("categorized_data", [])

if not st.session_state.get("uploaded_files", []) or not test_results:
    st.info("📢 Please upload and analyze a medical report on the Home page first! 🚀")
else:
    try:
        if metadata:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#ffd700'>👤 Patient Information 📋</h3>", unsafe_allow_html=True)
            with st.expander("👁️‍🗨️ View Details"):
                for item in metadata:
                    fields = "<br>".join(f"<b style='color:#ffd700'>{k}</b>: <span style='color:#00ff99'>{v}</span>" for k, v in item.items() if v)
                    st.markdown(fields, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

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

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffd700'>📝 Summary & Recommendations 🌿</h3>", unsafe_allow_html=True)
        if explanation and test_results and summary_bullets:
            if summary_bullets and summary_bullets != "Unable to generate summary due to an error.":
                formatted_summary = summary_bullets.replace("**Summary:**", "<b style='color:#ffd700'>✨ Summary:</b>")
                formatted_summary = formatted_summary.replace("**Risks/Conditions:**", "<b style='color:#ffd700'>🚨 Risks/Conditions:</b>")
                formatted_summary = formatted_summary.replace("**Actions/Recommendations:**", "<b style='color:#ffd700'>✅ Actions/Recommendations:</b>")
                formatted_summary = formatted_summary.replace("* ", "🌟 ").replace("\n", "<br>")
                st.markdown(f"<div class='bullet-point'>{formatted_summary}</div>", unsafe_allow_html=True)
            else:
                st.markdown('<p class="warning">⚠️ No summary generated.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="warning">⚠️ No explanations or test results available for summary.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

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
    except Exception as e:
        st.markdown(f'<p class="warning">❌ Error displaying results: {str(e)}</p>', unsafe_allow_html=True)
        logger.error(f"Error displaying results: {str(e)}")