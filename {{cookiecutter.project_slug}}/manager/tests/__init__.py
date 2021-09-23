import os
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from manager.src.app import create_app


@pytest.fixture(scope="session")
async def test_client() -> AsyncClient:
    api = create_app(create_db=True)
    async with AsyncClient(app=api, base_url='http://localhost:5050') as client, LifespanManager(api):
        yield client
