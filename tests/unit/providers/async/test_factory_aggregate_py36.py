"""FactoryAggregate provider async mode tests."""

from dependency_injector import providers
from pytest import mark


@mark.asyncio
async def test_async_mode():
    object1 = object()
    object2 = object()

    async def _get_object1():
        return object1

    def _get_object2():
        return object2

    provider = providers.FactoryAggregate(
        object1=providers.Factory(_get_object1),
        object2=providers.Factory(_get_object2),
    )

    assert provider.is_async_mode_undefined() is True

    created_object1 = await provider("object1")
    assert created_object1 is object1
    assert provider.is_async_mode_enabled() is True

    created_object2 = await provider("object2")
    assert created_object2 is object2
