# layout_editor.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# --- Placeholder for vf-extractor's conversion logic ---
# You MUST replace this with the real function from your vf-extractor package
# This function should be imported from vfextractor.utils.coordinates
def convert_normalized_to_pixel(image_pil, normalized_box):
    W, H = image_pil.size
    nl, nt, nr, nb = normalized_box
    
    left = int(nl * W)
    top = int(nt * H)
    right = int(nr * W)
    bottom = int(nb * H)
    return (left, top, right, bottom)
# --------------------------------------------------------


def layout_editor_view():
    st.header("📐 Layout Editor (Coordinate Finder)")
    st.markdown(
        "Upload an image and draw rectangles over the regions of interest. "
        "The coordinates will be generated below as normalized floats (0.0 to 1.0)."
    )
    
    uploaded_file = st.file_uploader("Upload Image for Layout Analysis", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image_pil = Image.open(uploaded_file).convert("RGB")
        original_width, original_height = image_pil.size
        
        MAX_CANVAS_WIDTH = 1000  
        MAX_CANVAS_HEIGHT = 800  
        
        width_ratio = MAX_CANVAS_WIDTH / original_width
        dynamic_height = original_height * width_ratio
        dynamic_width = MAX_CANVAS_WIDTH

        if dynamic_height > MAX_CANVAS_HEIGHT:
            height_ratio = MAX_CANVAS_HEIGHT / original_height
            dynamic_width = original_width * height_ratio
            dynamic_height = MAX_CANVAS_HEIGHT

        display_width = int(dynamic_width)
        display_height = int(dynamic_height)
        
        st.subheader("Interactive Drawing Canvas")
        st.info(f"Displaying image at {display_width}x{display_height} (Original: {original_width}x{original_height})")

        # --- Canvas Component ---
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            stroke_color="#ff0000",
            background_image=image_pil,
            height=display_height,
            width=display_width,   
            drawing_mode="rect",
            key="layout_canvas",
        )

        # --- Results Processing ---
        if canvas_result.json_data is not None and canvas_result.json_data['objects']:
            raw_boxes = [obj for obj in canvas_result.json_data['objects'] if obj['type'] == 'rect']
            
            # You can remove these debug prints once you're confident it works
            print("Canvas Result: ")
            print(canvas_result)
            
            if raw_boxes:
                st.subheader("Normalized Coordinates (0.0 to 1.0)")
                
                # CRITICAL FIX: Get the actual dimensions the canvas was rendered at
                # These attributes are directly on the canvas_result object.
                display_width = display_width
                display_height = display_height
                
                normalized_boxes = []
                
                for i, box in enumerate(raw_boxes):
                    # 1. Get raw pixel values from the display
                    # 'left', 'top', 'width', 'height' are pixel values relative to the displayed canvas
                    x1 = box['left']
                    y1 = box['top']
                    
                    # Calculate right (x2) and bottom (y2) boundary
                    x2 = x1 + box['width']
                    y2 = y1 + box['height']
                    
                    # 2. Normalize the coordinates (Divide by display dimensions)
                    normalized_box = (
                        x1 / display_width,
                        y1 / display_height,
                        x2 / display_width,
                        y2 / display_height
                    )
                    normalized_boxes.append(normalized_box)
                    
                    # Optional: Convert back to original pixels to show user the scale
                    # (Assuming image_pil is available from the file uploader context)
                    original_pixels = convert_normalized_to_pixel(image_pil, normalized_box)

                    with st.expander(f"Box {i+1} Coordinates", expanded=True):
                        st.code(f"Normalized: {normalized_box}")
                        st.markdown(f"**Original Image Size:** {image_pil.size}")
                        st.markdown(f"**Absolute Pixels:** `{original_pixels}`")

                # Display the complete list of coordinates for copy/paste
                st.markdown("### 📋 Copy/Paste List")
                st.code(str(normalized_boxes).replace('), (', '),\n ('))