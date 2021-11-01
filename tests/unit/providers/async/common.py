"""Common test artifacts."""

import asyncio
import random

from dependency_injector import containers, providers


RESOURCE1 = object()
RESOURCE2 = object()


async def init_resource(resource):
    await asyncio.sleep(random.randint(1, 10) / 1000)
    yield resource
    await asyncio.sleep(random.randint(1, 10) / 1000)


class Client:
    def __init__(self, resource1: object, resource2: object) -> None:
        self.resource1 = resource1
        self.resource2 = resource2


class Service:
    def __init__(self, client: Client) -> None:
        self.client = client


class BaseContainer(containers.DeclarativeContainer):
    resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))
    resource2 = providers.Resource(init_resource, providers.Object(RESOURCE2))


class Container(BaseContainer):
    client = providers.Factory(
        Client,
        resource1=BaseContainer.resource1,
        resource2=BaseContainer.resource2,
    )

    service = providers.Factory(
        Service,
        client=client,
    )
