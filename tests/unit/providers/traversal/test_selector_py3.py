"""Selector provider traversal tests."""

from dependency_injector import providers


def test_traverse():
    switch = lambda: "provider1"
    provider1 = providers.Callable(list)
    provider2 = providers.Callable(dict)

    provider = providers.Selector(
        switch,
        provider1=provider1,
        provider2=provider2,
    )

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_switch():
    switch = providers.Callable(lambda: "provider1")
    provider1 = providers.Callable(list)
    provider2 = providers.Callable(dict)

    provider = providers.Selector(
        switch,
        provider1=provider1,
        provider2=provider2,
    )

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert switch in all_providers
    assert provider1 in all_providers
    assert provider2 in all_providers


def test_traverse_overridden():
    provider1 = providers.Callable(list)
    provider2 = providers.Callable(dict)
    selector1 = providers.Selector(lambda: "provider1", provider1=provider1)

    provider = providers.Selector(
        lambda: "provider2",
        provider2=provider2,
    )
    provider.override(selector1)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert selector1 in all_providers
