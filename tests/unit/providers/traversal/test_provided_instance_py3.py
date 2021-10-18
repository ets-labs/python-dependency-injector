"""ProvidedInstance provider traversal tests."""

from dependency_injector import providers


def test_traverse():
    provider1 = providers.Provider()
    provider = provider1.provided

    all_providers = list(provider.traverse())

    assert len(all_providers) == 1
    assert provider1 in all_providers


def test_traverse_overridden():
    provider1 = providers.Provider()
    provider2 = providers.Provider()

    provider = provider1.provided
    provider.override(provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers
