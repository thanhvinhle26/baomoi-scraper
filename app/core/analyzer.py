from collections import Counter
from typing import List

import py_vncorenlp

from app.models.entities import Entity, EntityType
from app.utils.logger import setup_logger
from config import settings
from app.utils.exceptions import AnalysisError

logger = setup_logger(__name__)

class NERAnalyzer:
    def __init__(self):
        try:
            self.model = py_vncorenlp.VnCoreNLP(save_dir=str(settings.VNCORENLP_DIR))
        except Exception as e:
            logger.error(f"Failed to load VnCoreNLP: {e}")
            raise

    def extract_entities(self, text: str) -> List[Entity]:
        try:
            annotations = self.model.annotate_text(text)
            entities = []
            
            for idx in range(len(annotations)):
                for word in annotations[idx]:
                    if 'nerLabel' in word and word['nerLabel'] in ['B-PER', 'B-LOC']:
                        entity_type = EntityType.PERSON if word['nerLabel'] == 'B-PER' else EntityType.LOCATION
                        entities.append(Entity(
                            text=word['wordForm'],
                            type=entity_type
                        ))
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            raise AnalysisError(f"Error extracting entities {text}")

    def analyze_articles(self, articles: List[str]) -> List[Entity]:
        entity_counter = Counter()
        for article in articles:
            entities = self.extract_entities(article)
            for entity in entities:
                entity_counter[(entity.text, entity.type)] += 1
                
        return [
            Entity(text=text, type=type, count=count)
            for (text, type), count in entity_counter.most_common(50)
        ]