from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    url: str
    title: str
    content: str
    published_at: datetime