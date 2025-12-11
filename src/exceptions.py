# ocr_library/src/exceptions.py

class CustomLibraryError(Exception):
    """Base exception for the OCR library."""
    pass

class OcrFailedError(CustomLibraryError):
    """Raised when the underlying OCR engine fails."""
    pass