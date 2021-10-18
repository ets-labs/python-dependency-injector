"""Dependency provider traversal tests."""

from dependency_injector import providers


def test_traversal():
    provider = providers.Dependency()
    all_providers = list(provider.traverse())
    assert len(all_providers) == 0


def test_traversal_default():
    another_provider = providers.Provider()
    provider = providers.Dependency(default=another_provider)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 1
    assert another_provider in all_providers


def test_traversal_overriding():
    provider1 = providers.Provider()

    provider2 = providers.Provider()
    provider2.override(provider1)

    provider = providers.Dependency()
    provider.override(provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers
