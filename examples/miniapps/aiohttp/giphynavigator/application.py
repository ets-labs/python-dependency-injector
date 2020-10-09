"""Application module."""

from aiohttp import web

from .containers import Container
from . import handlers


def create_app() -> web.Application:
    container = Container()
    container.config.from_yaml('config.yml')
    container.config.giphy.api_key.from_env('GIPHY_API_KEY')
    container.wire(modules=[handlers])

    app = web.Application()
    app.container = container
    app.add_routes([
        web.get('/', handlers.index),
    ])
    return app
