#!/usr/bin/env python
# uvicorn --factory example:container.app

from asyncio import sleep
from logging import basicConfig, getLogger
from typing import AsyncIterator

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.ext.starlette import Lifespan
from dependency_injector.providers import Factory, Resource, Self, Singleton

count = 0


async def periodic_task(interval: float) -> None:
    global count
    log = getLogger(__name__)

    while True:
        log.debug("doing some periodic job #%d", count)
        count += 1
        await sleep(interval)


async def housekeeping(lifespan: Lifespan) -> AsyncIterator[None]:
    log = getLogger(__name__)
    log.debug("startup")
    lifespan.schedule(periodic_task, 5)
    yield
    log.debug("shutdown")


async def homepage(request: Request) -> JSONResponse:
    return JSONResponse({"hello": "world", "count": count})


class Container(DeclarativeContainer):
    __self__ = Self()
    lifespan = Singleton(Lifespan, __self__)
    housekeeping = Resource(housekeeping, lifespan)
    logging = Resource(
        basicConfig,
        level="DEBUG",
        datefmt="%Y-%m-%d %H:%M",
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    app = Factory(
        Starlette,
        debug=True,
        lifespan=lifespan,
        routes=[Route("/", homepage)],
    )


container = Container()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(container.app, factory=True, log_config=None)
