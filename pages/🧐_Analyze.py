import streamlit as st
import pandas as pd
from scripts.pdf_generator import generate_pdf_summary
from scripts.utils import apply_custom_css
from scripts.config import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Medical Report Analyzer", page_icon="🩺", layout="wide")
apply_custom_css()

def main():
    """Main function for the Analyze page to display medical report results."""
    st.sidebar.title("🧐 Analyze Page Overview")
    st.sidebar.markdown(
        "<p style='color:#00ff99'>This page displays the analyzed results of your medical report, processed on the Home page. View patient information, test results with color-coded statuses, detailed explanations, and a summary with recommendations. Download a PDF report for easy sharing.</p>",
        unsafe_allow_html=True
    )

    st.header("🩺 Medical Report Analysis 🌟")
    st.markdown("<p style='color:#00ff99'>Detailed analysis of your medical report.</p>", unsafe_allow_html=True)

    metadata = st.session_state.get("metadata", [])
    test_results = st.session_state.get("test_results", [])
    explanation = st.session_state.get("explanation", "")
    summary_bullets = st.session_state.get("summary_bullets", "")
    categorized_data = st.session_state.get("categorized_data", [])

    if not st.session_state.get("uploaded_files") or not test_results:
        st.info("📢 Upload and analyze a report on the Home page first.")
        return

    try:
        # Patient Information
        if metadata:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#ffd700'>👤 Patient Information 📋</h3>", unsafe_allow_html=True)
            for item in metadata:
                fields = "<br>".join(
                    f"<b style='color:#ffd700'>{k.capitalize()}</b>: <span style='color:#00ff99'>{v}</span>"
                    for k, v in item.items() if v
                )
                st.markdown(f"<div class='bullet-point'>{fields}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Test Results
        if test_results:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#ffd700'>🧪 Test Results 📊</h3>", unsafe_allow_html=True)
            df = pd.DataFrame(test_results)
            def color_status(val):
                colors = {
                    "Critical": "color: #ff5252; font-weight: bold",
                    "Borderline": "color: #ffca28; font-weight: bold",
                    "Normal": "color: #00ff99; font-weight: bold"
                }
                return colors.get(val, "color: #00ff99")
            styled_df = df.style.applymap(color_status, subset=['status'])
            st.dataframe(styled_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Explanations
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#ffd700'>📘 Explanations 💡</h3>", unsafe_allow_html=True)
            if explanation and "error" not in explanation.lower():
                formatted_explanation = (
                    explanation
                    .replace("**", "<b style='color:#ffd700'>")
                    .replace("**", "</b>")
                    .replace("Critical", "🚨 <span class='critical'>Critical</span>")
                    .replace("Borderline", "⚠️ <span class='borderline'>Borderline</span>")
                    .replace("Normal", "✅ <span class='normal'>Normal</span>")
                )
                st.markdown(formatted_explanation, unsafe_allow_html=True)
            else:
                st.markdown('<p class="warning">⚠️ No explanations generated.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Summary & Recommendations
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffd700'>📝 Summary & Recommendations 🌿</h3>", unsafe_allow_html=True)
        if summary_bullets and "error" not in summary_bullets.lower():
            formatted_summary = (
                summary_bullets
                .replace("**Summary:**", "<b style='color:#ffd700'>✨ Summary:</b>")
                .replace("**Risks/Conditions:**", "<b style='color:#ffd700'>🚨 Risks/Conditions:</b>")
                .replace("**Actions/Recommendations:**", "<b style='color:#ffd700'>✅ Actions/Recommendations:</b>")
                .replace("* ", "🌟 ")
                .replace("\n", "<br>")
            )
            st.markdown(f"<div class='bullet-point'>{formatted_summary}</div>", unsafe_allow_html=True)
        else:
            st.markdown('<p class="warning">⚠️ No summary generated.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # PDF Download
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffd700'>📄 Download Summary 📥</h3>", unsafe_allow_html=True)
        if test_results and explanation:
            if st.button("📄 Generate PDF Summary"):
                pdf_bytes = generate_pdf_summary(categorized_data, explanation, summary_bullets)
                st.download_button(
                    label="💾 Save PDF Report",
                    data=pdf_bytes,
                    file_name="medical_summary.pdf",
                    mime="application/pdf"
                )
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error displaying results: {str(e)}")
        logger.error(f"❌ Error displaying results: {str(e)}")

if __name__ == "__main__":
    main()