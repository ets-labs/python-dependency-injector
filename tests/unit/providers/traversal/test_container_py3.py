"""Container provider traversal tests."""

from dependency_injector import containers, providers


def test_traverse():
    class Container(containers.DeclarativeContainer):
        provider1 = providers.Callable(list)
        provider2 = providers.Callable(dict)

    provider = providers.Container(Container)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 2
    assert {list, dict} == {provider.provides for provider in all_providers}


def test_traverse_overridden():
    class Container1(containers.DeclarativeContainer):
        provider1 = providers.Callable(list)
        provider2 = providers.Callable(dict)

    class Container2(containers.DeclarativeContainer):
        provider1 = providers.Callable(tuple)
        provider2 = providers.Callable(str)

    container2 = Container2()

    provider = providers.Container(Container1)
    provider.override(container2)

    all_providers = list(provider.traverse())

    assert len(all_providers) == 5
    assert {list, dict, tuple, str} == {
        provider.provides
        for provider in all_providers
        if isinstance(provider, providers.Callable)
    }
    assert provider.last_overriding in all_providers
    assert provider.last_overriding() is container2
