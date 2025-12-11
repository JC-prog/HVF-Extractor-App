# ocr_library/src/logger_config.py
import logging
import os

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%H:%M:%S'

def get_logger(name: str) -> logging.Logger:
    """Configures and returns a standard logger instance."""
    
    log_level = os.environ.get('LIBRARY_LOG_LEVEL', 'INFO').upper()
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger