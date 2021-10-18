"""DelegatedThreadLocalSingleton provider async mode tests."""

import asyncio

from dependency_injector import providers
from pytest import mark


@mark.asyncio
async def test_async_mode():
    instance = object()

    async def create_instance():
        return instance

    provider = providers.DelegatedThreadLocalSingleton(create_instance)

    instance1 = await provider()
    instance2 = await provider()

    assert instance1 is instance2
    assert instance1 is instance
    assert instance2 is instance


@mark.asyncio
async def test_concurrent_init():
    async def create_instance():
        return object()

    provider = providers.DelegatedThreadLocalSingleton(create_instance)

    future_instance1 = provider()
    future_instance2 = provider()

    instance1, instance2 = await asyncio.gather(future_instance1, future_instance2)

    assert instance1 is instance2
