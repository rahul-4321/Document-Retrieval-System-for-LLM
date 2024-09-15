from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Retrieval System"
    PROJECT_VERSION: str = "1.0.0"
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    REDIS_URL: str = "redis://redis:6379"
    POSTGRES_URL: str = "postgresql://postgres:password@postgres/userdb"
    RATE_LIMIT: int = 5
    SCRAPER_INTERVAL: int = 3600  # 1 hour

settings = Settings()