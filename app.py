import streamlit as st
import os
import pathlib
import tempfile
import sys

# --- CRITICAL FIX: Add the project root to path for local imports ---
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

# 1. Import your local modules
try:
    from utils.helpers import setup_paths_and_logging, LOGS_DIR, INPUT_DIR, OUTPUT_DIR
    from utils.extraction import run_hvf_extraction
    APP_READY = True
except ImportError as e:
    st.error(f"FATAL: Local package import error. Check your 'src' folder structure. Error: {e}")
    APP_READY = False

# 2. Run Setup
if APP_READY:
    setup_paths_and_logging()

def main():
    st.set_page_config(page_title="HVF Report Data Extractor", layout="wide")
    st.title("HVF Report Data Extractor")

    # Display setup info in the sidebar
    st.sidebar.markdown(f"**Output Dir:** `{OUTPUT_DIR.resolve()}`")

    # --- Sidebar ---
    with st.sidebar:
        st.header("⚙️ Configuration")

    # --- Main File Uploader ---
    uploaded_files = st.file_uploader(
        "Upload one or more HVF Image Files",
        type=["png", "jpg", "jpeg", "dcm"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.subheader(f"Processing {len(uploaded_files)} file(s)")
        col1, col2 = st.columns(2)

        for i, uploaded_file in enumerate(uploaded_files):
            temp_path = None
            try:
                # Save uploaded file to temp path
                suffix = pathlib.Path(uploaded_file.name).suffix 
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    temp_path = tmp_file.name

                # Call the placeholder wrapper function
                results_content, success = run_hvf_extraction(temp_path, output_dir=OUTPUT_DIR)

                # Display results
                target_col = col1 if i % 2 == 0 else col2
                with target_col:
                    with st.expander(f"**Results for: {uploaded_file.name}**", expanded=True):
                        st.image(uploaded_file, caption=uploaded_file.name)
                        st.text_area("Extracted Data:", value=results_content, height=200)
                        st.info(f"Data would be saved in the **output/** folder.")

            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)
    else:
        st.info("Please upload an image file to begin extraction.")

if __name__ == "__main__":
    main()