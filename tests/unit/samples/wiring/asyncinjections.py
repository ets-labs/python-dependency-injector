import asyncio

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide, Closing


class TestResource:
    def __init__(self):
        self.init_counter = 0
        self.shutdown_counter = 0

    def reset_counters(self):
        self.init_counter = 0
        self.shutdown_counter = 0


resource1 = TestResource()
resource2 = TestResource()


async def async_resource(resource):
    await asyncio.sleep(0.001)
    resource.init_counter += 1

    yield resource

    await asyncio.sleep(0.001)
    resource.shutdown_counter += 1


class Container(containers.DeclarativeContainer):

    resource1 = providers.Resource(async_resource, providers.Object(resource1))
    resource2 = providers.Resource(async_resource, providers.Object(resource2))


@inject
async def async_injection(
        resource1: object = Provide[Container.resource1],
        resource2: object = Provide[Container.resource2],
):
    return resource1, resource2


@inject
async def async_injection_with_closing(
        resource1: object = Closing[Provide[Container.resource1]],
        resource2: object = Closing[Provide[Container.resource2]],
):
    return resource1, resource2
