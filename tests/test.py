import os
from PIL import Image
from ophtho_ocr.hvf.extractor import HVFExtractor
from ophtho_ocr.export.xlsx import XLSXExporter
from ophtho_ocr.preprocessing.pdf_converter import PDFConverter

file_name = "VRVF_OD.jpg"
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, "../samples", file_name)

# pdf_converter = PDFConverter()
# img_paths = pdf_converter.convert(img_path)   # <-- returns list

# Use the first page
# converted_path = img_paths[0]

# Crop box
x = 1104
y = 985
width = 178
height = 160

# Load image
print(img_path)
img = Image.open(img_path)

# Crop
cropped = img.crop((x, y, x + width, y + height))

# Save cropped file
output_path = os.path.join(script_dir, "cropped_region.png")
cropped.save(output_path)
print("Saved cropped image to:", output_path)

# OCR extract
extractor = HVFExtractor()
data = extractor.full_extract(output_path)
print(data)
