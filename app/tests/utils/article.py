from app.models.article import Article


async def create_random_article() -> Article:

    article = await Article.create(
        title="Mon titre de test",
        content="Un peu de contenu<br />avec deux lignes"
    )

    return article
