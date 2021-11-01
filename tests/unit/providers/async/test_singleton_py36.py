"""Singleton provider async mode tests."""

import asyncio
import random

from dependency_injector import providers
from pytest import mark, raises

from .common import RESOURCE1, RESOURCE2, BaseContainer, Client, Service


@mark.asyncio
async def test_injections():
    class ContainerWithSingletons(BaseContainer):
        client = providers.Singleton(
            Client,
            resource1=BaseContainer.resource1,
            resource2=BaseContainer.resource2,
        )

        service = providers.Singleton(
            Service,
            client=client,
        )

    container = ContainerWithSingletons()

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

    assert service1 is service2
    assert service1.client is service2.client
    assert service1.client is client1

    assert service2.client is client2
    assert client1 is client2


@mark.asyncio
async def test_async_mode():
    instance = object()

    async def create_instance():
        return instance

    provider = providers.Singleton(create_instance)

    instance1 = await provider()
    instance2 = await provider()

    assert instance1 is instance2
    assert instance1 is instance
    assert instance2 is instance


@mark.asyncio
async def test_concurrent_init():
    async def create_instance():
        await asyncio.sleep(random.randint(1, 10) / 1000)
        return object()

    provider = providers.Singleton(create_instance)

    future_instance1 = provider()
    future_instance2 = provider()

    instance1, instance2 = await asyncio.gather(future_instance1, future_instance2)
    instance3 = await provider()

    assert instance1 is instance2 is instance3


@mark.asyncio
async def test_async_init_with_error():
    async def create_instance():
        create_instance.counter += 1
        raise RuntimeError()

    create_instance.counter = 0

    provider = providers.Singleton(create_instance)

    future = provider()
    assert provider.is_async_mode_enabled() is True

    with raises(RuntimeError):
        await future

    assert create_instance.counter == 1
    assert provider.is_async_mode_enabled() is True

    with raises(RuntimeError):
        await provider()

    assert create_instance.counter == 2
    assert provider.is_async_mode_enabled() is True
