from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.article import Article
from app.schemas.article import Article as ArticleSchema
from app.schemas.article import ArticleCreate, ArticleUpdate

articles_views = APIRouter()


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@articles_views.post("/articles", response_model=ArticleSchema)
async def api_articles_create(
    article_create: ArticleCreate, db: Session = Depends(get_db)
):
    article = Article(title=article_create.title, content=article_create.content)

    db.add(article)
    db.commit()
    db.refresh(article)

    return article


@articles_views.get("/articles", response_model=List[ArticleSchema])
async def api_articles_list(
    offset: int = 0,
    limit: int | None = None,
    sort_order: SortOrder = SortOrder.asc,
    db: Session = Depends(get_db),
):
    articles_statement = (
        select(Article)
        .order_by(
            Article.created_at.desc()
            if sort_order == SortOrder.desc
            else Article.created_at
        )
        .offset(offset)
    )

    if limit:
        articles_statement = articles_statement.limit(limit)

    return db.scalars(articles_statement).all()


@articles_views.get("/articles/{article_id}", response_model=ArticleSchema)
async def articles_get(article_id: int, db: Session = Depends(get_db)):
    article: Article | None = db.get(Article, article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article


@articles_views.put("/articles/{article_id}", response_model=ArticleSchema)
async def articles_update(
    article_id: int, article_update: ArticleUpdate, db: Session = Depends(get_db)
):
    article: Article | None = db.get(Article, article_id)

    # Pour information, le code ci-dessus est équivalent à ce code-ci
    # article: Article | None = (
    #    db.execute(select(Article).filter_by(id=article_id)).scalars().one_or_none()
    # )

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.title = article_update.title
    article.content = article_update.content

    db.commit()

    return article


@articles_views.delete("/articles/{article_id}")
async def articles_delete(article_id: int, db: Session = Depends(get_db)):
    article: Article | None = db.get(Article, article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    db.delete(article)
    db.commit()
