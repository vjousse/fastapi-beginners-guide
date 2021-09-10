from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.views.article import articles_views

# added to prevent following warning message
# RuntimeWarning: Module "app.main" has no models
from app.models.article import Article

# tortoise logging patch (https://github.com/tortoise/tortoise-orm/issues/529)
import logging
from tortoise.contrib import fastapi
fastapi.logging = logging.getLogger('uvicorn')
# end of patch

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(
    articles_views,
    tags=["Articles"])