from fastapi import APIRouter, HTTPException, Request
from app.models.article import Article
from app.core.config import templates
from app.schemas.article import (
    Article as ArticleSchema,
    ArticleCreate,
    ArticleUpdate)
from typing import List, Optional

articles_views = APIRouter()


@articles_views.post("/articles",
                     response_model=ArticleSchema)
async def articles_create(article_create: ArticleCreate):

    article = await Article.create(
        title=article_create.title,
        content=article_create.content
    )

    return article


@articles_views.put("/articles/{article_id}",
                    response_model=ArticleSchema)
async def articles_update(article_id: int,
                          article_update: ArticleUpdate):

    article: Optional[Article] = await Article.get_or_none(id=article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.title = article_update.title
    article.content = article_update.content

    await article.save()

    return article


@articles_views.get("/articles/{article_id}",
                    response_model=ArticleSchema)
async def articles_get(article_id: int):

    article: Optional[Article] = await Article.get_or_none(id=article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article


@articles_views.get("/articles", response_model=List[ArticleSchema])
async def api_articles_list(offset: int = 0, limit: Optional[int] = None):

    files_query = Article\
        .all()\
        .order_by('-created_at')\
        .offset(offset)

    if limit:
        files_query = files_query.limit(limit)

    articles = await files_query

    return articles


@articles_views.delete("/articles/{article_id}")
async def articles_delete(article_id: int):

    article: Optional[Article] = await Article.get_or_none(id=article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    await article.delete()


@articles_views.get("/", include_in_schema=False)
async def root(request: Request):

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request
        })
