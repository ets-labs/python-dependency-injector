"""Tests module."""

from unittest import mock

import pytest

from giphynavigator.application import create_app
from giphynavigator.giphy import GiphyClient


@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()


async def test_index(app):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        'data': [
            {'url': 'https://giphy.com/gif1.gif'},
            {'url': 'https://giphy.com/gif2.gif'},
        ],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        _, response = await app.asgi_client.get(
            '/',
            params={
                'query': 'test',
                'limit': 10,
            },
        )

    assert response.status == 200
    data = response.json()
    assert data == {
        'query': 'test',
        'limit': 10,
        'gifs': [
            {'url': 'https://giphy.com/gif1.gif'},
            {'url': 'https://giphy.com/gif2.gif'},
        ],
    }


async def test_index_no_data(app):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        'data': [],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        _, response = await app.asgi_client.get('/')

    assert response.status == 200
    data = response.json()
    assert data['gifs'] == []


async def test_index_default_params(app):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        'data': [],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        _, response = await app.asgi_client.get('/')

    assert response.status == 200
    data = response.json()
    assert data['query'] == app.container.config.default.query()
    assert data['limit'] == app.container.config.default.limit()
