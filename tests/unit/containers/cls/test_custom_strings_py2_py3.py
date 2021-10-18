"""Tests for container cls with custom string classes as attribute names.

See: https://github.com/ets-labs/python-dependency-injector/issues/479
"""

from dependency_injector import containers, providers
from pytest import fixture, raises


class CustomString(str):
    pass


class CustomClass:
    thing = None


class Container(containers.DeclarativeContainer):
    pass


@fixture
def provider():
    return providers.Provider()


def test_setattr(provider):
    setattr(Container, CustomString("test_attr"), provider)
    assert Container.test_attr is provider


def test_delattr():
    setattr(Container, CustomString("test_attr"), provider)
    delattr(Container, CustomString("test_attr"))
    with raises(AttributeError):
        Container.test_attr
