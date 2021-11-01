"""FactoryAggregate provider traversal tests."""

from dependency_injector import providers


def test_traverse():
    factory1 = providers.Factory(dict)
    factory2 = providers.Factory(list)
    provider = providers.FactoryAggregate(factory1=factory1, factory2=factory2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert factory1 in all_providers
    assert factory2 in all_providers
