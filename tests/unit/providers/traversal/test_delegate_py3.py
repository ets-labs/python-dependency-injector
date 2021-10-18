"""Delegate provider traversal tests."""

from dependency_injector import providers


def test_traversal_provider():
    another_provider = providers.Provider()
    provider = providers.Delegate(another_provider)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 1
    assert another_provider in all_providers


def test_traversal_provider_and_overriding():
    provider1 = providers.Provider()
    provider2 = providers.Provider()

    provider3 = providers.Provider()
    provider3.override(provider2)

    provider = providers.Delegate(provider1)

    provider.override(provider3)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provider3 in all_providers
