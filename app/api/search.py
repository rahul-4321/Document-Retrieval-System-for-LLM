from fastapi import APIRouter, HTTPException, Depends
from app.services.document_service import search_documents
from app.services.user_service import check_rate_limit
from app.models import SearchResponse
from functools import wraps
import time
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function {func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@router.get("/search", response_model=SearchResponse)
@measure_time
async def search(text: str, top_k: int = 10, threshold: float = 0.5, user_id: str = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    if not check_rate_limit(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    results = await search_documents(text, top_k, threshold)
    return SearchResponse(results=results)