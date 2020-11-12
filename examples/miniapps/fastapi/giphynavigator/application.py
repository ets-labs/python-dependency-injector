"""Application module."""

from fastapi import FastAPI

from .containers import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml('config.yml')
    container.config.giphy.api_key.from_env('GIPHY_API_KEY')
    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.add_api_route('/', endpoints.index)
    return app


app = create_app()
