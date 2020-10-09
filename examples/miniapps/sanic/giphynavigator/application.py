"""Application module."""

from sanic import Sanic

from .containers import Container
from . import handlers


def create_app() -> Sanic:
    """Create and return Sanic application."""
    container = Container()
    container.config.from_yaml('config.yml')
    container.config.giphy.api_key.from_env('GIPHY_API_KEY')
    container.wire(modules=[handlers])

    app = Sanic('Giphy Navigator')
    app.container = container
    app.add_route(handlers.index, '/')
    return app
