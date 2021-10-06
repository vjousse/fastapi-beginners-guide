from fastapi.testclient import TestClient
import asyncio

from app.models.article import Article


async def create_article():
    article = await Article.create(
        title="Mon titre de test",
        content="Un peu de contenu<br />avec deux lignes"
    )

    return article


def test_create_article(client: TestClient,
                        event_loop: asyncio.AbstractEventLoop) -> None:

    article = event_loop.run_until_complete(create_article())

    response = client.get("articles")
    assert response.status_code == 200
    content = response.json()
    first_article = content[0]
    assert first_article["title"] == article.title
    assert first_article["content"] == article.content
