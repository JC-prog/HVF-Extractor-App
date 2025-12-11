from ophtho_ocr.hvf.extractor import HVFExtractor

def test_hvf_import():
    extractor = HVFExtractor()
    assert extractor is not None
