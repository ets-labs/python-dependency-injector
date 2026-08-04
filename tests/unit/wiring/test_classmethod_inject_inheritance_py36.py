"""Test that @inject on classmethods preserves correct cls in subclasses.

See issue for details: https://github.com/ets-labs/python-dependency-injector/issues/947
"""

import sys

from pytest import fixture
from typing_extensions import Annotated

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import Provide, inject


class Container(DeclarativeContainer):
    singleton = providers.Singleton(lambda: object())


class Base:
    @classmethod
    @inject
    def injected_factory(cls, singleton: Annotated[object, Provide["singleton"]]):
        return cls, singleton


class Sub1(Base):
    pass


class Sub2(Sub1):
    pass


@fixture
def container():
    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    yield container
    container.unwire()


def test_base_injected_classmethod(container):
    sentinel = container.singleton()

    for cls in [Sub2, Sub1, Base]:
        result = cls.injected_factory()
        assert result == (cls, sentinel)
