import pytest
from httpx import AsyncClient

from service.src.asgi import api


@pytest.fixture
def test_client(event_loop) -> AsyncClient:
    client = AsyncClient(app=api, base_url='http://test')
    yield client

    event_loop.run_until_complete(client.aclose())
