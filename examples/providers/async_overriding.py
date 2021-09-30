"""Provider overriding in async mode example."""

import asyncio

from dependency_injector import containers, providers


async def init_async_resource():
    return ...


def init_resource_mock():
    return ...


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(init_async_resource)


async def main(container: Container):
    resource1 = await container.resource()

    container.resource.override(providers.Callable(init_resource_mock))
    resource2 = await container.resource()
    ...


if __name__ == "__main__":
    container = Container()

    asyncio.run(main(container))
