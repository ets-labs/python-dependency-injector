"""Provider utils tests."""

from dependency_injector import providers, errors
from pytest import raises


def test_with_instance():
    provider = providers.Provider()
    assert providers.ensure_is_provider(provider), provider


def test_with_class():
    with raises(errors.Error):
        providers.ensure_is_provider(providers.Provider)


def test_with_string():
    with raises(errors.Error):
        providers.ensure_is_provider("some_string")


def test_with_object():
    with raises(errors.Error):
        providers.ensure_is_provider(object())
