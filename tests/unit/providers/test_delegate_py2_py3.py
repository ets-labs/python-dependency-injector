"""Delegate provider tests."""

from dependency_injector import providers, errors
from pytest import fixture, raises


@fixture
def provider():
    return providers.Provider()


@fixture
def delegate(provider):
    return providers.Delegate(provider)


def test_is_provider(delegate):
    assert providers.is_provider(delegate) is True


def test_init_optional_provides(provider):
    delegate = providers.Delegate()
    delegate.set_provides(provider)
    assert delegate.provides is provider
    assert delegate() is provider


def test_set_provides_returns_self(delegate, provider):
    assert delegate.set_provides(provider) is delegate


def test_init_with_not_provider():
    with raises(errors.Error):
        providers.Delegate(object())


def test_call(delegate, provider):
    delegated1 = delegate()
    delegated2 = delegate()

    assert delegated1 is provider
    assert delegated2 is provider


def test_repr(delegate, provider):
    assert repr(delegate) == (
        "<dependency_injector.providers."
        "Delegate({0}) at {1}>".format(repr(provider), hex(id(delegate)))
    )
