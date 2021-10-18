"""Dependency provider async mode tests."""

from dependency_injector import providers, errors
from pytest import mark, raises


@mark.asyncio
async def test_provide_error():
    async def get_async():
        raise Exception

    provider = providers.Dependency()
    provider.override(providers.Callable(get_async))

    with raises(Exception):
        await provider()


@mark.asyncio
async def test_isinstance():
    dependency = 1.0

    async def get_async():
        return dependency

    provider = providers.Dependency(instance_of=float)
    provider.override(providers.Callable(get_async))

    assert provider.is_async_mode_undefined() is True

    dependency1 = await provider()

    assert provider.is_async_mode_enabled() is True

    dependency2 = await provider()

    assert dependency1 == dependency
    assert dependency2 == dependency


@mark.asyncio
async def test_isinstance_invalid():
    async def get_async():
        return {}

    provider = providers.Dependency(instance_of=float)
    provider.override(providers.Callable(get_async))

    assert provider.is_async_mode_undefined() is True

    with raises(errors.Error):
        await provider()

    assert provider.is_async_mode_enabled() is True


@mark.asyncio
async def test_async_mode():
    dependency = 123

    async def get_async():
        return dependency

    def get_sync():
        return dependency

    provider = providers.Dependency(instance_of=int)
    provider.override(providers.Factory(get_async))

    assert provider.is_async_mode_undefined() is True

    dependency1 = await provider()

    assert provider.is_async_mode_enabled() is True

    dependency2 = await provider()
    assert dependency1 == dependency
    assert dependency2 == dependency

    provider.override(providers.Factory(get_sync))

    dependency3 = await provider()

    assert provider.is_async_mode_enabled() is True

    dependency4 = await provider()
    assert dependency3 == dependency
    assert dependency4 == dependency
