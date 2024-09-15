import pytest
from unittest.mock import patch, MagicMock
from app.services.document_service import search_documents, index_document

@pytest.mark.asyncio
@patch('app.services.document_service.redis_client')
@patch('app.services.document_service.es')
async def test_search_documents_cache_hit(mock_es, mock_redis):
    mock_redis.get.return_value = b'[{"id": "1", "score": 0.9, "content": "Cached content"}]'

    result = await search_documents("test", 10, 0.5)

    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["content"] == "Cached content"
    mock_es.search.assert_not_called()

@pytest.mark.asyncio
@patch('app.services.document_service.redis_client')
@patch('app.services.document_service.es')
async def test_search_documents_cache_miss(mock_es, mock_redis):
    mock_redis.get.return_value = None
    mock_es.search.return_value = {
        "hits": {
            "hits": [
                {"_id": "1", "_score": 0.9, "_source": {"content": "ES content"}}
            ]
        }
    }

    result = await search_documents("test", 10, 0.5)

    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["content"] == "ES content"
    mock_es.search.assert_called_once()
    mock_redis.setex.assert_called_once()

@pytest.mark.asyncio
@patch('app.services.document_service.es')
async def test_index_document(mock_es):
    await index_document("Test Title", "Test Content")

    mock_es.index.assert_called_once_with(
        index="documents",
        body={
            "title": "Test Title",
            "content": "Test Content"
        }
    )