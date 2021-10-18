"""ThreadLocalSingleton provider async mode tests."""

import asyncio

from dependency_injector import providers
from pytest import mark, raises


@mark.asyncio
async def test_async_mode():
    instance = object()

    async def create_instance():
        return instance

    provider = providers.ThreadLocalSingleton(create_instance)

    instance1 = await provider()
    instance2 = await provider()

    assert instance1 is instance2
    assert instance1 is instance
    assert instance2 is instance


@mark.asyncio
async def test_concurrent_init():
    async def create_instance():
        return object()

    provider = providers.ThreadLocalSingleton(create_instance)

    future_instance1 = provider()
    future_instance2 = provider()

    instance1, instance2 = await asyncio.gather(future_instance1, future_instance2)

    assert instance1 is instance2


@mark.asyncio
async def test_async_init_with_error():
    async def create_instance():
        create_instance.counter += 1
        raise RuntimeError()
    create_instance.counter = 0

    provider = providers.ThreadLocalSingleton(create_instance)

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
