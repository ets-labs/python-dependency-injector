from unittest import mock

import pytest
from httpx import ASGITransport, AsyncClient

from fastapi_di_example import app, container, Service


@pytest.fixture
async def client(event_loop):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_index(client):
    service_mock = mock.AsyncMock(spec=Service)
    service_mock.process.return_value = "Foo"

    with container.service.override(service_mock):
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"result": "Foo"}
