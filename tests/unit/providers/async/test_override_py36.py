"""Tests for provider overriding in async mode."""

from dependency_injector import providers
from pytest import mark


@mark.asyncio
async def test_provider():
    dependency = object()

    async def _get_dependency_async():
        return dependency

    def _get_dependency_sync():
        return dependency

    provider = providers.Provider()

    provider.override(providers.Callable(_get_dependency_async))
    dependency1 = await provider()

    provider.override(providers.Callable(_get_dependency_sync))
    dependency2 = await provider()

    assert dependency1 is dependency
    assert dependency2 is dependency


@mark.asyncio
async def test_callable():
    dependency = object()

    async def _get_dependency_async():
        return dependency

    def _get_dependency_sync():
        return dependency

    provider = providers.Callable(_get_dependency_async)
    dependency1 = await provider()

    provider.override(providers.Callable(_get_dependency_sync))
    dependency2 = await provider()

    assert dependency1 is dependency
    assert dependency2 is dependency


@mark.asyncio
async def test_factory():
    dependency = object()

    async def _get_dependency_async():
        return dependency

    def _get_dependency_sync():
        return dependency

    provider = providers.Factory(_get_dependency_async)
    dependency1 = await provider()

    provider.override(providers.Callable(_get_dependency_sync))
    dependency2 = await provider()

    assert dependency1 is dependency
    assert dependency2 is dependency


@mark.asyncio
async def test_async_mode_enabling():
    dependency = object()

    async def _get_dependency_async():
        return dependency

    provider = providers.Callable(_get_dependency_async)
    assert provider.is_async_mode_undefined() is True

    await provider()

    assert provider.is_async_mode_enabled() is True


@mark.asyncio
async def test_async_mode_disabling():
    dependency = object()

    def _get_dependency():
        return dependency

    provider = providers.Callable(_get_dependency)
    assert provider.is_async_mode_undefined() is True

    provider()

    assert provider.is_async_mode_disabled() is True


@mark.asyncio
async def test_async_mode_enabling_on_overriding():
    dependency = object()

    async def _get_dependency_async():
        return dependency

    provider = providers.Provider()
    provider.override(providers.Callable(_get_dependency_async))
    assert provider.is_async_mode_undefined() is True

    await provider()

    assert provider.is_async_mode_enabled() is True


def test_async_mode_disabling_on_overriding():
    dependency = object()

    def _get_dependency():
        return dependency

    provider = providers.Provider()
    provider.override(providers.Callable(_get_dependency))
    assert provider.is_async_mode_undefined() is True

    provider()

    assert provider.is_async_mode_disabled() is True
