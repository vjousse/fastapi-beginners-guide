from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="app/templates")

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

class Article(Model):

    id = fields.IntField(pk=True)

    title = fields.TextField()
    content = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.title


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request
        })


@app.get("/articles/create")
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


@app.get("/articles")
async def articles_list(request: Request):

    articles = await Article.all().order_by('created_at')

    return templates.TemplateResponse(
        "articles_list.html",
        {
            "request": request,
            "articles": articles
        })


@app.get("/api/articles")
async def api_articles_list():

    articles = await Article.all().order_by('created_at')

    return articles