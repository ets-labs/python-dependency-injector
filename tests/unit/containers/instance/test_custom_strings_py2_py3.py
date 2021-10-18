"""Tests for container with custom string classes as attribute names.

See: https://github.com/ets-labs/python-dependency-injector/issues/479
"""

from dependency_injector import containers, providers
from pytest import fixture, raises


class CustomString(str):
    pass


class CustomClass:
    thing = None


@fixture
def container():
    return containers.DynamicContainer()


@fixture
def provider():
    return providers.Provider()


def test_setattr(container, provider):
    setattr(container, CustomString("test_attr"), provider)
    assert container.test_attr is provider


def test_delattr(container, provider):
    setattr(container, CustomString("test_attr"), provider)
    delattr(container, CustomString("test_attr"))
    with raises(AttributeError):
        container.test_attr


def test_set_provider(container, provider):
    container.set_provider(CustomString("test_attr"), provider)
    assert container.test_attr is provider


def test_set_providers(container, provider):
    container.set_providers(**{CustomString("test_attr"): provider})
    assert container.test_attr is provider
