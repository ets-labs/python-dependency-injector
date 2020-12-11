import asyncio
import random

from dependency_injector import containers, providers

# Runtime import to get asyncutils module
import os
_TOP_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../',
    )),
)
import sys
sys.path.append(_TOP_DIR)

from asyncutils import AsyncTestCase


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


class Container(containers.DeclarativeContainer):
    resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))
    resource2 = providers.Resource(init_resource, providers.Object(RESOURCE2))

    client = providers.Factory(
        Client,
        resource1=resource1,
        resource2=resource2,
    )

    service = providers.Factory(
        Service,
        client=client,
    )


class FactoryTests(AsyncTestCase):

    def test_direct_injection(self):
        container = Container()

        client1 = self._run(container.client())
        client2 = self._run(container.client())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

    def test_children_injection(self):
        container = Container()

        service1 = self._run(container.service())
        service2 = self._run(container.service())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIsNot(service1.client, service2.client)
