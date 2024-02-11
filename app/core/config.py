import os

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings

dir_path = os.path.dirname(os.path.realpath(__file__))


class Settings(BaseSettings):
    APP_NAME: str = "fastapi-tutorial"
    APP_VERSION: str = "0.0.1"
    SQLITE_URL: str = "sqlite:///./sql_app.db"

    TEMPLATES_DIR: str = os.path.join(dir_path, "..", "templates")
    STATIC_FILES_DIR: str = os.path.join(dir_path, "..", "..", "public")


settings = Settings()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
