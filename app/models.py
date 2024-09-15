from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    id: str
    score: float
    content: str

class SearchResponse(BaseModel):
    results: List[SearchResult]