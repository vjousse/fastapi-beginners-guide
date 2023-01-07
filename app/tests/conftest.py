import asyncio
import os
from typing import Generator, Iterator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.core.config import settings
from app.main import app


@pytest.fixture(scope="module")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test client
@pytest.fixture(scope="module")
def client(event_loop: asyncio.BaseEventLoop) -> Iterator[TestClient]:
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(
        settings.TORTOISE_MODELS, db_url=db_url, app_label="models", loop=event_loop
    )
    with TestClient(app) as c:
        yield c
    finalizer()
