"""Object provider traversal tests."""

from dependency_injector import providers


def test_traversal():
    provider = providers.Object("string")
    all_providers = list(provider.traverse())
    assert len(all_providers) == 0


def test_traversal_provider():
    another_provider = providers.Provider()
    provider = providers.Object(another_provider)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 1
    assert another_provider in all_providers


def test_traversal_provider_and_overriding():
    another_provider_1 = providers.Provider()
    another_provider_2 = providers.Provider()
    another_provider_3 = providers.Provider()

    provider = providers.Object(another_provider_1)

    provider.override(another_provider_2)
    provider.override(another_provider_3)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert another_provider_1 in all_providers
    assert another_provider_2 in all_providers
    assert another_provider_3 in all_providers
