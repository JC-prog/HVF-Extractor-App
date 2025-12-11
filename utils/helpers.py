import pathlib, os, logging

BASE_DIR = pathlib.Path(os.getcwd())
LOGS_DIR = BASE_DIR / "logs"
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LAYOUT_DIR = BASE_DIR / "layout"

def setup_paths_and_logging():
    LOGS_DIR.mkdir(exist_ok=True)
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    LAYOUT_DIR.mkdir(exist_ok=True)
    # Setup basic logging here for later

# Define logger globally so other modules can use it
logger = logging.getLogger(__name__)