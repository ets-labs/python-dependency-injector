from typing import AsyncIterator, Iterator
from unittest.mock import ANY

from anyio import sleep
from pytest import mark, raises

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.ext.starlette import Lifespan
from dependency_injector.providers import Resource, Self, Singleton


class TestLifespan:
    @mark.parametrize("sync", [False, True])
    @mark.asyncio
    async def test_context_manager(self, sync: bool) -> None:
        init, shutdown = False, False

        def sync_resource() -> Iterator[None]:
            nonlocal init, shutdown

            init = True
            yield
            shutdown = True

        async def async_resource() -> AsyncIterator[None]:
            nonlocal init, shutdown

            init = True
            yield
            shutdown = True

        class Container(DeclarativeContainer):
            x = Resource(sync_resource if sync else async_resource)

        container = Container()
        lifespan = Lifespan(container)

        async with lifespan(ANY) as scope:
            assert scope is None
            assert init

        assert shutdown

    @mark.asyncio
    async def test_schedule(self) -> None:
        done = False

        async def task() -> None:
            nonlocal done
            await sleep(0)
            done = True

        async def async_resource(lifespan: Lifespan) -> AsyncIterator[None]:
            lifespan.schedule(task)
            yield

        class Container(DeclarativeContainer):
            __self__ = Self()
            lifespan = Singleton(Lifespan, __self__)
            x = Resource(async_resource, lifespan)

        container = Container()

        async with container.lifespan():
            pass

        assert done

    @mark.asyncio
    async def test_non_reentrant(self) -> None:
        class Container(DeclarativeContainer):
            pass

        container = Container()
        lifespan = Lifespan(container)

        async with lifespan:
            with raises(RuntimeError, match=r"non-reentrant"):
                async with lifespan:
                    assert False, "should not reach this code"

    def test_not_initialized(self) -> None:
        with raises(RuntimeError, match=r"not initialized"):
            Lifespan(ANY).schedule(ANY)
