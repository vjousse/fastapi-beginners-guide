from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.database import Base, engine
from app.views.article import articles_views

app = FastAPI()

app.mount("/public", StaticFiles(directory=settings.STATIC_FILES_DIR), name="public")

templates = Jinja2Templates(directory="app/templates")


Base.metadata.create_all(bind=engine)


app.include_router(articles_views, tags=["Articles"])


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
