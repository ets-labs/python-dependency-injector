from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Coroutine, Optional

from anyio import create_task_group
from anyio.abc import TaskGroup
from typing_extensions import Self

from dependency_injector.containers import Container


class AbstractLifespan(metaclass=ABCMeta):
    """An interface class for OOP lunatics.

    See :class:`Lifespan`.
    """

    @abstractmethod
    def schedule(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        *args: Any,
        name: Optional[str] = None,
    ) -> None:
        """Schedule a background task."""

    @abstractmethod
    async def __aenter__(self) -> None:
        """Enter context."""

    @abstractmethod
    async def __aexit__(self, *exc_info: Any) -> None:
        """Exit context."""

    def __call__(self, app: Any) -> Self:
        return self


class Lifespan(AbstractLifespan):
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
    tg: Optional[TaskGroup]

    def __init__(self, container: Container) -> None:
        self.container = container
        self.tg = None

    async def __aenter__(self) -> None:
        if self.tg is not None:
            raise RuntimeError("non-reentrant")

        self.tg = tg = create_task_group()

        await tg.__aenter__()

        result = self.container.init_resources()

        if result is not None:
            await result

    async def __aexit__(self, *exc_info: Any) -> None:
        tg = self.tg
        result = self.container.shutdown_resources()

        if result is not None:
            await result

        if tg is not None:
            tg.cancel_scope.cancel()
            await tg.__aexit__(*exc_info)

    def schedule(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        *args: Any,
        name: Optional[str] = None,
    ) -> None:
        """Schedule a background task.

        :param func: a coroutine function
        :param args: positional arguments to call the function with
        :param name: name of the task, for the purposes of introspection and debugging
        """

        if self.tg is None:
            raise RuntimeError("not initialized")

        self.tg.start_soon(func, *args, name=name)


class NoopLifespan(AbstractLifespan):
    """A do-nothing implementation of the :class:`AbstractLifespan`.

    For use in tests to prevent unwanted resource initialization.
    """

    async def __aenter__(self) -> None:
        """Do nothing"""

    async def __aexit__(self, *exc_info: Any) -> None:
        """Do nothing"""

    def schedule(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        *args: Any,
        name: Optional[str] = None,
    ) -> None:
        """Do nothing"""
