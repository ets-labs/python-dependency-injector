"""Main module."""

from aiohttp import web

from .application import create_app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
