from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
BASE_URL = "https://baomoi.com"
SPORT_CATEGORY_URL = f"{BASE_URL}/bong-da-viet-nam"
OUTPUT_DIR = BASE_DIR / "output"
VNCORENLP_DIR = BASE_DIR / "vncorenlp"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

MAX_ARTICLES = 200
DAYS_BACK = 4