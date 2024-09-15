# Document Retrieval System

This project implements a document retrieval system for chat applications to use as context. It provides a backend for retrieving documents, storing them in a database, and caching responses for faster retrieval.

## Architecture

The system consists of the following components:

1. FastAPI web server
2. Elasticsearch for document storage and retrieval
3. Redis for caching search results
4. PostgreSQL for user management and rate limiting
5. Background scraper for fetching news articles

## Caching Strategy

We use Redis for caching search results. Redis was chosen over Memcached for the following reasons:

1. Support for complex data structures: Redis allows us to store structured search results more efficiently.
2. Data persistence: Redis can persist data to disk, which helps maintain the cache across server restarts.
3. Distributed caching: Redis has built-in support for distributed caching scenarios, which is beneficial for scaling.

The caching strategy works as follows:

1. When a search query is received, we first check if the results are available in Redis.
2. If found, we return the cached results immediately.
3. If not found, we perform the search in Elasticsearch, cache the results in Redis with a 1-hour expiration, and then return the results.

This strategy significantly reduces the load on Elasticsearch for frequently requested searches while ensuring that the results are updated periodically.

## Rate Limiting

Rate limiting is implemented using PostgreSQL. Each user is allowed 5 requests per hour. The user's request count is stored in the database and incremented with each request. If the limit is exceeded, a 429 status code is returned.

## Setup and Running

1. Clone the repository
2. Install Docker and Docker Compose
3. Run `docker-compose up --build`
4. The API will be available at `http://localhost:8000`

## API Endpoints

- `/health`: Returns the health status of the API
- `/search`: Performs a document search
  - Parameters:
    - `text`: The search query
    - `top_k`: Number of results to return (default: 10)
    - `threshold`: Minimum similarity score (default: 0.5)
    - `user_id`: Required for rate limiting

## Future Improvements

- Implement re-ranking algorithms for search results
- Add fine-tuning scripts for retrievers
- Implement more robust error handling and logging
- Add comprehensive unit and integration tests

## License

This project is licensed under the MIT License.


## modules used

# 1. FastAPI
- FastAPI is a modern web framework for building APIs with Python. It's known for its high performance, automatic generation of OpenAPI documentation, and asynchronous support.
Purpose in the Project:
- To build the REST API endpoints (/health, /search, etc.).
Handles HTTP requests, parameter validation, and provides input/output schemas using Pydantic.
# 2. Uvicorn
- Uvicorn is an ASGI (Asynchronous Server Gateway Interface) web server implementation for Python.
Purpose in Your Project:
To serve the FastAPI application. It supports asynchronous operations, which is beneficial for handling concurrent requests efficiently, such as multiple document retrieval queries.
# 3. Elasticsearch
- Elasticsearch is a distributed, RESTful search and analytics engine. It allows for full-text search and document retrieval using powerful query mechanisms like term matching and similarity searches.
Purpose in Your Project:
To store, index, and retrieve documents based on semantic search queries. It will handle the core document retrieval functionality, allowing for fast searches across large document sets.
# 4. Redis
- Redis is an in-memory key-value store known for its speed and support for caching and message brokering.
Purpose in Your Project:
To cache frequently searched queries and their results, which speeds up response times for repeated searches.
Redis can also be used as a message broker for managing background tasks like scraping articles.
# 5. Psycopg2-binary
- This is a PostgreSQL database adapter for Python. It allows Python programs to interact with a PostgreSQL database.
Purpose in Your Project:
To interact with PostgreSQL for storing and retrieving user-related data, such as user requests and request counts for rate-limiting.
It will manage relational data like user activity logs or metadata associated with stored documents.
# 6. Newspaper3k
- Newspaper3k is a Python library for scraping and extracting articles from news websites.
Purpose in Your Project:
To scrape news articles in the background and store the extracted content in Elasticsearch for future document retrieval.
It simplifies the process of gathering news data, handling tasks like parsing, content extraction, and cleaning.
# 7. Pydantic
- Pydantic is a data validation and settings management library for Python. It uses Python type hints to validate data structures.
Purpose in Your Project:
To validate and parse the input data (such as query parameters for the /search endpoint).
Pydantic models will ensure that the incoming API requests meet the required schema and handle type coercion.
# 8. Pydantic-settings
- An extension of Pydantic, pydantic-settings allows managing environment variables and configurations with Pydantic models.
Purpose in Your Project:
To manage your application’s configuration, such as database connection strings, API keys, Redis configurations, Elasticsearch details, etc., from environment variables.
It centralizes configuration management, making it easier to configure and modify settings without hardcoding values.