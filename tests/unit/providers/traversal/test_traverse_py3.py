"""Provider's traversal tests."""

from dependency_injector import providers


def test_traverse_cycled_graph():
    provider1 = providers.Provider()

    provider2 = providers.Provider()
    provider2.override(provider1)

    provider3 = providers.Provider()
    provider3.override(provider2)

    provider1.override(provider3)  # Cycle: provider3 -> provider2 -> provider1 -> provider3

    all_providers = list(providers.traverse(provider1))

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provider3 in all_providers


def test_traverse_types_filtering():
    provider1 = providers.Resource(dict)
    provider2 = providers.Resource(dict)
    provider3 = providers.Provider()

    provider = providers.Provider()

    provider.override(provider1)
    provider.override(provider2)
    provider.override(provider3)

    all_providers = list(providers.traverse(provider, types=[providers.Resource]))

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers
