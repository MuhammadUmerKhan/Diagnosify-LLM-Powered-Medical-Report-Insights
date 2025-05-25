import pytesseract
from src.preprocess import preprocess_image, extract_text_from_pdf
import logging, os

os.makedirs(os.path.join("logs"), exist_ok=True)  # 📂 Creates a 'logs' directory if it doesn't exist
logging.basicConfig(  # ⚙️ Configures the logging system with specified settings
    level=logging.INFO,  # 📏 Sets logging level to INFO to capture informational messages and above
    format="%(asctime)s [%(levelname)s] %(message)s",  # 📝 Defines log message format: timestamp, level, and message
    handlers=[  # 📤 Specifies where logs are sent
        logging.FileHandler(os.path.join("logs", "app.log")),  # 📜 Logs to a file named 'logging.log' in the 'logs' directory
        logging.StreamHandler()  # 🖥️ Also logs to the console (standard output)
    ]
)

def extract_text(file_path: str) -> str:
    """Extract text from image or PDF."""
    logging.info(f"Starting text extraction for file: {file_path}")
    try:
        if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            img = preprocess_image(file_path)
            if img is None:
                logging.warning("No image data after preprocessing")
                return ""
            text = pytesseract.image_to_string(img)
            logging.info("Text extracted from image")
        elif file_path.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
            logging.info("Text extracted from PDF")
        else:
            logging.error(f"Unsupported file format: {file_path}")
            raise ValueError("Unsupported file format. Use PDF, PNG, or JPEG.")
        return text
    except Exception as e:
        logging.error(f"Error in OCR for {file_path}: {str(e)}")
        raise