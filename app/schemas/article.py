from datetime import datetime

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str


class Article(ArticleBase):
    id: int
    updated_at: datetime
    created_at: datetime


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass
