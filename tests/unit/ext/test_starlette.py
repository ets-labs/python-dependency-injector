from typing import AsyncIterator, Iterator, TypeVar
from unittest.mock import ANY

from pytest import mark

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.ext.starlette import Lifespan
from dependency_injector.providers import Resource

T = TypeVar("T")


class XResource(Resource[T]):
    """A test provider"""


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

        def nope():
            assert False, "should not be called"

        class Container(DeclarativeContainer):
            x = XResource(sync_resource if sync else async_resource)
            y = Resource(nope)

        container = Container()
        lifespan = Lifespan(container, resource_type=XResource)

        async with lifespan(ANY) as scope:
            assert scope is None
            assert init

        assert shutdown
