from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.models.article import Article

articles_views = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@articles_views.get("/articles/create", include_in_schema=False)
async def articles_create(request: Request):

    article = await Article.create(
        title="Mon titre de test",
        content="Un peu de contenu<br />avec deux lignes"
    )

    return templates.TemplateResponse(
        "articles_create.html",
        {
            "request": request,
            "article": article
        })


@articles_views.get("/articles", include_in_schema=False)
async def articles_list(request: Request):

    articles = await Article.all().order_by('created_at')

    return templates.TemplateResponse(
        "articles_list.html",
        {
            "request": request,
            "articles": articles
        })


@articles_views.get("/api/articles")
async def api_articles_list():

    articles = await Article.all().order_by('created_at')

    return articles


@articles_views.get("/", include_in_schema=False)
async def root(request: Request):

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request
        })
