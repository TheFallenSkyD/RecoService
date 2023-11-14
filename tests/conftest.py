# pylint: disable=redefined-outer-name
import asyncio
from typing import AsyncGenerator, Iterator

import nest_asyncio
import pytest
from httpx import AsyncClient

from main import app


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def jwt_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiIn0.qaNDbCKz5PkUk4KcZOkuaLF6LGztgC6WEpI8evwhm2E"


@pytest.fixture
async def client(jwt_token) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="https://test") as client:
        client.headers.update({"Authorization": f"Bearer {jwt_token}"})

        yield client
