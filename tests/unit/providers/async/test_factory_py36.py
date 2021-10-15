"""Factory async mode tests."""

import asyncio
import random

from dependency_injector import containers, providers
from pytest import mark, raises


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


@mark.asyncio
async def test_args_injection():
    class ContainerWithArgs(BaseContainer):
        client = providers.Factory(
            Client,
            BaseContainer.resource1,
            BaseContainer.resource2,
        )

        service = providers.Factory(
            Service,
            client,
        )

    container = ContainerWithArgs()

    client1 = await container.client()
    client2 = await container.client()

    assert isinstance(client1, Client)
    assert client1.resource1 is RESOURCE1
    assert client1.resource2 is RESOURCE2

    assert isinstance(client2, Client)
    assert client2.resource1 is RESOURCE1
    assert client2.resource2 is RESOURCE2

    service1 = await container.service()
    service2 = await container.service()

    assert isinstance(service1, Service)
    assert isinstance(service1.client, Client)
    assert service1.client.resource1 is RESOURCE1
    assert service1.client.resource2 is RESOURCE2

    assert isinstance(service2, Service)
    assert isinstance(service2.client, Client)
    assert service2.client.resource1 is RESOURCE1
    assert service2.client.resource2 is RESOURCE2

    assert service1.client is not service2.client


@mark.asyncio
async def test_kwargs_injection():
    class ContainerWithKwArgs(Container):
        ...

    container = ContainerWithKwArgs()

    client1 = await container.client()
    client2 = await container.client()

    assert isinstance(client1, Client)
    assert client1.resource1 is RESOURCE1
    assert client1.resource2 is RESOURCE2

    assert isinstance(client2, Client)
    assert client2.resource1 is RESOURCE1
    assert client2.resource2 is RESOURCE2

    service1 = await container.service()
    service2 = await container.service()

    assert isinstance(service1, Service)
    assert isinstance(service1.client, Client)
    assert service1.client.resource1 is RESOURCE1
    assert service1.client.resource2 is RESOURCE2

    assert isinstance(service2, Service)
    assert isinstance(service2.client, Client)
    assert service2.client.resource1 is RESOURCE1
    assert service2.client.resource2 is RESOURCE2

    assert service1.client is not service2.client


@mark.asyncio
async def test_context_kwargs_injection():
    resource2_extra = object()

    container = Container()

    client1 = await container.client(resource2=resource2_extra)
    client2 = await container.client(resource2=resource2_extra)

    assert isinstance(client1, Client)
    assert client1.resource1 is RESOURCE1
    assert client1.resource2 is resource2_extra

    assert isinstance(client2, Client)
    assert client2.resource1 is RESOURCE1
    assert client2.resource2 is resource2_extra


@mark.asyncio
async def test_args_kwargs_injection():
    class ContainerWithArgsAndKwArgs(BaseContainer):
        client = providers.Factory(
            Client,
            BaseContainer.resource1,
            resource2=BaseContainer.resource2,
        )

        service = providers.Factory(
            Service,
            client=client,
        )

    container = ContainerWithArgsAndKwArgs()

    client1 = await container.client()
    client2 = await container.client()

    assert isinstance(client1, Client)
    assert client1.resource1 is RESOURCE1
    assert client1.resource2 is RESOURCE2

    assert isinstance(client2, Client)
    assert client2.resource1 is RESOURCE1
    assert client2.resource2 is RESOURCE2

    service1 = await container.service()
    service2 = await container.service()

    assert isinstance(service1, Service)
    assert isinstance(service1.client, Client)
    assert service1.client.resource1 is RESOURCE1
    assert service1.client.resource2 is RESOURCE2

    assert isinstance(service2, Service)
    assert isinstance(service2.client, Client)
    assert service2.client.resource1 is RESOURCE1
    assert service2.client.resource2 is RESOURCE2

    assert service1.client is not service2.client


@mark.asyncio
async def test_injection_error():
    async def init_resource():
        raise Exception("Something went wrong")

    class Container(containers.DeclarativeContainer):
        resource_with_error = providers.Resource(init_resource)

        client = providers.Factory(
            Client,
            resource1=resource_with_error,
            resource2=None,
        )

    container = Container()

    with raises(Exception, match="Something went wrong"):
        await container.client()


@mark.asyncio
async def test_injection_runtime_error_async_provides():
    async def create_client(*args,  **kwargs):
        raise Exception("Something went wrong")

    class Container(BaseContainer):
        client = providers.Factory(
            create_client,
            resource1=BaseContainer.resource1,
            resource2=None,
        )

    container = Container()

    with raises(Exception, match="Something went wrong"):
        await container.client()


@mark.asyncio
async def test_injection_call_error_async_provides():
    async def create_client():  # <-- no args defined
        ...

    class Container(BaseContainer):
        client = providers.Factory(
            create_client,
            resource1=BaseContainer.resource1,
            resource2=None,
        )

    container = Container()

    with raises(TypeError) as exception_info:
        await container.client()
    assert "create_client() got" in str(exception_info.value)
    assert "unexpected keyword argument" in str(exception_info.value)


@mark.asyncio
async def test_attributes_injection():
    class ContainerWithAttributes(BaseContainer):
        client = providers.Factory(
            Client,
            BaseContainer.resource1,
            resource2=None,
        )
        client.add_attributes(resource2=BaseContainer.resource2)

        service = providers.Factory(
            Service,
            client=None,
        )
        service.add_attributes(client=client)

    container = ContainerWithAttributes()

    client1 = await container.client()
    client2 = await container.client()

    assert isinstance(client1, Client)
    assert client1.resource1 is RESOURCE1
    assert client1.resource2 is RESOURCE2

    assert isinstance(client2, Client)
    assert client2.resource1 is RESOURCE1
    assert client2.resource2 is RESOURCE2

    service1 = await container.service()
    service2 = await container.service()

    assert isinstance(service1, Service)
    assert isinstance(service1.client, Client)
    assert service1.client.resource1 is RESOURCE1
    assert service1.client.resource2 is RESOURCE2

    assert isinstance(service2, Service)
    assert isinstance(service2.client, Client)
    assert service2.client.resource1 is RESOURCE1
    assert service2.client.resource2 is RESOURCE2

    assert service1.client is not service2.client


@mark.asyncio
async def test_attributes_injection_attribute_error():
    class ClientWithException(Client):
        @property
        def attribute_set_error(self):
            return None

        @attribute_set_error.setter
        def attribute_set_error(self, value):
            raise Exception("Something went wrong")

    class Container(BaseContainer):
        client = providers.Factory(
            ClientWithException,
            resource1=BaseContainer.resource1,
            resource2=BaseContainer.resource2,
        )
        client.add_attributes(attribute_set_error=123)

    container = Container()

    with raises(Exception, match="Something went wrong"):
        await container.client()


@mark.asyncio
async def test_attributes_injection_runtime_error():
    async def init_resource():
        raise Exception("Something went wrong")

    class Container(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource)

        client = providers.Factory(
            Client,
            resource1=None,
            resource2=None,
        )
        client.add_attributes(resource1=resource)
        client.add_attributes(resource2=resource)

    container = Container()

    with raises(Exception, match="Something went wrong"):
        await container.client()


@mark.asyncio
async def test_async_instance_and_sync_attributes_injection():
    class ContainerWithAttributes(BaseContainer):
        resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))

        client = providers.Factory(
            Client,
            BaseContainer.resource1,
            resource2=None,
        )
        client.add_attributes(resource2=providers.Object(RESOURCE2))

        service = providers.Factory(
            Service,
            client=None,
        )
        service.add_attributes(client=client)

    container = ContainerWithAttributes()

    client1 = await container.client()
    client2 = await container.client()

    assert isinstance(client1, Client)
    assert client1.resource1 is RESOURCE1
    assert client1.resource2 is RESOURCE2

    assert isinstance(client2, Client)
    assert client2.resource1 is RESOURCE1
    assert client2.resource2 is RESOURCE2

    service1 = await container.service()
    service2 = await container.service()

    assert isinstance(service1, Service)
    assert isinstance(service1.client, Client)
    assert service1.client.resource1 is RESOURCE1
    assert service1.client.resource2 is RESOURCE2

    assert isinstance(service2, Service)
    assert isinstance(service2.client, Client)
    assert service2.client.resource1 is RESOURCE1
    assert service2.client.resource2 is RESOURCE2

    assert service1.client is not service2.client
