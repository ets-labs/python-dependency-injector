import sys

from fastapi import FastAPI, Depends
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide


class Service:
    async def process(self) -> str:
        return 'Ok'


class Container(containers.DeclarativeContainer):

    service = providers.Factory(Service)


app = FastAPI()


@app.api_route('/')
@inject
async def index(service: Service = Depends(Provide[Container.service])):
    result = await service.process()
    return {'result': result}


container = Container()
container.wire(modules=[sys.modules[__name__]])
