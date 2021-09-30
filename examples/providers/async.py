"""Asynchronous injections example."""

import asyncio

from dependency_injector import containers, providers


async def init_async_resource():
    await asyncio.sleep(0.1)
    yield "Initialized"


class Service:
    def __init__(self, resource):
        self.resource = resource


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(init_async_resource)

    service = providers.Factory(
        Service,
        resource=resource,
    )


async def main(container: Container):
    resource = await container.resource()
    service = await container.service()
    ...


if __name__ == "__main__":
    container = Container()

    asyncio.run(main(container))
