import pytesseract
from src.preprocess import extract_text_from_pdf
from src.logger import get_logger

logger = get_logger(__name__)

def extract_text(file_path: str) -> str:
    """Extract text from image or PDF."""
    logger.info(f"Starting text extraction for file: {file_path}")
    try:
        # if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        #     img = preprocess_image(file_path)
        #     if img is None:
        #         logger.warning("No image data after preprocessing")
        #         return ""
        #     text = pytesseract.image_to_string(img)
        #     logger.info("Text extracted from image")
        if file_path.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
            logger.info("Text extracted from PDF")
        else:
            logger.error(f"Unsupported file format: {file_path}")
            raise ValueError("Unsupported file format. Use PDF, PNG, or JPEG.")
        return text
    except Exception as e:
        logger.error(f"Error in OCR for {file_path}: {str(e)}")
        raise