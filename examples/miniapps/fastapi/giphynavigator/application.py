"""Application module."""

from fastapi import FastAPI

from .containers import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()
    container.config.giphy.api_key.from_env("GIPHY_API_KEY")

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()
