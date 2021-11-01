"""Factory provider async mode tests."""

import asyncio

from dependency_injector import containers, providers
from pytest import mark, raises

from .common import RESOURCE1, RESOURCE2, Client, Service, BaseContainer, Container, init_resource


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
async def test_async_provider_with_async_injections():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/368
    async def async_client_provider():
        return {"client": "OK"}

    async def async_service(client):
        return {"service": "OK", "client": client}

    class Container(containers.DeclarativeContainer):
        client = providers.Factory(async_client_provider)
        service = providers.Factory(async_service, client=client)

    container = Container()
    service = await container.service()

    assert service == {"service": "OK", "client": {"client": "OK"}}


@mark.asyncio
async def test_with_awaitable_injection():
    class SomeResource:
        def __await__(self):
            raise RuntimeError("Should never happen")

    async def init_resource():
        yield SomeResource()

    class Service:
        def __init__(self, resource) -> None:
            self.resource = resource

    class Container(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource)
        service = providers.Factory(Service, resource=resource)

    container = Container()

    assert isinstance(container.service(), asyncio.Future)
    assert isinstance(container.resource(), asyncio.Future)

    resource = await container.resource()
    service = await container.service()

    assert isinstance(resource, SomeResource)
    assert isinstance(service.resource, SomeResource)
    assert service.resource is resource


@mark.asyncio
async def test_with_awaitable_injection_and_with_init_resources_call():
    class SomeResource:
        def __await__(self):
            raise RuntimeError("Should never happen")

    async def init_resource():
        yield SomeResource()

    class Service:
        def __init__(self, resource) -> None:
            self.resource = resource

    class Container(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource)
        service = providers.Factory(Service, resource=resource)

    container = Container()

    await container.init_resources()
    assert isinstance(container.service(), asyncio.Future)
    assert isinstance(container.resource(), asyncio.Future)

    resource = await container.resource()
    service = await container.service()

    assert isinstance(resource, SomeResource)
    assert isinstance(service.resource, SomeResource)
    assert service.resource is resource


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
