from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.views.article import articles_views
from app.core.config import settings

app = FastAPI()

app.mount("/public",
          StaticFiles(directory=settings.STATIC_FILES_DIR),
          name="public")

register_tortoise(
    app,
    db_url=settings.SQLITE_URL,
    modules={"models": settings.TORTOISE_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(
    articles_views,
    tags=["Articles"])
