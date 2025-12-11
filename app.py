# app.py (SIMPLIFIED)

# System Imports
import os
import sys
import pathlib
# ... (rest of system imports, remove tempfile, st_canvas, PIL, numpy imports) ...

# Streamlit
import streamlit as st

try:
    from utils.helpers import setup_paths_and_logging, OUTPUT_DIR
    from views.single_extraction_view import single_extraction_view
    from views.layout_editor_view import layout_editor_view
    APP_READY = True
except ImportError as e:
    st.error(f"FATAL: Could not import utility or page modules. Check paths. Error: {e}")
    APP_READY = False

# 2. Run Setup
if APP_READY:
    setup_paths_and_logging()

def main():
    st.set_page_config(page_title="HVF Report Data Extractor", layout="wide")
    
    # --- Sidebar Navigation ---
    with st.sidebar:
        st.header("Views")
        
        # 1. Navigation Selector
        view_selection = st.radio(
            "Select View",
            options=["Extraction", "Layout Editor"],
            index=0,
            captions=["Run OCR on uploaded files.", "Interactively define coordinates."]
        )
        
        st.markdown("---")
        # Display setup info in the sidebar
        st.markdown(f"**Output Dir:** `{OUTPUT_DIR.resolve()}`")

    
    # --- View Content Switching ---
    if view_selection == "Extraction":
        single_extraction_view() 

    elif view_selection == "Layout Editor":
        layout_editor_view() 


if __name__ == "__main__":
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())
        
    if APP_READY:
        main()