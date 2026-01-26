from pathlib import Path

# This finds the absolute path to the 'tests' folder, regardless of where you run pytest from
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Define specific sub-directories
DATA_DIR = ROOT_DIR / "tests" / "data"
LOGS_DIR = ROOT_DIR / "tests" / "logs"
REPORTS_DIR = ROOT_DIR / "tests" / "allure-results"

# Specific file paths
SAMPLE_PDF = DATA_DIR / "sample.pdf"
USER_JSON = DATA_DIR / "users.json"