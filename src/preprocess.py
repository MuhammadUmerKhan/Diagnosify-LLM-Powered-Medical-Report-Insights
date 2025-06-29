# import cv2
import numpy as np
import PyPDF2
from src.logger import get_logger

logger = get_logger(__name__)

# def preprocess_image(image_path: str) -> np.ndarray:
#     """Preprocess image for OCR: convert to grayscale, denoise, and binarize."""
#     logger.info(f"Preprocessing image: {image_path}")
#     try:
#         img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             logger.error(f"Failed to load image: {image_path}")
#             raise ValueError("Invalid image file")
#         # Denoising
#         img = cv2.fastNlMeansDenoising(img)
#         # Adaptive thresholding
#         img = cv2.adaptiveThreshold(
#             img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
#         )
#         logger.info("Image preprocessing completed")
#         return img
#     except Exception as e:
#         logger.error(f"Error preprocessing image {image_path}: {str(e)}")
#         raise

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyPDF2."""
    logger.info(f"Extracting text from PDF: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            logger.info("PDF text extraction completed")
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        raise