"""Factory delegate provider tests."""

from dependency_injector import providers, errors
from pytest import fixture, raises


@fixture
def factory():
    return providers.Factory(object)


@fixture
def delegate(factory):
    return providers.FactoryDelegate(factory)


def test_is_delegate(delegate):
    assert isinstance(delegate, providers.Delegate)


def test_init_with_not_factory():
    with raises(errors.Error):
        providers.FactoryDelegate(providers.Object(object()))
