import os
from paddleocr import PaddleOCR  

ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False,
    use_textline_orientation=False, 
)

def run_extraction(image_path, output_dir=None):
    placeholder_content = f"--- Placeholder Data ---\nFile: {os.path.basename(image_path)}"

    result = ocr.predict(image_path)  
    for res in result:  
        res.print()  
        res.save_to_img("output")  
        res.save_to_json("output")

    NORMALIZED_BOX_1 = (0.0011627906976744186, 0.045, 0.9918604651162791, 0.2275) 
    image_np_loaded = load_image(image_path)
    image_pil = Image.fromarray(image_np_loaded)


    result2 = ocr.ocr(cropped_img):
    

    return placeholder_content, True


    



