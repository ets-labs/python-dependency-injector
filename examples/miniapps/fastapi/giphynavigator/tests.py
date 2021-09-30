"""Tests module."""

from unittest import mock

import pytest
from httpx import AsyncClient

from giphynavigator.application import app
from giphynavigator.giphy import GiphyClient


@pytest.fixture
def client(event_loop):
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    event_loop.run_until_complete(client.aclose())


@pytest.mark.asyncio
async def test_index(client):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [
            {"url": "https://giphy.com/gif1.gif"},
            {"url": "https://giphy.com/gif2.gif"},
        ],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        response = await client.get(
            "/",
            params={
                "query": "test",
                "limit": 10,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data == {
        "query": "test",
        "limit": 10,
        "gifs": [
            {"url": "https://giphy.com/gif1.gif"},
            {"url": "https://giphy.com/gif2.gif"},
        ],
    }


@pytest.mark.asyncio
async def test_index_no_data(client):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["gifs"] == []


@pytest.mark.asyncio
async def test_index_default_params(client):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == app.container.config.default.query()
    assert data["limit"] == app.container.config.default.limit()
