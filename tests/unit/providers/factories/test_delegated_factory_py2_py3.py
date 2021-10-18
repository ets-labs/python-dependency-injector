"""DelegatedFactory provider tests."""

from dependency_injector import providers

from .common import Example


def test_inheritance():
    assert isinstance(providers.DelegatedFactory(object), providers.Factory)


def test_is_provider():
    assert providers.is_provider(providers.DelegatedFactory(object)) is True


def test_is_delegated_provider():
    assert providers.is_delegated(providers.DelegatedFactory(object)) is True


def test_repr():
    provider = providers.DelegatedFactory(Example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "DelegatedFactory({0}) at {1}>".format(repr(Example), hex(id(provider)))
    )
