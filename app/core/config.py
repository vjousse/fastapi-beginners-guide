from pydantic import BaseSettings
import os
from fastapi.templating import Jinja2Templates

dir_path = os.path.dirname(os.path.realpath(__file__))


class Settings(BaseSettings):
    APP_NAME: str = "fastapi-tutorial"
    APP_VERSION: str = "0.0.1"
    SQLITE_URL: str = "sqlite://db.sqlite3"

    TORTOISE_MODELS = [
        "app.models.article"
    ]

    TEMPLATES_DIR = os.path.join(dir_path, "..", "templates")
    STATIC_FILES_DIR = os.path.join(dir_path, "..", "..", "public")


settings = Settings()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

