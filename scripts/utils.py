import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.callbacks import BaseCallbackHandler
from reportlab.lib import colors
from reportlab.platypus import TableStyle
import scripts.config as CONFIG

logger = CONFIG.get_logger(__name__)

# Check if API key is available
if not CONFIG.GROQ_API_KEY:
    st.error("❌ Missing API Token!")
    st.stop()  # Stop execution if API token is missing

# Singleton LLM instance
_llm_instance = None

@st.cache_resource
def configure_llm():
    """Configures and caches a singleton LLM (ChatGroq) instance."""
    global _llm_instance
    if _llm_instance is None:
        logger.info("Initializing singleton ChatGroq LLM instance")
        _llm_instance = ChatGroq(
            model_name=CONFIG.MODEL_NAME,
            temperature=CONFIG.TEMPERATURE,
            groq_api_key=CONFIG.GROQ_API_KEY
        )
    return _llm_instance

@st.cache_resource
def configure_embedding_model():
    """Configures and caches the embedding model."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_llm_prompt(system_role: str, task_instructions: str, input_data: str) -> list:
    """Creates a standardized LLM prompt with system and human messages."""
    return [
        SystemMessage(content=system_role),
        HumanMessage(content=f"""
            {task_instructions}
            Input:
            {input_data}
            """)
    ]

def get_default_table_style() -> TableStyle:
    """Returns a default TableStyle for PDF tables."""
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ])

def stream_llm_response(messages: list, container) -> str:
    """Streams LLM response to a Streamlit container."""
    class StreamHandler(BaseCallbackHandler):
        def __init__(self, container, initial_text=""):
            self.container = container
            self.text = initial_text
        def on_llm_new_token(self, token: str, **kwargs):
            self.text += token
            self.container.markdown(self.text)
    
    handler = StreamHandler(container)
    response = configure_llm().stream(messages, callbacks=[handler])
    return "".join(response.content for response in response)

def enable_chat_history(func):
    """Decorator to handle chat history and UI interactions."""
    current_page = func.__qualname__

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your medical report?"}]

    # Clear cache only if explicitly requested
    if "current_page" in st.session_state and st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            st.session_state["current_page"] = current_page
        except Exception:
            pass

    # Display chat history
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Displays a chat message in the UI and appends it to session history."""
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def print_qa(cls, question, answer):
    """Logs the Q&A interaction for debugging and tracking."""
    log_str = f"\nUsecase: {cls.__name__}\nQuestion: {question}\nAnswer: {answer}\n" + "-" * 50
    logger.info(log_str)

def apply_custom_css():
    """Applies custom CSS for Streamlit pages."""
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