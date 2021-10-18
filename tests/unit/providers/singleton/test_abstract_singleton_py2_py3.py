"""AbstractSingleton provider tests."""

from dependency_injector import providers, errors
from pytest import raises

from .common import Example


def test_inheritance():
    assert isinstance(providers.AbstractSingleton(Example), providers.BaseSingleton)


def test_call_overridden_by_singleton():
    provider = providers.AbstractSingleton(object)
    provider.override(providers.Singleton(Example))
    assert isinstance(provider(), Example)


def test_call_overridden_by_delegated_singleton():
    provider = providers.AbstractSingleton(object)
    provider.override(providers.DelegatedSingleton(Example))
    assert isinstance(provider(), Example)


def test_call_not_overridden():
    provider = providers.AbstractSingleton(object)
    with raises(errors.Error):
        provider()


def test_reset_overridden():
    provider = providers.AbstractSingleton(object)
    provider.override(providers.Singleton(Example))

    instance1 = provider()

    provider.reset()

    instance2 = provider()

    assert instance1 is not instance2
    assert isinstance(instance1, Example)
    assert isinstance(instance2, Example)


def test_reset_not_overridden():
    provider = providers.AbstractSingleton(object)
    with raises(errors.Error):
        provider.reset()


def test_override_by_not_singleton():
    provider = providers.AbstractSingleton(object)
    with raises(errors.Error):
        provider.override(providers.Factory(object))


def test_repr():
    provider = providers.AbstractSingleton(Example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "AbstractSingleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
    )
