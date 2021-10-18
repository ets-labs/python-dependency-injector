"""Provider traversal tests."""

from dependency_injector import providers


def test_traversal_overriding():
    provider1 = providers.Provider()
    provider2 = providers.Provider()
    provider3 = providers.Provider()

    provider = providers.Provider()

    provider.override(provider1)
    provider.override(provider2)
    provider.override(provider3)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provider3 in all_providers


def test_traversal_overriding_nested():
    provider1 = providers.Provider()

    provider2 = providers.Provider()
    provider2.override(provider1)

    provider3 = providers.Provider()
    provider3.override(provider2)

    provider = providers.Provider()
    provider.override(provider3)

    all_providers = list(provider.traverse())

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

    all_providers = list(provider.traverse(types=[providers.Resource]))

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers
