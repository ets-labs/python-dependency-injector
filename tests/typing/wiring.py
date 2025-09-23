from typing import Iterator

from typing_extensions import Annotated

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Object, Resource
from dependency_injector.wiring import Closing, Provide, required


def _resource() -> Iterator[int]:
    yield 1


class Container(DeclarativeContainer):
    value = Object(1)
    res = Resource(_resource)


def default_by_ref(value: int = Provide[Container.value]) -> None: ...
def default_by_string(value: int = Provide["value"]) -> None: ...
def default_by_string_with_modifier(
    value: int = Provide["value", required().as_int()]
) -> None: ...
def default_container(container: Container = Provide[Container]) -> None: ...
def default_with_closing(value: int = Closing[Provide[Container.res]]) -> None: ...
def annotated_by_ref(value: Annotated[int, Provide[Container.value]]) -> None: ...
def annotated_by_string(value: Annotated[int, Provide["value"]]) -> None: ...
def annotated_by_string_with_modifier(
    value: Annotated[int, Provide["value", required().as_int()]],
) -> None: ...
def annotated_container(
    container: Annotated[Container, Provide[Container]],
) -> None: ...
def annotated_with_closing(
    value: Annotated[int, Closing[Provide[Container.res]]],
) -> None: ...
