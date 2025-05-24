from app.core.analyzer import NERAnalyzer
from app.core.crawler import BaomoiCrawler
from app.core.storage import JSONStorage
from app.core.visualizer import Visualizer
from app.utils.logger import setup_logger
from config import settings

logger = setup_logger(__name__)

def main():
    try:
        logger.info("Starting Baomoi sports scraper")
        
        # Initialize components
        crawler = BaomoiCrawler()
        analyzer = NERAnalyzer()
        storage = JSONStorage()
        visualizer = Visualizer()
        
        # Crawl articles
        logger.info(f"Scraping up to {settings.MAX_ARTICLES} sports articles")
        articles = crawler.crawl()
        
        # Analyze content
        logger.info("Analyzing article content")
        entities = analyzer.analyze_articles([article.content for article in articles])
        
        # Save results
        logger.info("Saving results")
        storage.save_articles(articles)
        storage.save_entities(entities)
        
        # Generate visualization
        visualizer.generate_entity_chart(entities)
        
        logger.info("Scraping completed successfully")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise

if __name__ == "__main__":
    main()