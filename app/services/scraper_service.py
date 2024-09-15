import asyncio
import newspaper
from app.services.document_service import index_document
from app.services.document_service import article_exists
from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def scrape_articles():

    news_sources=["https://www.bbc.com/news","https://www.nytimes.com/"]
    while True:
        for source in news_sources:
            try:
                paper=newspaper.build(source,memoize_articles=False)
                for article_url in paper.article_urls():
                    
                    #check if article already exista
                    if await article_exists(article_url):
                        logger.info(f"Article already exists: {article_url}")
                        continue
                    
                    article=newspaper.Article(article_url)
                    await article.download()
                    await article.parse()

                    await index_document(article.title,article.txt)

                    logger.info(f"Indexed article: {article.title} from {source}")

            except Exception as e:
                logger.error(f"Error scraping {source}: {str(e)}")
        
        await asyncio.sleep(settings.SCRAPER_INTERVAL)

def start_scraper():
    asyncio.create_task(scrape_articles())