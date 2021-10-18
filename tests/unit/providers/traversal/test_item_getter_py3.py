"""ItemGetter provider traversal tests."""

from dependency_injector import providers


def test_traverse():
    provider1 = providers.Provider()
    provided = provider1.provided
    provider = provided["item"]

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provided in all_providers


def test_traverse_overridden():
    provider1 = providers.Provider()
    provided = provider1.provided
    provider2 = providers.Provider()

    provider = provided["item"]
    provider.override(provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provided in all_providers
