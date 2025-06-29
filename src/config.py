import dotenv, os
from src.logger import get_logger

# Configure Logging
logger = get_logger(__name__)

try:
    # Load environment variables
    dotenv.load_dotenv()

    # Load API Key & Model Name
    GROK_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROK_API_KEY:
        logger.warning("⚠️ GROQ_API_KEY is missing. Some features may not work.")

    MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

    # Directory for temporary file storage
    TEMP_DIR = os.path.join("tmp")
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        logger.info(f"✅ Created temporary directory: {TEMP_DIR}")

    logger.info("✅ Configuration loaded successfully.")

except Exception as e:
    logger.error(f"❌ Error loading configuration: {e}")
    raise