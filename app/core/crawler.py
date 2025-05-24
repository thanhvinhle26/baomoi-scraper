import random
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.models.article import Article
from app.utils.exceptions import CrawlerError
from app.utils.logger import setup_logger
from config import settings
from typing import Optional

logger = setup_logger(__name__)

class BaomoiCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(settings.HEADERS)
        self.exceed_day_flag = True

    def _parse_article_content(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            time_tag = soup.find('time')
            article_time = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if datetime.now(article_time.tzinfo) - article_time > timedelta(days=settings.DAYS_BACK):
                self.exceed_day_flag = False
                return None
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else ""
            body = soup.find('div', class_='content-body')
            body_text = body.get_text(strip=False) if body else ""
            

            return title_text, body_text, article_time
        except Exception as e:
            logger.error(f"Error parsing article content: {e}")
            raise CrawlerError(f"Failed parse article content {url}")

    def _parse_article(self, article_div) -> Optional[Article]:
        try:   
            link_tag = article_div.find('div', class_='bm-card-header')
            if not link_tag:
                return None
                
            link_tag = link_tag.find('a')
            if link_tag and 'href' in link_tag.attrs:
                url = urljoin(settings.BASE_URL, link_tag['href'])
                title, content, article_time = self._parse_article_content(url)
                
                return Article(
                    url=url,
                    title=title,
                    content=content,
                    published_at=article_time
                )
        except Exception as e:
            logger.error(f"Error parsing article: {e}")
            raise CrawlerError(f"Failed to crawl article {article_div}")

    def crawl_page(self, page_num: int) -> list[Article]:
        try:
            url = f"{settings.SPORT_CATEGORY_URL}/trang{page_num}.epi"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return [
                article for article_div in soup.find_all('div', class_='bm-card-content')
                if (article := self._parse_article(article_div))
            ]
        except Exception as e:
            logger.error(f"Error crawling page {page_num}: {e}")
            raise CrawlerError(f"Failed to crawl page {page_num}")

    def crawl(self, max_articles: int = settings.MAX_ARTICLES) -> list[Article]:
        articles = []
        current_page = 1
        
        while len(articles) < max_articles and self.exceed_day_flag:
            try:
                new_articles = self.crawl_page(current_page)
                if not new_articles:
                    break
                    
                articles.extend(new_articles)
                logger.info(f"Page {current_page}: Found {len(new_articles)} articles")
                
                current_page += 1
                time.sleep(random.uniform(1, 3))
                
            except CrawlerError:
                time.sleep(5)
                continue
                
        return articles[:max_articles]