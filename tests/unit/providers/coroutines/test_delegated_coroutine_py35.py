"""DelegatedCoroutine provider tests."""

from dependency_injector import providers

from .common import example


def test_inheritance():
    assert isinstance(providers.DelegatedCoroutine(example), providers.Coroutine)


def test_is_provider():
    assert providers.is_provider(providers.DelegatedCoroutine(example)) is True


def test_is_delegated_provider():
    provider = providers.DelegatedCoroutine(example)
    assert providers.is_delegated(provider) is True


def test_repr():
    provider = providers.DelegatedCoroutine(example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "DelegatedCoroutine({0}) at {1}>".format(repr(example), hex(id(provider)))
    )
