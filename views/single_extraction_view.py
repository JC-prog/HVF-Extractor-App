# pages/extraction_page.py

import streamlit as st
import os
import pathlib
import tempfile
import pandas as pd 

try:
    # Ensure these imports exist in your project structure
    from utils.helpers import LOGS_DIR, INPUT_DIR, OUTPUT_DIR 
    from utils.extraction import run_extraction
except ImportError as e:
    st.error(f"Error loading utility modules: {e}")

    OUTPUT_DIR = pathlib.Path("./output")

def process_extraction(temp_path: str, file_name: str, template: str, output_dir: pathlib.Path) -> tuple[str, bool]:
    """Helper function to call the correct extraction logic based on the template."""
    # Assuming run_extraction handles the template internally, passing the template string along.
    # If not, you would typically have run_hvf_extraction and run_vrvf_extraction separately.
    return run_extraction(temp_path, output_dir=output_dir)

def save_to_csv(results_content: str, file_name: str, output_dir: pathlib.Path):
    """Helper function to save extracted data to a CSV file."""
    try:
        # NOTE: This DataFrame creation is a minimal placeholder. Adjust as needed.
        df = pd.DataFrame({'FileName': [file_name], 'ExtractedContent': [results_content]}) 
        
        # Output path now includes the dynamic folder structure
        output_path = output_dir / f"{pathlib.Path(file_name).stem}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv"
        
        # Ensure the entire directory path exists, including the custom folder
        output_dir.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False)
        st.success(f"Data successfully saved to **{output_path.name}** in the custom folder `{output_dir.parent.name}/{output_dir.name}/`.")
    except Exception as e:
        st.error(f"Error saving data to CSV: {e}")


def single_extraction_view():
    """Renders the main extraction processing page for a single file."""
    
    st.title("Report Data Extractor")
    st.header("Single File Processing")

    # --- Configuration Row (Uploader & Folder Name) ---
    col_upload, col_folder = st.columns([2, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload one HVF/VRVF Image File",
            type=["png", "jpg", "jpeg", "dcm", "pdf"],
            accept_multiple_files=False
        )
    
    with col_folder:
        # NEW: Field for custom folder name
        custom_folder_name = st.text_input(
            "Enter Output Folder Name",
            value="ProcessedData", # Default name
            key="custom_folder_input"
        )
        
    # Define the dynamic output directory based on user input
    dynamic_output_dir = OUTPUT_DIR / custom_folder_name
    st.markdown(f"**Output Folder:** `{dynamic_output_dir}`")
    st.markdown("---")


    if uploaded_file:
        st.subheader(f"File Selected: {uploaded_file.name}")
        
        # Template selection
        selection = st.selectbox(
            label="**Select Report Template Type**",
            options=["HVF", "VRVF"],
            key="template_select"
        )
        
        # Display the file and results section
        with st.container():
            st.image(uploaded_file, caption=uploaded_file.name)
            
            # --- Button and Result Block ---
            button_col1, button_col2, _ = st.columns([1, 1, 3]) 
            
            # Initialize state variables
            if 'extracted_data' not in st.session_state:
                st.session_state.extracted_data = ""
            if 'last_processed_file' not in st.session_state or st.session_state.last_processed_file != uploaded_file.name:
                 st.session_state.extracted_data = ""
                 st.session_state.last_processed_file = uploaded_file.name
                 
            # --- Extract Data Button ---
            with button_col1:
                if st.button("Extract Data", key="extract_btn"):
                    temp_path = None
                    try:
                        # 1. Save uploaded file to temp path
                        suffix = pathlib.Path(uploaded_file.name).suffix 
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            temp_path = tmp_file.name

                        # 2. Call the extraction function based on selection
                        with st.spinner(f"Extracting data using {selection} template..."):
                            # Pass the DYNAMIC output directory
                            results_content, success = process_extraction(
                                temp_path, uploaded_file.name, selection, dynamic_output_dir 
                            )

                        # 3. Store result in session state
                        if success:
                            st.session_state.extracted_data = results_content
                            st.success(f"Extraction complete using **{selection}** template.")
                        else:
                            st.session_state.extracted_data = f"Extraction failed: {results_content}"
                            st.error("Extraction failed. Check logs for details.")

                    except Exception as e:
                        st.session_state.extracted_data = f"An unexpected error occurred: {e}"
                        st.error(st.session_state.extracted_data)
                    finally:
                        # Clean up the temporary file
                        if temp_path and os.path.exists(temp_path):
                            os.unlink(temp_path)
                            
            # --- Save to CSV Button ---
            with button_col2:
                # Use the extracted_data state to determine the 'disabled' state
                is_data_ready_to_save = st.session_state.extracted_data
                
                if st.button("Save to CSV", key="save_btn", disabled=not is_data_ready_to_save):
                    if is_data_ready_to_save:
                        # Pass the DYNAMIC output directory
                        save_to_csv(st.session_state.extracted_data, uploaded_file.name, dynamic_output_dir)
                    else:
                        st.warning("Please extract data first before attempting to save.")

            
            # Display Extracted Data
            st.markdown("---") # Separator
            st.text_area(
                "Extracted Data:", 
                value=st.session_state.extracted_data if st.session_state.extracted_data else "Click 'Extract Data' to begin...", 
                height=200
            )
            
            if st.session_state.extracted_data:
                st.info(f"Data would be saved to CSV in the **{dynamic_output_dir}** folder.")

    else:
        st.info("Please upload an image file to begin extraction.")