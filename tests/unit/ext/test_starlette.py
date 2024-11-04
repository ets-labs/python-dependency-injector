from typing import AsyncIterator, Iterator
from unittest.mock import ANY

from pytest import mark

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.ext.starlette import Lifespan
from dependency_injector.providers import Resource


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
