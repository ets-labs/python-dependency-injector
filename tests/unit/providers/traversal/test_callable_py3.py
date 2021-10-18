"""Callable provider traversal tests."""

from dependency_injector import providers


def test_traverse():
    provider = providers.Callable(dict)
    all_providers = list(provider.traverse())
    assert len(all_providers) == 0


def test_traverse_args():
    provider1 = providers.Object("bar")
    provider2 = providers.Object("baz")
    provider = providers.Callable(list, "foo", provider1, provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_kwargs():
    provider1 = providers.Object("bar")
    provider2 = providers.Object("baz")
    provider = providers.Callable(dict, foo="foo", bar=provider1, baz=provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_overridden():
    provider1 = providers.Object("bar")
    provider2 = providers.Object("baz")

    provider = providers.Callable(dict, "foo")
    provider.override(provider1)
    provider.override(provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_provides():
    provider1 = providers.Callable(list)
    provider2 = providers.Object("bar")
    provider3 = providers.Object("baz")

    provider = providers.Callable(provider1, provider2)
    provider.override(provider3)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provider3 in all_providers
