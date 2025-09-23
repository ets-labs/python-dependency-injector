from typing import Any, Iterator

from pytest import fixture

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Object
from dependency_injector.wiring import Provide, inject


class A:
    @inject
    def foo(self, value: str = Provide["value"]) -> str:
        return "A" + value


class B(A): ...


class C(A):
    def foo(self, *args: Any, **kwargs: Any) -> str:
        return "C" + super().foo()


class D(B, C): ...


class Container(DeclarativeContainer):
    value = Object("X")


@fixture
def container() -> Iterator[Container]:
    c = Container()
    c.wire(modules=[__name__])
    yield c
    c.unwire()


def test_preserve_mro(container: Container) -> None:
    assert D().foo() == "CAX"
