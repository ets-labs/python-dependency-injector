"""Tests module."""

from unittest import mock

import pytest
from sanic import Sanic

from giphynavigator.application import create_app
from giphynavigator.giphy import GiphyClient


@pytest.fixture
def app():
    Sanic.test_mode = True
    app = create_app()
    yield app
    app.ctx.container.unwire()


@pytest.fixture
def test_client(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def test_index(app, test_client):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [
            {"url": "https://giphy.com/gif1.gif"},
            {"url": "https://giphy.com/gif2.gif"},
        ],
    }

    with app.ctx.container.giphy_client.override(giphy_client_mock):
        response = await test_client.get(
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


async def test_index_no_data(app, test_client):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [],
    }

    with app.ctx.container.giphy_client.override(giphy_client_mock):
        response = await test_client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["gifs"] == []


async def test_index_default_params(app, test_client):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [],
    }

    with app.ctx.container.giphy_client.override(giphy_client_mock):
        response = await test_client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == app.ctx.container.config.default.query()
    assert data["limit"] == app.ctx.container.config.default.limit()
