"""DependencyContainer provider tests."""

from dependency_injector import containers, providers, errors
from pytest import fixture, raises


class Container(containers.DeclarativeContainer):

    dependency = providers.Provider()


@fixture
def provider():
    return providers.DependenciesContainer()


@fixture
def container():
    return Container()


def test_getattr(provider):
    has_dependency = hasattr(provider, "dependency")
    dependency = provider.dependency

    assert isinstance(dependency, providers.Dependency)
    assert dependency is provider.dependency
    assert has_dependency is True
    assert dependency.last_overriding is None


def test_getattr_with_container(provider, container):
    provider.override(container)

    dependency = provider.dependency

    assert dependency.overridden == (container.dependency,)
    assert dependency.last_overriding is container.dependency


def test_providers(provider):
    dependency1 = provider.dependency1
    dependency2 = provider.dependency2
    assert provider.providers == {"dependency1": dependency1, "dependency2": dependency2}


def test_override(provider, container):
    dependency = provider.dependency
    provider.override(container)

    assert dependency.overridden == (container.dependency,)
    assert dependency.last_overriding is container.dependency


def test_reset_last_overriding(provider, container):
    dependency = provider.dependency
    provider.override(container)
    provider.reset_last_overriding()

    assert dependency.last_overriding is None
    assert dependency.last_overriding is None


def test_reset_override(provider, container):
    dependency = provider.dependency
    provider.override(container)
    provider.reset_override()

    assert dependency.overridden == tuple()
    assert not dependency.overridden


def test_assign_parent(provider):
    parent = providers.DependenciesContainer()
    provider.assign_parent(parent)
    assert provider.parent is parent


def test_parent_name(provider):
    container = containers.DynamicContainer()
    container.name = provider
    assert provider.parent_name == "name"


def test_parent_name_with_deep_parenting(provider):
    container = providers.DependenciesContainer(name=provider)
    _ = providers.DependenciesContainer(container=container)
    assert provider.parent_name == "container.name"


def test_parent_name_is_none(provider):
    assert provider.parent_name is None


def test_parent_deepcopy(provider, container):
    container.name = provider
    copied = providers.deepcopy(container)

    assert container.name.parent is container
    assert copied.name.parent is copied

    assert container is not copied
    assert container.name is not copied.name
    assert container.name.parent is not copied.name.parent


def test_parent_set_on__getattr__(provider):
    assert isinstance(provider.name, providers.Dependency)
    assert provider.name.parent is provider


def test_parent_set_on__init__():
    provider = providers.Dependency()
    container = providers.DependenciesContainer(name=provider)
    assert container.name is provider
    assert container.name.parent is container


def test_resolve_provider_name(provider):
    assert provider.resolve_provider_name(provider.name) == "name"


def test_resolve_provider_name_no_provider(provider):
    with raises(errors.Error):
        provider.resolve_provider_name(providers.Provider())
