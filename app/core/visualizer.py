import matplotlib.pyplot as plt
from pathlib import Path
from typing import List

from app.models.entities import Entity
from app.utils.logger import setup_logger
from config import settings

logger = setup_logger(__name__)

class Visualizer:
    @staticmethod
    def generate_entity_chart(entities: List[Entity], top_n: int = 50):
        """Generate horizontal bar chart of top entities"""
        try:
            # Prepare data
            top_entities = sorted(entities, key=lambda x: x.count, reverse=True)[:top_n]
            labels = [e.text.replace("_", " ") for e in top_entities]
            counts = [e.count for e in top_entities]
            
            # Configure plot
            plt.style.use('ggplot')
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create horizontal bar plot
            y_pos = range(len(top_entities))
            ax.barh(y_pos, counts, color='skyblue')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels)
            ax.invert_yaxis()  # Highest count at top
            ax.set_xlabel('Mention Count', fontsize=12)
            ax.set_title(f'Top {top_n} Named Entities in Sports Articles', fontsize=14)
            
            # Save visualization
            output_path = settings.OUTPUT_DIR / 'entity_distribution.png'
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Saved visualization to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to generate visualization: {e}")
            raise