"""Resource provider async tests."""

import asyncio
import inspect
import sys
from typing import Any

from dependency_injector import containers, providers, resources
from pytest import mark, raises


@mark.asyncio
async def test_init_async_function():
    resource = object()

    async def _init():
        await asyncio.sleep(0.001)
        _init.counter += 1
        return resource

    _init.counter = 0

    provider = providers.Resource(_init)

    result1 = await provider()
    assert result1 is resource
    assert _init.counter == 1

    result2 = await provider()
    assert result2 is resource
    assert _init.counter == 1

    await provider.shutdown()


@mark.asyncio
@mark.skipif(sys.version_info < (3, 6), reason="requires Python 3.6+")
async def test_init_async_generator():
    resource = object()

    async def _init():
        await asyncio.sleep(0.001)
        _init.init_counter += 1

        yield resource

        await asyncio.sleep(0.001)
        _init.shutdown_counter += 1

    _init.init_counter = 0
    _init.shutdown_counter = 0

    provider = providers.Resource(_init)

    result1 = await provider()
    assert result1 is resource
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 0

    await provider.shutdown()
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 1

    result2 = await provider()
    assert result2 is resource
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 1

    await provider.shutdown()
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 2


@mark.asyncio
async def test_init_async_class():
    resource = object()

    class TestResource(resources.AsyncResource):
        init_counter = 0
        shutdown_counter = 0

        async def init(self):
            await asyncio.sleep(0.001)
            self.__class__.init_counter += 1
            return resource

        async def shutdown(self, resource_):
            await asyncio.sleep(0.001)
            self.__class__.shutdown_counter += 1
            assert resource_ is resource

    provider = providers.Resource(TestResource)

    result1 = await provider()
    assert result1 is resource
    assert TestResource.init_counter == 1
    assert TestResource.shutdown_counter == 0

    await provider.shutdown()
    assert TestResource.init_counter == 1
    assert TestResource.shutdown_counter == 1

    result2 = await provider()
    assert result2 is resource
    assert TestResource.init_counter == 2
    assert TestResource.shutdown_counter == 1

    await provider.shutdown()
    assert TestResource.init_counter == 2
    assert TestResource.shutdown_counter == 2


def test_init_async_class_generic_typing():
    # See issue: https://github.com/ets-labs/python-dependency-injector/issues/488
    class TestDependency:
        ...

    class TestAsyncResource(resources.AsyncResource[TestDependency]):
        async def init(self, *args: Any, **kwargs: Any) -> TestDependency:
            return TestDependency()

        async def shutdown(self, resource: TestDependency) -> None: ...

    assert issubclass(TestAsyncResource, resources.AsyncResource) is True


def test_init_async_class_abc_init_definition_is_required():
    class TestAsyncResource(resources.AsyncResource):
        ...

    with raises(TypeError) as context:
        TestAsyncResource()

    assert "Can't instantiate abstract class TestAsyncResource" in str(context.value)
    assert "init" in str(context.value)


def test_init_async_class_abc_shutdown_definition_is_not_required():
    class TestAsyncResource(resources.AsyncResource):
        async def init(self):
            ...

    assert hasattr(TestAsyncResource(), "shutdown") is True
    assert inspect.iscoroutinefunction(TestAsyncResource.shutdown) is True


@mark.asyncio
async def test_init_with_error():
    async def _init():
        raise RuntimeError()

    provider = providers.Resource(_init)

    future = provider()
    assert provider.initialized is True
    assert provider.is_async_mode_enabled() is True

    with raises(RuntimeError):
        await future

    assert provider.initialized is False
    assert provider.is_async_mode_enabled() is True


@mark.asyncio
async def test_init_async_gen_with_error():
    async def _init():
        raise RuntimeError()
        yield

    provider = providers.Resource(_init)

    future = provider()
    assert provider.initialized is True
    assert provider.is_async_mode_enabled() is True

    with raises(RuntimeError):
        await future

    assert provider.initialized is False
    assert provider.is_async_mode_enabled() is True


@mark.asyncio
async def test_init_async_subclass_with_error():
    class _Resource(resources.AsyncResource):
        async def init(self):
            raise RuntimeError()

        async def shutdown(self, resource):
            pass

    provider = providers.Resource(_Resource)

    future = provider()
    assert provider.initialized is True
    assert provider.is_async_mode_enabled() is True

    with raises(RuntimeError):
        await future

    assert provider.initialized is False
    assert provider.is_async_mode_enabled() is True


@mark.asyncio
async def test_init_with_dependency_to_other_resource():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/361
    async def init_db_connection(db_url: str):
        await asyncio.sleep(0.001)
        yield {"connection": "OK", "url": db_url}

    async def init_user_session(db):
        await asyncio.sleep(0.001)
        yield {"session": "OK", "db": db}

    class Container(containers.DeclarativeContainer):
        config = providers.Configuration()

        db_connection = providers.Resource(
            init_db_connection,
            db_url=config.db_url,
        )

        user_session = providers.Resource(
            init_user_session,
            db=db_connection
        )

    async def main():
        container = Container(config={"db_url": "postgres://..."})
        try:
            return await container.user_session()
        finally:
            await container.shutdown_resources()

    result = await main()
    assert result == {"session": "OK", "db": {"connection": "OK", "url": "postgres://..."}}


@mark.asyncio
async def test_init_and_shutdown_methods():
    async def _init():
        await asyncio.sleep(0.001)
        _init.init_counter += 1

        yield

        await asyncio.sleep(0.001)
        _init.shutdown_counter += 1

    _init.init_counter = 0
    _init.shutdown_counter = 0

    provider = providers.Resource(_init)

    await provider.init()
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 0

    await provider.shutdown()
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 1

    await provider.init()
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 1

    await provider.shutdown()
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 2


@mark.asyncio
async def test_shutdown_of_not_initialized():
    async def _init():
        yield

    provider = providers.Resource(_init)
    provider.enable_async_mode()

    result = await provider.shutdown()
    assert result is None


@mark.asyncio
async def test_concurrent_init():
    resource = object()

    async def _init():
        await asyncio.sleep(0.001)
        _init.counter += 1
        return resource

    _init.counter = 0

    provider = providers.Resource(_init)

    result1, result2 = await asyncio.gather(
        provider(),
        provider()
    )

    assert result1 is resource
    assert _init.counter == 1

    assert result2 is resource
    assert _init.counter == 1
