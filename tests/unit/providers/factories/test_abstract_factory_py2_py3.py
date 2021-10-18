"""AbstractFactory provider tests."""

from dependency_injector import providers, errors
from pytest import raises

from .common import Example


def test_inheritance():
    assert isinstance(providers.AbstractFactory(Example), providers.Factory)


def test_call_overridden_by_factory():
    provider = providers.AbstractFactory(object)
    provider.override(providers.Factory(Example))
    assert isinstance(provider(), Example)


def test_call_overridden_by_delegated_factory():
    provider = providers.AbstractFactory(object)
    provider.override(providers.DelegatedFactory(Example))
    assert isinstance(provider(), Example)


def test_call_not_overridden():
    provider = providers.AbstractFactory(object)
    with raises(errors.Error):
        provider()


def test_override_by_not_factory():
    provider = providers.AbstractFactory(object)
    with raises(errors.Error):
        provider.override(providers.Callable(object))


def test_provide_not_implemented():
    provider = providers.AbstractFactory(Example)
    with raises(NotImplementedError):
        provider._provide(tuple(), dict())


def test_repr():
    provider = providers.AbstractFactory(Example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "AbstractFactory({0}) at {1}>".format(repr(Example), hex(id(provider)))
    )
