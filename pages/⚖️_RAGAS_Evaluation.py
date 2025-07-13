import streamlit as st
import pandas as pd
from scripts.ragas_evaluator import get_user_chat_history
from scripts.config import get_logger

# Logger setup
logger = get_logger(__name__)

st.set_page_config(page_title="RAGAS Evaluation", page_icon="📊", layout="wide")

def display_ragas_evaluation():
    """Display user's chat history and RAGAS metrics in a DataFrame."""
    # Sidebar content
    st.sidebar.title("🤖 Medical Report Analyzer")
    st.sidebar.markdown(
        "<p style='color:#00ff99'>This page displays your chat history and RAGAS evaluation metrics for medical report analysis. Navigate to Medical Report Chatbot to ask questions and generate data! 😊</p>",
        unsafe_allow_html=True
    )

    st.header("📊 RAGAS Evaluation")
    st.markdown("<p style='color:#00ff99'>View your questions, answers, contexts, and RAGAS evaluation metrics.</p>", unsafe_allow_html=True)

    # Check if user_id exists in session state
    if "user_id" not in st.session_state:
        st.error("❌ No user session found. Please start a chat session on the Medical Report Chatbot page first.")
        return

    try:
        chats = get_user_chat_history(st.session_state.user_id)
        if not chats:
            st.info("No chat history found. Start asking questions in the Medical Report Chatbot page to see your history and metrics here! 😊")
            return

        # Create DataFrame from chat data
        df = pd.DataFrame([{
            "Question": chat["question"],
            "Answer": chat["generated_answer"],
            "Context": chat["retrieved_context"],
            "Faithfulness Score": chat["faithfulness_score"],
            "Timestamp": chat.get("timestamp", "N/A")
        } for chat in chats])

        # Display DataFrame
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        logger.error(f"❌ Error retrieving RAGAS evaluation data: {e}")
        st.error("❌ Failed to load evaluation data. Please try again.")

if __name__ == "__main__":
    display_ragas_evaluation()