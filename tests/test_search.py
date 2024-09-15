from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@patch('app.services.document_service.search_documents')
@patch('app.services.user_service.check_rate_limit')
def test_search_endpoint(mock_check_rate_limit, mock_search_documents):
    mock_check_rate_limit.return_value = True
    mock_search_documents.return_value = [
        {"id": "1", "score": 0.9, "content": "Test content 1"},
        {"id": "2", "score": 0.8, "content": "Test content 2"},
    ]

    response = client.get("/search?text=test&user_id=123")
    assert response.status_code == 200
    assert len(response.json()["results"]) == 2
    assert response.json()["results"][0]["id"] == "1"
    assert response.json()["results"][1]["id"] == "2"

@patch('app.services.user_service.check_rate_limit')
def test_search_rate_limit_exceeded(mock_check_rate_limit):
    mock_check_rate_limit.return_value = False

    response = client.get("/search?text=test&user_id=123")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["detail"]

def test_search_missing_user_id():
    response = client.get("/search?text=test")
    assert response.status_code == 400
    assert "User ID is required" in response.json()["detail"]