import sys
from typing import Any

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

from dependency_injector.containers import Container


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
    """

    container: Container

    def __init__(self, container: Container) -> None:
        self.container = container

    def __call__(self, app: Any) -> Self:
        return self

    async def __aenter__(self) -> None:
        result = self.container.init_resources()

        if result is not None:
            await result

    async def __aexit__(self, *exc_info: Any) -> None:
        result = self.container.shutdown_resources()

        if result is not None:
            await result
