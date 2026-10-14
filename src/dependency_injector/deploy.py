"""Deploy module."""

import sys
from types import ModuleType
from typing import Any, Iterable, Optional, Union

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

from .containers import Container
from .wiring import ProvidersMap, _patched_registry


class ContainerDeploy:
    """Wire a container and initialize its resources for the duration of an async context.

    On enter, the container is wired and its resources are initialized. On exit, resources
    are shut down and the container is unwired, even when startup or shutdown fails.

    Calling the instance with an application returns the instance itself, so it can be passed
    to any framework that accepts a lifespan callable, e.g. Starlette or FastAPI.

    Modules to wire come from :py:attr:`wire_modules`, which returns :py:attr:`modules`. Set
    ``modules`` as a class attribute, pass it as a parameter, or override ``wire_modules`` to
    compute it. When it is ``None``, every imported module with an ``@inject`` callable whose
    markers this container resolves is wired.

    Usage:

    .. code-block:: python

        from dependency_injector.containers import DeclarativeContainer
        from dependency_injector.deploy import ContainerDeploy
        from fastapi import FastAPI

        class AppDeploy(ContainerDeploy):

            modules = ["app.api.routes", "app.api.websockets"]

        class Container(DeclarativeContainer):
            ...

        app = FastAPI(lifespan=AppDeploy(Container()))

        async def main():
            async with ContainerDeploy(Container(), modules=["app.cli"]):
                ...

    :param container: container instance
    :param modules: Modules to wire. Overrides the class attribute of the same name.
    """

    container: Container
    modules: Optional[Iterable[Union[ModuleType, str]]] = None

    def __init__(
        self,
        container: Container,
        modules: Optional[Iterable[Union[ModuleType, str]]] = None,
    ) -> None:
        self.container = container
        if modules is not None:
            self.modules = modules

    @property
    def wire_modules(self) -> Optional[Iterable[Union[ModuleType, str]]]:
        """Modules to wire, defaulting to modules with ``@inject`` markers this container resolves."""
        if self.modules is None:
            providers_map = ProvidersMap(self.container)
            self.modules = sorted(
                {
                    sys.modules[patched.patched.__module__]
                    for patched in _patched_registry._callables.values()
                    if any(
                        providers_map.resolve_provider(marker.provider, marker.modifier)
                        for marker in patched.reference_injections.values()
                    )
                },
                key=lambda module: module.__name__,
            )
        return self.modules

    def __call__(self, app: Any) -> Self:
        return self

    async def __aenter__(self) -> None:
        self.container.wire(modules=self.wire_modules)

        try:
            await self.init_resources()
        except BaseException:
            self.container.unwire()
            raise

    async def __aexit__(self, *exc_info: Any) -> None:
        try:
            await self.shutdown_resources()
        finally:
            self.container.unwire()

    async def init_resources(self) -> None:
        """Initialize container resources."""
        result = self.container.init_resources()

        if result is not None:
            await result

    async def shutdown_resources(self) -> None:
        """Shutdown container resources."""
        result = self.container.shutdown_resources()

        if result is not None:
            await result
