from paddleocr import PaddleOCR
import cv2
import json
from pathlib import Path
from typing import Dict

class HVFExtractor:
    def __init__(self, template_name="hvf_24_2"):
        # PaddleOCR object
        self.ocr = PaddleOCR(lang="en", use_angle_cls=False)
        
        # Load bounding box template (normalized coordinates 0-1)
        tmpl_path = Path(__file__).parent / "templates" / f"{template_name}.json"
        if not tmpl_path.exists():
            raise FileNotFoundError(f"Template file not found: {tmpl_path}")
        with open(tmpl_path, "r") as f:
            self.bboxes = json.load(f)

    def extract(self, image_path: str) -> Dict[str, str]:
        """Extract text from each normalized bounding box, return dict {field_name: rec_text}"""
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Cannot read image at {image_path}")

        h, w = img.shape[:2]
        results: Dict[str, str] = {}

        for key, (nx1, ny1, nx2, ny2) in self.bboxes.items():
            # Convert normalized coordinates to absolute pixel coordinates
            x1 = max(0, min(int(nx1 * w), w - 1))
            x2 = max(0, min(int(nx2 * w), w))
            y1 = max(0, min(int(ny1 * h), h - 1))
            y2 = max(0, min(int(ny2 * h), h))

            if x1 >= x2 or y1 >= y2:
                print(f"Skipping {key}, invalid crop: {x1},{y1},{x2},{y2}")
                results[key] = ""
                continue

            crop = img[y1:y2, x1:x2]

            # Run PaddleOCR prediction
            ocr_result = self.ocr.predict(crop)

            # Extract recognized text
            rec_texts = []
            for block in ocr_result:
                rec_texts.extend(block.get("rec_texts", []))

            results[key] = " ".join(rec_texts) if rec_texts else ""

        return results
