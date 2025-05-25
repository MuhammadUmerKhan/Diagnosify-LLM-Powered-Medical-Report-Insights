import logging
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

os.makedirs(os.path.join("logs"), exist_ok=True)  # 📂 Creates a 'logs' directory if it doesn't exist
logging.basicConfig(  # ⚙️ Configures the logging system with specified settings
    level=logging.INFO,  # 📏 Sets logging level to INFO to capture informational messages and above
    format="%(asctime)s [%(levelname)s] %(message)s",  # 📝 Defines log message format: timestamp, level, and message
    handlers=[  # 📤 Specifies where logs are sent
        logging.FileHandler(os.path.join("logs", "app.log")),  # 📜 Logs to a file named 'logging.log' in the 'logs' directory
        logging.StreamHandler()  # 🖥️ Also logs to the console (standard output)
    ]
)

# Initialize Groq client
try:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    logging.info("GROQ_API_KEY environment variable not set")
except Exception as e:
    logging.exception("Failed to initialize API for categorization")
    raise ValueError("GROQ_API_KEY environment variable not set")

try:
    llm = ChatGroq(api_key=GROQ_API_KEY, model="meta-llama/llama-4-scout-17b-16e-instruct")
except Exception as e:
    logging.exception("Failed to initialize Groq client for categorization")
    raise