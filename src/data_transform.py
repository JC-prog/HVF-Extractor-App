# src/data_transform.py
import pandas as pd
import io
from src.ocr_engine import run_paddle_ocr

def transform_ocr_to_csv(ocr_data: list[dict]) -> str:
    """Converts structured OCR data into a CSV string based on business rules."""
    
    # 1. Apply your custom logic here (e.g., extracting key-value pairs from bounding boxes)
    # For this example, we'll just put the text and confidence into a DataFrame
    
    if not ocr_data:
        return ""
        
    df = pd.DataFrame(ocr_data)
    
    # Simple example of transforming columns
    final_df = df[['text', 'confidence']].rename(columns={'text': 'Extracted Text', 'confidence': 'Confidence Score'})
    
    # Write DataFrame to a CSV string in memory
    csv_buffer = io.StringIO()
    final_df.to_csv(csv_buffer, index=False)
    
    return csv_buffer.getvalue()

# A simple wrapper to combine the two library steps
def process_image_to_csv(image_bytes: bytes) -> str:
    """End-to-end function for external callers."""
    # 1. Core Logic
    structured_data = run_paddle_ocr(image_bytes)
    # 2. Transformation
    csv_string = transform_ocr_to_csv(structured_data)
    return csv_string