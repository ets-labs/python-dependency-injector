"""DelegatedCallable provider tests."""

from dependency_injector import providers

from .common import example


def test_inheritance():
    assert isinstance(providers.DelegatedCallable(example), providers.Callable)


def test_is_provider():
    assert providers.is_provider(providers.DelegatedCallable(example)) is True


def test_is_delegated_provider():
    provider = providers.DelegatedCallable(example)
    assert providers.is_delegated(provider) is True


def test_repr():
    provider = providers.DelegatedCallable(example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "DelegatedCallable({0}) at {1}>".format(repr(example), hex(id(provider)))
    )
