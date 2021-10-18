"""CoroutineDelegate provider tests."""

from dependency_injector import providers, errors
from pytest import raises

from .common import example


def test_is_delegate():
    provider = providers.Coroutine(example)
    delegate = providers.CoroutineDelegate(provider)
    assert isinstance(delegate, providers.Delegate)


def test_init_with_not_coroutine():
    with raises(errors.Error):
        providers.CoroutineDelegate(providers.Object(object()))
