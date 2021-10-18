"""Delegated singleton provider tests."""

from dependency_injector import providers
from pytest import fixture

from .common import Example


PROVIDER_CLASSES = [
    providers.DelegatedSingleton,
    providers.DelegatedThreadLocalSingleton,
    providers.DelegatedThreadSafeSingleton,
]


@fixture(params=PROVIDER_CLASSES)
def singleton_cls(request):
    return request.param


@fixture
def provider(singleton_cls):
    return singleton_cls(Example)


def test_is_delegated_provider(provider):
    assert providers.is_delegated(provider) is True
