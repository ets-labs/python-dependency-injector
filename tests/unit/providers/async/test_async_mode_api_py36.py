"""Tests for provider async mode API."""

from dependency_injector import providers
from pytest import fixture


@fixture
def provider():
    return providers.Provider()


def test_default_mode(provider: providers.Provider):
    assert provider.is_async_mode_enabled() is False
    assert provider.is_async_mode_disabled() is False
    assert provider.is_async_mode_undefined() is True


def test_enable(provider: providers.Provider):
    provider.enable_async_mode()

    assert provider.is_async_mode_enabled() is True
    assert provider.is_async_mode_disabled() is False
    assert provider.is_async_mode_undefined() is False


def test_disable(provider: providers.Provider):
    provider.disable_async_mode()

    assert provider.is_async_mode_enabled() is False
    assert provider.is_async_mode_disabled() is True
    assert provider.is_async_mode_undefined() is False


def test_reset(provider: providers.Provider):
    provider.enable_async_mode()

    assert provider.is_async_mode_enabled() is True
    assert provider.is_async_mode_disabled() is False
    assert provider.is_async_mode_undefined() is False

    provider.reset_async_mode()

    assert provider.is_async_mode_enabled() is False
    assert provider.is_async_mode_disabled() is False
    assert provider.is_async_mode_undefined() is True
