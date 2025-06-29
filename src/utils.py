import streamlit as st
from streamlit.logger import get_logger
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import src.config as CONFIG

# Initialize logger
logger = get_logger(__name__)

# Decorator to enable chat history
def enable_chat_history(func):
    """
    Decorator to handle chat history and UI interactions.
    Ensures chat messages persist across interactions.
    """
    current_page = func.__qualname__

    # Clear session state if model/chatbot is switched
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except Exception:
            pass

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your medical report?"}]

    # Display chat history
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """
    Displays a chat message in the UI and appends it to session history.
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def print_qa(cls, question, answer):
    """
    Logs the Q&A interaction for debugging and tracking.
    """
    log_str = f"\nUsecase: {cls.__name__}\nQuestion: {question}\nAnswer: {answer}\n" + "-" * 50
    logger.info(log_str)

@st.cache_resource
def configure_llm():
    """
    Configures and caches the LLM (ChatGroq).
    """
    llm = ChatGroq(
        model_name=CONFIG.MODEL_NAME,
        temperature=0.3,
        groq_api_key=CONFIG.GROK_API_KEY
    )
    return llm

@st.cache_resource
def configure_embedding_model():
    """
    Configures and caches the embedding model.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def configure_vector_embeddings():
    """
    Configures and caches the vector embeddings for Groq API.

    Returns:
        vector_embeddings (HuggingFaceEmbeddings): The loaded vector embeddings.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # Load and return the vector embeddings

def sync_st_session():
    """
    Ensures Streamlit session state values are properly synchronized.
    """
    for k, v in st.session_state.items():
        st.session_state[k] = v