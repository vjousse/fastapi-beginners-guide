import asyncio
from fastapi.testclient import TestClient

from app.tests.utils.article import create_random_article


def test_read_item(client: TestClient,
                   event_loop: asyncio.AbstractEventLoop) -> None:

    article = event_loop.run_until_complete(create_random_article())

    response = client.get("api/articles")
    assert response.status_code == 200
    content = response.json()
    first_article = content[0]
    assert first_article["title"] == article.title
    assert first_article["content"] == article.content
