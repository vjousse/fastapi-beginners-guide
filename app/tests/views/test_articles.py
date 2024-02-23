from fastapi.testclient import TestClient

from app.models.article import Article
from app.tests.conftest import TestingSessionLocal


def test_create_article(client: TestClient, session: TestingSessionLocal) -> None:
    article = Article(
        title="Mon titre de test", content="Un peu de contenu<br />avec deux lignes"
    )

    session.add(article)
    session.commit()

    response = client.get("articles")
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    first_article = content[0]
    assert first_article["title"] == article.title
    assert first_article["content"] == article.content
