# app.py
import streamlit as st
import io

from src.ocr_engine import run_paddle_ocr
from src.data_transform import process_image_to_csv
from src.exceptions import OcrFailedError

st.set_page_config(page_title="OCR to CSV", layout="centered")
st.title("OCR to CSV Converter")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Image File", 
    type=['png', 'jpg', 'jpeg'], 
    help="Try uploading a standard JPEG or PNG document image."
)

if uploaded_file is not None:
    # Display image preview
    st.image(uploaded_file, caption=uploaded_file.name)
    
    # 1. I/O HANDLING (Streamlit's job)
    # Read the file buffer into raw bytes
    image_bytes = uploaded_file.read()
    
    if st.button("Run OCR and Convert to CSV 🚀", use_container_width=True):
        st.info("Processing started... Check your terminal for library logs!")
        
        # 2. LIBRARY CALL (Bridge)
        try:
            # Call the single wrapper function from the external library
            csv_output = process_image_to_csv(image_bytes)
            
            # 3. OUTPUT DISPLAY & ERROR HANDLING
            if csv_output:
                st.success("Conversion successful!")
                
                # Use st.download_button
                st.download_button(
                    label="Download CSV",
                    data=csv_output,
                    file_name="ocr_output.csv",
                    mime="text/csv"
                )
                
                st.subheader("CSV Preview")
                st.code(csv_output, language='csv')

            else:
                st.warning("OCR ran successfully but the mock result was empty. Try a larger file.")
        
        # --- 4. EXCEPTION HANDLING (Catches errors from the library) ---
        except OcrFailedError as e:
            # Handle the specific, known error from the OCR engine
            st.error(f"OCR Engine Failed: {e}")
            st.caption("The core OCR process encountered a problem. Check the terminal logs for details.")
        
        except Exception as e:
            # Catch all other unexpected errors
            st.exception(f"An unexpected error occurred during processing: {e}")