import sys
from typing import Any, Type

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

from dependency_injector.containers import Container
from dependency_injector.providers import Resource


class Lifespan:
    """A starlette lifespan handler performing container resource initialization and shutdown.

    See https://www.starlette.io/lifespan/ for details.

    Usage:

    .. code-block:: python

        from dependency_injector.containers import DeclarativeContainer
        from dependency_injector.ext.starlette import Lifespan
        from dependency_injector.providers import Factory, Self, Singleton
        from starlette.applications import Starlette

        class Container(DeclarativeContainer):
            __self__ = Self()
            lifespan = Singleton(Lifespan, __self__)
            app = Factory(Starlette, lifespan=lifespan)

    :param container: container instance
    :param resource_type: A :py:class:`~dependency_injector.resources.Resource`
        subclass. Limits the resources to be initialized and shutdown.
    """

    container: Container
    resource_type: Type[Resource[Any]]

    def __init__(
        self,
        container: Container,
        resource_type: Type[Resource[Any]] = Resource,
    ) -> None:
        self.container = container
        self.resource_type = resource_type

    def __call__(self, app: Any) -> Self:
        return self

    async def __aenter__(self) -> None:
        result = self.container.init_resources(self.resource_type)

        if result is not None:
            await result

    async def __aexit__(self, *exc_info: Any) -> None:
        result = self.container.shutdown_resources(self.resource_type)

        if result is not None:
            await result
