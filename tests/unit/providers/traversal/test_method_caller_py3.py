"""MethodCaller provider traversal tests."""

from dependency_injector import providers


def test_traverse():
    provider1 = providers.Provider()
    provided = provider1.provided
    method = provided.method
    provider = method.call()

    all_providers = list(provider.traverse())

    assert len(all_providers) == 3
    assert provider1 in all_providers
    assert provided in all_providers
    assert method in all_providers


def test_traverse_args():
    provider1 = providers.Provider()
    provided = provider1.provided
    method = provided.method
    provider2 = providers.Provider()
    provider = method.call("foo", provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 4
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provided in all_providers
    assert method in all_providers


def test_traverse_kwargs():
    provider1 = providers.Provider()
    provided = provider1.provided
    method = provided.method
    provider2 = providers.Provider()
    provider = method.call(foo="foo", bar=provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 4
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provided in all_providers
    assert method in all_providers


def test_traverse_overridden():
    provider1 = providers.Provider()
    provided = provider1.provided
    method = provided.method
    provider2 = providers.Provider()

    provider = method.call()
    provider.override(provider2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 4
    assert provider1 in all_providers
    assert provider2 in all_providers
    assert provided in all_providers
    assert method in all_providers
