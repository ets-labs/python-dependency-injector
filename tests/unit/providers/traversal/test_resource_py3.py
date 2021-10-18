"""Resource provider traversal tests."""

from dependency_injector import providers


def test_traverse():
    provider = providers.Resource(dict)
    all_providers = list(provider.traverse())
    assert len(all_providers) == 0


def test_traverse_args():
    provider1 = providers.Object("bar")
    provider2 = providers.Object("baz")
    provider = providers.Resource(list, "foo", provider1, provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_kwargs():
    provider1 = providers.Object("bar")
    provider2 = providers.Object("baz")
    provider = providers.Resource(dict, foo="foo", bar=provider1, baz=provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_overridden():
    provider1 = providers.Resource(list)
    provider2 = providers.Resource(tuple)

    provider = providers.Resource(dict, "foo")
    provider.override(provider1)
    provider.override(provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_provides():
    provider1 = providers.Callable(list)

    provider = providers.Resource(provider1)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 1
    assert provider1 in all_providers

