import json
from pathlib import Path
from typing import List

from app.models.article import Article
from app.models.entities import Entity
from app.utils.logger import setup_logger
from config import settings

logger = setup_logger(__name__)

class JSONStorage:
    def __init__(self):
        settings.OUTPUT_DIR.mkdir(exist_ok=True)
        
    def save_articles(self, articles: List[Article]):
        """Save article metadata to JSON"""
        try:
            output_path = settings.OUTPUT_DIR / 'article_links.json'
            data = {
                "metadata": {
                    "source": "baomoi.com",
                    "total_articles": len(articles)
                },
                "articles": [
                    {
                        "url": article.url,
                        "title": article.title,
                        "published_at": article.published_at.isoformat()
                    }
                    for article in articles
                ]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved {len(articles)} articles to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save articles: {e}")
            raise

    def save_entities(self, entities: List[Entity]):
        """Save entity analysis to JSON"""
        try:
            output_path = settings.OUTPUT_DIR / 'entity_distribution.json'
            data = {
                "metadata": {
                    "source": "baomoi.com",
                    "total_entities": len(entities)
                },
                "entities": [
                    {
                        "text": entity.text.replace("_", " "),
                        "type": entity.type.value,
                        "count": entity.count
                    }
                    for entity in entities
                ]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved {len(entities)} entities to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save entities: {e}")
            raise