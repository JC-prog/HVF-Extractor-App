import os
from ophtho_ocr.hvf.extractor import HVFExtractor
from ophtho_ocr.export.xlsx import XLSXExporter

# Make path relative to THIS script, not the current working directory
file_name = "hvf_od.png"
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, "../samples", file_name)

print("Absolute path:", img_path)
print("Exists:", os.path.exists(img_path))

# Ensure the image exists before extracting
if not os.path.exists(img_path):
    raise FileNotFoundError(f"Cannot find image at {img_path}")

extractor = HVFExtractor()
data = extractor.extract(img_path)

XLSXExporter().save(data, "left_result.xlsx")
print("Exported to left_result.xlsx")
