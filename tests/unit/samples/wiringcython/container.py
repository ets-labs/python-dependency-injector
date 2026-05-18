"""DI container used by the Cython-compiled wiring fixture."""

from dependency_injector import containers, providers


class Service:
    """Simple service injected into the Cython-compiled fixture handlers."""

    def __init__(self, value: str = "default") -> None:
        self.value = value

    async def aget(self) -> str:
        return self.value

    def get(self) -> str:
        return self.value


class Container(containers.DeclarativeContainer):
    service = providers.Factory(Service, value="injected")
