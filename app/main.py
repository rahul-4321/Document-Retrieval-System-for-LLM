from fastapi import FastAPI
from app.api import health, search
from app.config import settings
from app.services.scraper_service import start_scraper
from app.services.document_service import initialize_elasticsearch, close_elasticsearch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(health.router)
app.include_router(search.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing Elasticsearch...")
    await initialize_elasticsearch()
    logger.info("Starting background scraper...")
    start_scraper()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Closing Elasticsearch connection...")
    await close_elasticsearch()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)