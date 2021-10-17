"""CallableDelegate provider tests."""

from dependency_injector import providers, errors
from pytest import raises

from .common import example


def test_is_delegate():
    provider = providers.Callable(example)
    delegate = providers.CallableDelegate(provider)
    assert isinstance(delegate, providers.Delegate)


def test_init_with_not_callable():
    with raises(errors.Error):
        providers.CallableDelegate(providers.Object(object()))
