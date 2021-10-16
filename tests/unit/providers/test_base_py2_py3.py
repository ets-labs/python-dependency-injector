"""Dependency injector base providers unit tests."""

import unittest
import warnings

from dependency_injector import (
    containers,
    providers,
    errors,
)
from pytest import raises


class ProviderTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.Provider()

    def test_is_provider(self):
        assert providers.is_provider(self.provider) is True

    def test_call(self):
        with raises(NotImplementedError):
            self.provider()

    def test_delegate(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            delegate1 = self.provider.delegate()
            delegate2 = self.provider.delegate()

        assert isinstance(delegate1, providers.Delegate)
        assert delegate1() is self.provider

        assert isinstance(delegate2, providers.Delegate)
        assert delegate2() is self.provider

        assert delegate1 is not delegate2

    def test_provider(self):
        delegate1 = self.provider.provider

        assert isinstance(delegate1, providers.Delegate)
        assert delegate1() is self.provider

        delegate2 = self.provider.provider

        assert isinstance(delegate2, providers.Delegate)
        assert delegate2() is self.provider

        assert delegate1 is not delegate2

    def test_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)
        assert self.provider.overridden == (overriding_provider,)
        assert self.provider.last_overriding is overriding_provider

    def test_double_override(self):
        overriding_provider1 = providers.Object(1)
        overriding_provider2 = providers.Object(2)

        self.provider.override(overriding_provider1)
        overriding_provider1.override(overriding_provider2)

        assert self.provider() == overriding_provider2()

    def test_overriding_context(self):
        overriding_provider = providers.Provider()
        with self.provider.override(overriding_provider):
            assert self.provider.overridden == (overriding_provider,)
        assert self.provider.overridden == tuple()
        assert not self.provider.overridden

    def test_override_with_itself(self):
        with raises(errors.Error):
            self.provider.override(self.provider)

    def test_override_with_not_provider(self):
        obj = object()
        self.provider.override(obj)
        assert self.provider() is obj

    def test_reset_last_overriding(self):
        overriding_provider1 = providers.Provider()
        overriding_provider2 = providers.Provider()

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        assert self.provider.overridden[-1] is overriding_provider2
        assert self.provider.last_overriding is overriding_provider2

        self.provider.reset_last_overriding()
        assert self.provider.overridden[-1] is overriding_provider1
        assert self.provider.last_overriding is overriding_provider1

        self.provider.reset_last_overriding()
        assert self.provider.overridden == tuple()
        assert not self.provider.overridden
        assert self.provider.last_overriding is None

    def test_reset_last_overriding_of_not_overridden_provider(self):
        with raises(errors.Error):
            self.provider.reset_last_overriding()

    def test_reset_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)

        assert self.provider.overridden
        assert self.provider.overridden == (overriding_provider,)

        self.provider.reset_override()

        assert self.provider.overridden == tuple()

    def test_deepcopy(self):
        provider = providers.Provider()

        provider_copy = providers.deepcopy(provider)

        assert provider is not provider_copy
        assert isinstance(provider, providers.Provider)

    def test_deepcopy_from_memo(self):
        provider = providers.Provider()
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        assert provider_copy is provider_copy_memo

    def test_deepcopy_overridden(self):
        provider = providers.Provider()
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        assert provider is not provider_copy
        assert isinstance(provider, providers.Provider)

        assert overriding_provider is not overriding_provider_copy
        assert isinstance(overriding_provider_copy, providers.Provider)

    def test_repr(self):
        assert repr(self.provider) == (
            "<dependency_injector.providers."
            "Provider() at {0}>".format(hex(id(self.provider)))
        )


class DelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Provider()
        self.delegate = providers.Delegate(self.delegated)

    def test_is_provider(self):
        assert providers.is_provider(self.delegate) is True

    def test_init_optional_provides(self):
        provider = providers.Delegate()
        provider.set_provides(self.delegated)
        assert provider.provides is self.delegated
        assert provider() is self.delegated

    def test_set_provides_returns_self(self):
        provider = providers.Delegate()
        assert provider.set_provides(self.delegated) is provider

    def test_init_with_not_provider(self):
        with raises(errors.Error):
            providers.Delegate(object())

    def test_call(self):
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        assert delegated1 is self.delegated
        assert delegated2 is self.delegated

    def test_repr(self):
        assert repr(self.delegate) == (
            "<dependency_injector.providers."
            "Delegate({0}) at {1}>".format(repr(self.delegated), hex(id(self.delegate)))
        )


class DependencyTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.Dependency(instance_of=list)

    def test_init_optional(self):
        list_provider = providers.List(1, 2, 3)
        provider = providers.Dependency()
        provider.set_instance_of(list)
        provider.set_default(list_provider)

        assert provider.instance_of is list
        assert provider.default is list_provider
        assert provider() == [1, 2, 3]

    def test_set_instance_of_returns_self(self):
        provider = providers.Dependency()
        assert provider.set_instance_of(list) is provider

    def test_set_default_returns_self(self):
        provider = providers.Dependency()
        assert provider.set_default(providers.Provider()) is provider

    def test_init_with_not_class(self):
        with raises(TypeError):
            providers.Dependency(object())

    def test_with_abc(self):
        try:
            import collections.abc as collections_abc
        except ImportError:
            import collections as collections_abc

        provider = providers.Dependency(collections_abc.Mapping)
        provider.provided_by(providers.Factory(dict))

        assert isinstance(provider(), collections_abc.Mapping)
        assert isinstance(provider(), dict)

    def test_is_provider(self):
        assert providers.is_provider(self.provider) is True

    def test_provided_instance_provider(self):
        assert isinstance(self.provider.provided, providers.ProvidedInstance)

    def test_default(self):
        provider = providers.Dependency(instance_of=dict, default={"foo": "bar"})
        assert provider() == {"foo": "bar"}

    def test_default_attribute(self):
        provider = providers.Dependency(instance_of=dict, default={"foo": "bar"})
        assert provider.default() == {"foo": "bar"}

    def test_default_provider(self):
        provider = providers.Dependency(instance_of=dict, default=providers.Factory(dict, foo="bar"))
        assert provider.default() == {"foo": "bar"}

    def test_default_attribute_provider(self):
        default = providers.Factory(dict, foo="bar")
        provider = providers.Dependency(instance_of=dict, default=default)

        assert provider.default() == {"foo": "bar"}
        assert provider.default is default

    def test_is_defined(self):
        provider = providers.Dependency()
        assert provider.is_defined is False

    def test_is_defined_when_overridden(self):
        provider = providers.Dependency()
        provider.override("value")
        assert provider.is_defined is True

    def test_is_defined_with_default(self):
        provider = providers.Dependency(default="value")
        assert provider.is_defined is True

    def test_call_overridden(self):
        self.provider.provided_by(providers.Factory(list))
        assert isinstance(self.provider(), list)

    def test_call_overridden_but_not_instance_of(self):
        self.provider.provided_by(providers.Factory(dict))
        with raises(errors.Error):
            self.provider()

    def test_call_undefined(self):
        with raises(errors.Error, match="Dependency is not defined"):
            self.provider()

    def test_call_undefined_error_message_with_container_instance_parent(self):
        class UserService:
            def __init__(self, database):
                self.database = database

        class Container(containers.DeclarativeContainer):
            database = providers.Dependency()

            user_service = providers.Factory(
                UserService,
                database=database,  # <---- missing dependency
            )

        container = Container()

        with raises(errors.Error) as exception_info:
            container.user_service()
        assert str(exception_info.value) == "Dependency \"Container.database\" is not defined"

    def test_call_undefined_error_message_with_container_provider_parent_deep(self):
        class Database:
            pass

        class UserService:
            def __init__(self, db):
                self.db = db

        class Gateways(containers.DeclarativeContainer):
            database_client = providers.Singleton(Database)

        class Services(containers.DeclarativeContainer):
            gateways = providers.DependenciesContainer()

            user = providers.Factory(
                UserService,
                db=gateways.database_client,
            )

        class Container(containers.DeclarativeContainer):
            gateways = providers.Container(Gateways)

            services = providers.Container(
                Services,
                # gateways=gateways,  # <---- missing dependency
            )

        container = Container()

        with raises(errors.Error) as exception_info:
            container.services().user()
        assert str(exception_info.value) == "Dependency \"Container.services.gateways.database_client\" is not defined"

    def test_call_undefined_error_message_with_dependenciescontainer_provider_parent(self):
        class UserService:
            def __init__(self, db):
                self.db = db

        class Services(containers.DeclarativeContainer):
            gateways = providers.DependenciesContainer()

            user = providers.Factory(
                UserService,
                db=gateways.database_client,  # <---- missing dependency
            )

        services = Services()

        with raises(errors.Error) as exception_info:
            services.user()
        assert str(exception_info.value) == "Dependency \"Services.gateways.database_client\" is not defined"

    def test_assign_parent(self):
        parent = providers.DependenciesContainer()
        provider = providers.Dependency()

        provider.assign_parent(parent)

        assert provider.parent is parent

    def test_parent_name(self):
        container = containers.DynamicContainer()
        provider = providers.Dependency()
        container.name = provider
        assert provider.parent_name == "name"

    def test_parent_name_with_deep_parenting(self):
        provider = providers.Dependency()
        container = providers.DependenciesContainer(name=provider)
        _ = providers.DependenciesContainer(container=container)
        assert provider.parent_name == "container.name"

    def test_parent_name_is_none(self):
        provider = providers.DependenciesContainer()
        assert provider.parent_name is None

    def test_parent_deepcopy(self):
        container = containers.DynamicContainer()
        provider = providers.Dependency()
        container.name = provider

        copied = providers.deepcopy(container)

        assert container.name.parent is container
        assert copied.name.parent is copied

        assert container is not copied
        assert container.name is not copied.name
        assert container.name.parent is not copied.name.parent

    def test_forward_attr_to_default(self):
        default = providers.Configuration()

        provider = providers.Dependency(default=default)
        provider.from_dict({"foo": "bar"})

        assert default() == {"foo": "bar"}

    def test_forward_attr_to_overriding(self):
        overriding = providers.Configuration()

        provider = providers.Dependency()
        provider.override(overriding)
        provider.from_dict({"foo": "bar"})

        assert overriding() == {"foo": "bar"}

    def test_forward_attr_to_none(self):
        provider = providers.Dependency()
        with raises(AttributeError):
            provider.from_dict

    def test_deepcopy(self):
        provider = providers.Dependency(int)

        provider_copy = providers.deepcopy(provider)

        assert provider is not provider_copy
        assert isinstance(provider, providers.Dependency)

    def test_deepcopy_from_memo(self):
        provider = providers.Dependency(int)
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        assert provider_copy is provider_copy_memo

    def test_deepcopy_overridden(self):
        provider = providers.Dependency(int)
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        assert provider is not provider_copy
        assert isinstance(provider, providers.Dependency)

        assert overriding_provider is not overriding_provider_copy
        assert isinstance(overriding_provider_copy, providers.Provider)

    def test_deep_copy_default_object(self):
        default = {"foo": "bar"}
        provider = providers.Dependency(dict, default=default)

        provider_copy = providers.deepcopy(provider)

        assert provider_copy() is default
        assert provider_copy.default() is default

    def test_deep_copy_default_provider(self):
        bar = object()
        default = providers.Factory(dict, foo=providers.Object(bar))
        provider = providers.Dependency(dict, default=default)

        provider_copy = providers.deepcopy(provider)

        assert provider_copy() == {"foo": bar}
        assert provider_copy.default() == {"foo": bar}
        assert provider_copy()["foo"] is bar

    def test_with_container_default_object(self):
        default = {"foo": "bar"}

        class Container(containers.DeclarativeContainer):
            provider = providers.Dependency(dict, default=default)

        container = Container()

        assert container.provider() is default
        assert container.provider.default() is default

    def test_with_container_default_provider(self):
        bar = object()

        class Container(containers.DeclarativeContainer):
            provider = providers.Dependency(dict, default=providers.Factory(dict, foo=providers.Object(bar)))

        container = Container()

        assert container.provider() == {"foo": bar}
        assert container.provider.default() == {"foo": bar}
        assert container.provider()["foo"] is bar

    def test_with_container_default_provider_with_overriding(self):
        bar = object()
        baz = object()

        class Container(containers.DeclarativeContainer):
            provider = providers.Dependency(dict, default=providers.Factory(dict, foo=providers.Object(bar)))

        container = Container(provider=providers.Factory(dict, foo=providers.Object(baz)))

        assert container.provider() == {"foo": baz}
        assert container.provider.default() == {"foo": bar}
        assert container.provider()["foo"] is baz

    def test_repr(self):
        assert repr(self.provider) == (
            "<dependency_injector.providers."
            "Dependency({0}) at {1}>".format(repr(list), hex(id(self.provider)))
        )

    def test_repr_in_container(self):
        class Container(containers.DeclarativeContainer):
            dependency = providers.Dependency(instance_of=int)

        container = Container()

        assert repr(container.dependency) == (
            "<dependency_injector.providers."
            "Dependency({0}) at {1}, container name: \"Container.dependency\">".format(
                repr(int),
                hex(id(container.dependency)),
            )
        )


class ExternalDependencyTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.ExternalDependency(instance_of=list)

    def test_is_instance(self):
        assert isinstance(self.provider, providers.Dependency)


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
