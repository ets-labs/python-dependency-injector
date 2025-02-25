"""Application module."""

from typing import Annotated

from fastapi import Depends, FastAPI

from dependency_injector.wiring import Provide, inject

from .containers import Container
from .services import Service

app = FastAPI()


@app.api_route("/")
@inject
async def index(
    service: Annotated[Service, Depends(Provide[Container.service])]
) -> dict[str, str]:
    value = await service.process()
    return {"result": value}


container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost")
container.config.redis_password.from_env("REDIS_PASSWORD", "password")
container.wire(modules=[__name__])
