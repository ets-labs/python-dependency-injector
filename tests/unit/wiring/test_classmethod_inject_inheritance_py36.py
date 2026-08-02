"""Test that @inject on classmethods preserves correct cls in subclasses.

See issue for details: https://github.com/ets-labs/python-dependency-injector/issues/947
"""

import sys

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import inject, Provide
from pytest import fixture


class Container(DeclarativeContainer):
    singleton = providers.Singleton(lambda: object())


class Base:
    @classmethod
    @inject
    def injected_factory(cls, container: Container = Provide[Container]):
        return cls()


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


def test_base_injected_classmethod_returns_base(container):
    result = Base.injected_factory()
    assert isinstance(result, Base)
    assert type(result) is Base


def test_sub1_injected_classmethod_returns_sub1(container):
    result = Sub1.injected_factory()
    assert isinstance(result, Sub1)
    assert type(result) is Sub1


def test_sub2_injected_classmethod_returns_sub2(container):
    """Regression: Sub2.injected_factory() must return Sub2, not Sub1."""
    result = Sub2.injected_factory()
    assert isinstance(result, Sub2)
    assert type(result) is Sub2
