"""SingletonDelegate provider tests."""

from dependency_injector import providers, errors
from pytest import fixture, raises


@fixture
def provider():
    return providers.Singleton(object)


@fixture
def delegate(provider):
    return providers.SingletonDelegate(provider)


def test_is_delegate(delegate):
    assert isinstance(delegate, providers.Delegate)


def test_init_with_not_factory():
    with raises(errors.Error):
        providers.SingletonDelegate(providers.Object(object()))
