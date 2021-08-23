import os
import pytest
from tortoise.contrib.test import finalizer, initializer
from app.core.config import settings
from typing import Generator
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(settings.TORTOISE_MODELS, db_url=db_url, app_label="models")
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
