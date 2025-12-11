# src/ocr_engine.py
import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR # Assume this is installed in the library environment
from .exceptions import OcrFailedError
from .logger_config import get_logger
import io
import numpy as np

logger = get_logger(__name__)

# Initialize model only once
@st.cache_resource # If running in Streamlit, you can cache it there, or just initialize globally
def get_ocr_instance():
    # Model initialization logic
    return PaddleOCR(use_angle_cls=True, lang="en") 

def run_paddle_ocr(image_bytes: bytes, language: str = 'en') -> list[dict]:
    """Runs OCR on image bytes and returns structured result."""
    logger.info(f"Starting OCR processing with language: {language}")
    
    try:
        # Load image from bytes (PIL standard)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        ocr = get_ocr_instance() # Get the pre-initialized model
        
        # Run the model (returns list of blocks/dictionaries)
        result = ocr.ocr(np.array(image)) 
        
        # We process the raw output for easier downstream transformation
        # processed_result = [{"box": item[0], "text": item[1][0], "confidence": item[1][1]} for line in result for item in line]
        
        print(result)
        return "Sucess"

    except Exception as e:
        logger.exception("PaddleOCR processing failed.")
        raise OcrFailedError(f"OCR engine failed: {e}")