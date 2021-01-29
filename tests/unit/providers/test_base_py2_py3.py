"""Dependency injector base providers unit tests."""

import unittest2 as unittest

from dependency_injector import (
    containers,
    providers,
    errors,
)


class ProviderTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.Provider()

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.provider))

    def test_call(self):
        self.assertRaises(NotImplementedError, self.provider.__call__)

    def test_delegate(self):
        delegate1 = self.provider.delegate()

        self.assertIsInstance(delegate1, providers.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, providers.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_provider(self):
        delegate1 = self.provider.provider

        self.assertIsInstance(delegate1, providers.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.provider

        self.assertIsInstance(delegate2, providers.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)
        self.assertTrue(self.provider.overridden)
        self.assertIs(self.provider.last_overriding, overriding_provider)

    def test_double_override(self):
        overriding_provider1 = providers.Object(1)
        overriding_provider2 = providers.Object(2)

        self.provider.override(overriding_provider1)
        overriding_provider1.override(overriding_provider2)

        self.assertEqual(self.provider(), overriding_provider2())

    def test_overriding_context(self):
        overriding_provider = providers.Provider()
        with self.provider.override(overriding_provider):
            self.assertTrue(self.provider.overridden)
        self.assertFalse(self.provider.overridden)

    def test_override_with_itself(self):
        self.assertRaises(errors.Error, self.provider.override, self.provider)

    def test_override_with_not_provider(self):
        obj = object()
        self.provider.override(obj)
        self.assertIs(self.provider(), obj)

    def test_reset_last_overriding(self):
        overriding_provider1 = providers.Provider()
        overriding_provider2 = providers.Provider()

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        self.assertIs(self.provider.overridden[-1], overriding_provider2)
        self.assertIs(self.provider.last_overriding, overriding_provider2)

        self.provider.reset_last_overriding()
        self.assertIs(self.provider.overridden[-1], overriding_provider1)
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.reset_last_overriding()
        self.assertFalse(self.provider.overridden)
        self.assertIsNone(self.provider.last_overriding)

    def test_reset_last_overriding_of_not_overridden_provider(self):
        self.assertRaises(errors.Error, self.provider.reset_last_overriding)

    def test_reset_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)

        self.assertTrue(self.provider.overridden)
        self.assertEqual(self.provider.overridden, (overriding_provider,))

        self.provider.reset_override()

        self.assertEqual(self.provider.overridden, tuple())

    def test_deepcopy(self):
        provider = providers.Provider()

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Provider)

    def test_deepcopy_from_memo(self):
        provider = providers.Provider()
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Provider()
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Provider)

        self.assertIsNot(overriding_provider, overriding_provider_copy)
        self.assertIsInstance(overriding_provider_copy, providers.Provider)

    def test_repr(self):
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.'
                         'Provider() at {0}>'.format(hex(id(self.provider))))


class ObjectProviderTests(unittest.TestCase):

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.Object(object())))

    def test_provided_instance_provider(self):
        provider = providers.Object(object())
        self.assertIsInstance(provider.provided, providers.ProvidedInstance)

    def test_call_object_provider(self):
        obj = object()
        self.assertIs(providers.Object(obj)(), obj)

    def test_call_overridden_object_provider(self):
        obj1 = object()
        obj2 = object()
        provider = providers.Object(obj1)
        provider.override(providers.Object(obj2))
        self.assertIs(provider(), obj2)

    def test_deepcopy(self):
        provider = providers.Object(1)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Object)

    def test_deepcopy_from_memo(self):
        provider = providers.Object(1)
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Object(1)
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Object)

        self.assertIsNot(overriding_provider, overriding_provider_copy)
        self.assertIsInstance(overriding_provider_copy, providers.Provider)

    def test_deepcopy_doesnt_copy_provided_object(self):
        # Fixes bug #231
        # Details: https://github.com/ets-labs/python-dependency-injector/issues/231
        some_object = object()
        provider = providers.Object(some_object)

        provider_copy = providers.deepcopy(provider)

        self.assertIs(provider(), some_object)
        self.assertIs(provider_copy(), some_object)

    def test_repr(self):
        some_object = object()
        provider = providers.Object(some_object)
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Object({0}) at {1}>'.format(
                             repr(some_object),
                             hex(id(provider))))


class DelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Provider()
        self.delegate = providers.Delegate(self.delegated)

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.delegate))

    def test_init_with_not_provider(self):
        self.assertRaises(errors.Error, providers.Delegate, object())

    def test_call(self):
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        self.assertIs(delegated1, self.delegated)
        self.assertIs(delegated2, self.delegated)

    def test_repr(self):
        self.assertEqual(repr(self.delegate),
                         '<dependency_injector.providers.'
                         'Delegate({0}) at {1}>'.format(
                             repr(self.delegated),
                             hex(id(self.delegate))))


class DependencyTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.Dependency(instance_of=list)

    def test_init_with_not_class(self):
        self.assertRaises(TypeError, providers.Dependency, object())

    def test_with_abc(self):
        try:
            import collections.abc as collections_abc
        except ImportError:
            import collections as collections_abc

        provider = providers.Dependency(collections_abc.Mapping)
        provider.provided_by(providers.Factory(dict))

        self.assertIsInstance(provider(), collections_abc.Mapping)
        self.assertIsInstance(provider(), dict)

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.provider))

    def test_provided_instance_provider(self):
        self.assertIsInstance(self.provider.provided, providers.ProvidedInstance)

    def test_default(self):
        provider = providers.Dependency(instance_of=dict, default={'foo': 'bar'})
        self.assertEqual(provider(), {'foo': 'bar'})

    def test_default_attribute(self):
        provider = providers.Dependency(instance_of=dict, default={'foo': 'bar'})
        self.assertEqual(provider.default(), {'foo': 'bar'})

    def test_default_provider(self):
        provider = providers.Dependency(instance_of=dict, default=providers.Factory(dict, foo='bar'))
        self.assertEqual(provider.default(), {'foo': 'bar'})

    def test_default_attribute_provider(self):
        default = providers.Factory(dict, foo='bar')
        provider = providers.Dependency(instance_of=dict, default=default)

        self.assertEqual(provider.default(), {'foo': 'bar'})
        self.assertIs(provider.default, default)

    def test_call_overridden(self):
        self.provider.provided_by(providers.Factory(list))
        self.assertIsInstance(self.provider(), list)

    def test_call_overridden_but_not_instance_of(self):
        self.provider.provided_by(providers.Factory(dict))
        self.assertRaises(errors.Error, self.provider)

    def test_call_not_overridden(self):
        self.assertRaises(errors.Error, self.provider)

    def test_deepcopy(self):
        provider = providers.Dependency(int)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Dependency)

    def test_deepcopy_from_memo(self):
        provider = providers.Dependency(int)
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Dependency(int)
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Dependency)

        self.assertIsNot(overriding_provider, overriding_provider_copy)
        self.assertIsInstance(overriding_provider_copy, providers.Provider)

    def test_deep_copy_default_object(self):
        default = {'foo': 'bar'}
        provider = providers.Dependency(dict, default=default)

        provider_copy = providers.deepcopy(provider)

        self.assertIs(provider_copy(), default)
        self.assertIs(provider_copy.default(), default)

    def test_deep_copy_default_provider(self):
        bar = object()
        default = providers.Factory(dict, foo=providers.Object(bar))
        provider = providers.Dependency(dict, default=default)

        provider_copy = providers.deepcopy(provider)

        self.assertEqual(provider_copy(), {'foo': bar})
        self.assertEqual(provider_copy.default(), {'foo': bar})
        self.assertIs(provider_copy()['foo'], bar)

    def test_with_container_default_object(self):
        default = {'foo': 'bar'}

        class Container(containers.DeclarativeContainer):
            provider = providers.Dependency(dict, default=default)

        container = Container()

        self.assertIs(container.provider(), default)
        self.assertIs(container.provider.default(), default)

    def test_with_container_default_provider(self):
        bar = object()

        class Container(containers.DeclarativeContainer):
            provider = providers.Dependency(dict, default=providers.Factory(dict, foo=providers.Object(bar)))

        container = Container()

        self.assertEqual(container.provider(), {'foo': bar})
        self.assertEqual(container.provider.default(), {'foo': bar})
        self.assertIs(container.provider()['foo'], bar)

    def test_with_container_default_provider_with_overriding(self):
        bar = object()
        baz = object()

        class Container(containers.DeclarativeContainer):
            provider = providers.Dependency(dict, default=providers.Factory(dict, foo=providers.Object(bar)))

        container = Container(provider=providers.Factory(dict, foo=providers.Object(baz)))

        self.assertEqual(container.provider(), {'foo': baz})
        self.assertEqual(container.provider.default(), {'foo': bar})
        self.assertIs(container.provider()['foo'], baz)

    def test_repr(self):
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.'
                         'Dependency({0}) at {1}>'.format(
                             repr(list),
                             hex(id(self.provider))))


class ExternalDependencyTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.ExternalDependency(instance_of=list)

    def test_is_instance(self):
        self.assertIsInstance(self.provider, providers.Dependency)


class DependenciesContainerTests(unittest.TestCase):

    class Container(containers.DeclarativeContainer):

        dependency = providers.Provider()

    def setUp(self):
        self.provider = providers.DependenciesContainer()
        self.container = self.Container()

    def test_getattr(self):
        has_dependency = hasattr(self.provider, 'dependency')
        dependency = self.provider.dependency

        self.assertIsInstance(dependency, providers.Dependency)
        self.assertIs(dependency, self.provider.dependency)
        self.assertTrue(has_dependency)
        self.assertIsNone(dependency.last_overriding)

    def test_getattr_with_container(self):
        self.provider.override(self.container)

        dependency = self.provider.dependency

        self.assertTrue(dependency.overridden)
        self.assertIs(dependency.last_overriding, self.container.dependency)

    def test_providers(self):
        dependency1 = self.provider.dependency1
        dependency2 = self.provider.dependency2
        self.assertEqual(self.provider.providers, {'dependency1': dependency1,
                                                   'dependency2': dependency2})

    def test_override(self):
        dependency = self.provider.dependency
        self.provider.override(self.container)

        self.assertTrue(dependency.overridden)
        self.assertIs(dependency.last_overriding, self.container.dependency)

    def test_reset_last_overriding(self):
        dependency = self.provider.dependency
        self.provider.override(self.container)
        self.provider.reset_last_overriding()

        self.assertIsNone(dependency.last_overriding)
        self.assertIsNone(dependency.last_overriding)

    def test_reset_override(self):
        dependency = self.provider.dependency
        self.provider.override(self.container)
        self.provider.reset_override()

        self.assertFalse(dependency.overridden)
        self.assertFalse(dependency.overridden)
