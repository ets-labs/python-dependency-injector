"""Dependency injector static providers unit tests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    errors,
)


class ObjectProviderTests(unittest.TestCase):

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.Object(object())))

    def test_call_object_provider(self):
        obj = object()
        self.assertIs(providers.Object(obj)(), obj)

    def test_call_overridden_object_provider(self):
        obj1 = object()
        obj2 = object()
        provider = providers.Object(obj1)
        provider.override(providers.Object(obj2))
        self.assertIs(provider(), obj2)

    def test_repr(self):
        some_object = object()
        provider = providers.Object(some_object)
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.static.'
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
                         '<dependency_injector.providers.static.'
                         'Delegate({0}) at {1}>'.format(
                             repr(self.delegated),
                             hex(id(self.delegate))))


class ExternalDependencyTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.ExternalDependency(instance_of=list)

    def test_init_with_not_class(self):
        self.assertRaises(TypeError, providers.ExternalDependency, object())

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.provider))

    def test_call_overridden(self):
        self.provider.provided_by(providers.Factory(list))
        self.assertIsInstance(self.provider(), list)

    def test_call_overridden_but_not_instance_of(self):
        self.provider.provided_by(providers.Factory(dict))
        self.assertRaises(errors.Error, self.provider)

    def test_call_not_overridden(self):
        self.assertRaises(errors.Error, self.provider)

    def test_repr(self):
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.static.'
                         'ExternalDependency({0}) at {1}>'.format(
                             repr(list),
                             hex(id(self.provider))))
