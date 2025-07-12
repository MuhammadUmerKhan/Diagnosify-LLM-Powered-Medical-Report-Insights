import dotenv, os
import logging

# Configure Logging
logging.basicConfig(
    filename=os.path.join("logs", "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def get_logger(name):
    """Return a logger instance."""
    return logging.getLogger(name)

try:
    # Load environment variables
    dotenv.load_dotenv()

    # Load API Key & Model Name
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    TEMPERATURE: float = os.getenv("MODEL_TEMPERATURE")

    # Directory for temporary file storage
    TEMP_DIR = os.path.join("tmp")
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        logger.info(f"✅ Created temporary directory: {TEMP_DIR}")

    logger.info("✅ Configuration loaded successfully.")

except Exception as e:
    logger.error(f"❌ Error loading configuration: {e}")
    raise