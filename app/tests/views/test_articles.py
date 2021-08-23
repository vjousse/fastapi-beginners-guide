from fastapi.testclient import TestClient
from app.models.article import Article


def test_read_item(client: TestClient,
                   random_article: Article) -> None:

    response = client.get("api/articles")
    assert response.status_code == 200
    content = response.json()
    first_article = content[0]
    assert first_article["title"] == random_article.title
    assert first_article["content"] == random_article.content
