from elasticsearch import AsyncElasticsearch
from app.config import settings
import redis
import json
import logging
import hashlib

logger = logging.getLogger(__name__)

es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
redis_client = redis.Redis.from_url(settings.REDIS_URL)

async def search_documents(text: str, top_k: int, threshold: float):
    cache_key = f"search:{text}:{top_k}:{threshold}"
    cached_result = redis_client.get(cache_key)
    
    if cached_result:
        logger.info(f"Cache hit for query: {text}")
        return json.loads(cached_result)
    
    logger.info(f"Cache miss for query: {text}, searching in Elasticsearch")
    results = await es.search(index="documents", body={
        "query": {
            "match": {
                "content": text
            }
        },
        "size": top_k,
        "min_score": threshold
    })
    
    formatted_results = [
        {
            "id": hit["_id"],
            "score": hit["_score"],
            "content": hit["_source"]["content"]
        } 
        for hit in results["hits"]["hits"]
    ]
    
    redis_client.setex(cache_key, 3600, json.dumps(formatted_results))  # Cache for 1 hour
    logger.info(f"Cached search results for query: {text}")
    
    return formatted_results

async def index_document(title: str, content: str, url:str):

    article_hash=hashlib.md5((title+url).encode()).hexdigest()

    #check if the article already exists
    exists = await es.exists(index="document", id=article_hash)

    if exists:
        logger.info(f"Article already indexed: {title}")
        return None

    try:
        response = await es.index(index="documents",id=article_hash, body={
            "title": title,
            "content": content,
            "url":url
        })
        logger.info(f"Indexed new article: {title}")
        return response['_id']
    except Exception as e:
        logger.error(f"Error indexing document: {str(e)}")
        raise

async def article_exists(url:str):
    try:
        result=await es.search(index="document",body={
            "query":{
                "term":{
                    "url.keyword":url
                }
            }
        })
        return len(result['hits']['hits]'])>0
    
    except Exception as e:
        logger.error(f"Error checking article existance: {str(e)}")
        return False

async def initialize_elasticsearch():
    try:
        if not await es.indices.exists(index="documents"):
            await es.indices.create(index="documents", body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "content": {"type": "text"}
                    }
                }
            })
            logger.info("Created 'documents' index in Elasticsearch")
        else:
            logger.info("'documents' index already exists in Elasticsearch")
    except Exception as e:
        logger.error(f"Error initializing Elasticsearch: {str(e)}")
        raise

async def close_elasticsearch():
    await es.close()