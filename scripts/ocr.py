import PyPDF2
from scripts.config import get_logger

logger = get_logger(__name__)

def extract_text(file_path: str) -> str:
    """Extract text from a PDF file."""
    logger.info(f"♻ Extracting text from: {file_path}")
    if not file_path.lower().endswith(".pdf"):
        logger.error(f"❌ Unsupported file format: {file_path}")
        raise ValueError("Only PDF files are supported.")
    
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            logger.info("✅ PDF text extraction completed")
            return text.strip()
    except Exception as e:
        logger.error(f"❌ Error extracting text from {file_path}: {str(e)}")
        raise