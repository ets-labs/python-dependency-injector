"""Dependency injector base providers unit tests."""

import unittest

from dependency_injector import (
    containers,
    providers,
    errors,
)
from pytest import raises


class DependenciesContainerTests(unittest.TestCase):

    class Container(containers.DeclarativeContainer):

        dependency = providers.Provider()

    def setUp(self):
        self.provider = providers.DependenciesContainer()
        self.container = self.Container()

    def test_getattr(self):
        has_dependency = hasattr(self.provider, "dependency")
        dependency = self.provider.dependency

        assert isinstance(dependency, providers.Dependency)
        assert dependency is self.provider.dependency
        assert has_dependency is True
        assert dependency.last_overriding is None

    def test_getattr_with_container(self):
        self.provider.override(self.container)

        dependency = self.provider.dependency

        assert dependency.overridden == (self.container.dependency,)
        assert dependency.last_overriding is self.container.dependency

    def test_providers(self):
        dependency1 = self.provider.dependency1
        dependency2 = self.provider.dependency2
        assert self.provider.providers == {"dependency1": dependency1, "dependency2": dependency2}

    def test_override(self):
        dependency = self.provider.dependency
        self.provider.override(self.container)

        assert dependency.overridden == (self.container.dependency,)
        assert dependency.last_overriding is self.container.dependency

    def test_reset_last_overriding(self):
        dependency = self.provider.dependency
        self.provider.override(self.container)
        self.provider.reset_last_overriding()

        assert dependency.last_overriding is None
        assert dependency.last_overriding is None

    def test_reset_override(self):
        dependency = self.provider.dependency
        self.provider.override(self.container)
        self.provider.reset_override()

        assert dependency.overridden == tuple()
        assert not dependency.overridden

    def test_assign_parent(self):
        parent = providers.DependenciesContainer()
        provider = providers.DependenciesContainer()

        provider.assign_parent(parent)

        assert provider.parent is parent

    def test_parent_name(self):
        container = containers.DynamicContainer()
        provider = providers.DependenciesContainer()
        container.name = provider
        assert provider.parent_name == "name"

    def test_parent_name_with_deep_parenting(self):
        provider = providers.DependenciesContainer()
        container = providers.DependenciesContainer(name=provider)
        _ = providers.DependenciesContainer(container=container)
        assert provider.parent_name == "container.name"

    def test_parent_name_is_none(self):
        provider = providers.DependenciesContainer()
        assert provider.parent_name is None

    def test_parent_deepcopy(self):
        container = containers.DynamicContainer()
        provider = providers.DependenciesContainer()
        container.name = provider

        copied = providers.deepcopy(container)

        assert container.name.parent is container
        assert copied.name.parent is copied

        assert container is not copied
        assert container.name is not copied.name
        assert container.name.parent is not copied.name.parent

    def test_parent_set_on__getattr__(self):
        provider = providers.DependenciesContainer()
        assert isinstance(provider.name, providers.Dependency)
        assert provider.name.parent is provider

    def test_parent_set_on__init__(self):
        provider = providers.Dependency()
        container = providers.DependenciesContainer(name=provider)
        assert container.name is provider
        assert container.name.parent is container

    def test_resolve_provider_name(self):
        container = providers.DependenciesContainer()
        assert container.resolve_provider_name(container.name) == "name"

    def test_resolve_provider_name_no_provider(self):
        container = providers.DependenciesContainer()
        with raises(errors.Error):
            container.resolve_provider_name(providers.Provider())
