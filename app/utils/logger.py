import logging
import sys
from pathlib import Path

from config import settings

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(settings.OUTPUT_DIR / 'scraper.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger