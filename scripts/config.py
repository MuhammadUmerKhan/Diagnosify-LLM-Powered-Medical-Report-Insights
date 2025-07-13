import dotenv, os, logging
from urllib.parse import quote_plus

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

def get_mongo_uri():
    """Construct and return MongoDB Atlas URI from environment variables."""
    try:
        DB_NAME = os.getenv("MONGO_DB", "diagnosify")
        MONGO_USER = os.getenv("MONGO_USER")
        MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
        MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

        if not MONGO_USER or not MONGO_PASSWORD or not MONGO_CLUSTER:
            raise ValueError("❌ MongoDB credentials are missing! Check .env file.")

        MONGO_PASSWORD = quote_plus(MONGO_PASSWORD)
        MONGO_URI = (
            f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{DB_NAME}"
            "?retryWrites=true&w=majority&appName=Cluster0"
        )
        logger.info("✅ MongoDB URI constructed successfully.")
        return MONGO_URI
    except Exception as e:
        logger.error(f"❌ Error constructing MongoDB URI: {e}")
        raise