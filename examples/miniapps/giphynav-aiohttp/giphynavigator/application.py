"""Application module."""

from aiohttp import web

from .containers import ApplicationContainer


def create_app():
    """Create and return Flask application."""
    container = ApplicationContainer()
    container.config.from_yaml('config.yml')
    container.config.giphy.api_key.from_env('GIPHY_API_KEY')

    app: web.Application = container.app()
    app.container = container

    app.add_routes([
        web.get('/', container.index_view.as_view()),
    ])

    return app
