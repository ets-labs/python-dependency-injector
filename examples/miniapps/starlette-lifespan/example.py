#!/usr/bin/env python

from logging import basicConfig, getLogger

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.ext.starlette import Lifespan
from dependency_injector.providers import Factory, Resource, Self, Singleton
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

count = 0


def init():
    log = getLogger(__name__)
    log.info("Inittializing resources")
    yield
    log.info("Cleaning up resources")


async def homepage(request: Request) -> JSONResponse:
    global count
    response = JSONResponse({"hello": "world", "count": count})
    count += 1
    return response


class Container(DeclarativeContainer):
    __self__ = Self()
    lifespan = Singleton(Lifespan, __self__)
    logging = Resource(
        basicConfig,
        level="DEBUG",
        datefmt="%Y-%m-%d %H:%M",
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    init = Resource(init)
    app = Factory(
        Starlette,
        debug=True,
        lifespan=lifespan,
        routes=[Route("/", homepage)],
    )


container = Container()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        container.app,
        factory=True,
        # NOTE: `None` prevents uvicorn from configuring logging, which is
        #       impossible via CLI
        log_config=None,
    )
