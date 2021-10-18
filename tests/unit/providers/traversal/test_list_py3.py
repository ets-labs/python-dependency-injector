"""List provider traversal tests."""

from dependency_injector import providers


def test_traverse_args():
    provider1 = providers.Object("bar")
    provider2 = providers.Object("baz")
    provider = providers.List("foo", provider1, provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_overridden():
    provider1 = providers.Object("bar")
    provider2 = providers.Object("baz")
    provider3 = providers.List(provider1, provider2)

    provider = providers.List("foo")
    provider.override(provider3)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provider3 in all_providers
