"""Tests for provide async mode typing stubs."""

from pytest import mark

from .common import Container, Client, Service, RESOURCE1, RESOURCE2


@mark.asyncio
async def test_async_():
    container = Container()

    client1 = await container.client.async_()
    client2 = await container.client.async_()

    assert isinstance(client1, Client)
    assert client1.resource1 is RESOURCE1
    assert client1.resource2 is RESOURCE2

    assert isinstance(client2, Client)
    assert client2.resource1 is RESOURCE1
    assert client2.resource2 is RESOURCE2

    service1 = await container.service.async_()
    service2 = await container.service.async_()

    assert isinstance(service1, Service)
    assert isinstance(service1.client, Client)
    assert service1.client.resource1 is RESOURCE1
    assert service1.client.resource2 is RESOURCE2

    assert isinstance(service2, Service)
    assert isinstance(service2.client, Client)
    assert service2.client.resource1 is RESOURCE1
    assert service2.client.resource2 is RESOURCE2

    assert service1.client is not service2.client
