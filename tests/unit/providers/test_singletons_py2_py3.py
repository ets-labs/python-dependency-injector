"""Dependency injector singleton providers unit tests."""

import unittest

from dependency_injector import (
    providers,
    errors,
)

from .singleton_common import Example, _BaseSingletonTestCase


class SingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.Singleton

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Singleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.DelegatedSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class ThreadLocalSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.ThreadLocalSingleton

    def test_repr(self):
        provider = providers.ThreadLocalSingleton(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'ThreadLocalSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))

    def test_reset(self):
        provider = providers.ThreadLocalSingleton(Example)

        instance1 = provider()
        self.assertIsInstance(instance1, Example)

        provider.reset()

        instance2 = provider()
        self.assertIsInstance(instance2, Example)

        self.assertIsNot(instance1, instance2)

    def test_reset_clean(self):
        provider = providers.ThreadLocalSingleton(Example)
        instance1 = provider()

        provider.reset()
        provider.reset()

        instance2 = provider()
        self.assertIsNot(instance1, instance2)


class DelegatedThreadLocalSingletonTests(_BaseSingletonTestCase,
                                         unittest.TestCase):

    singleton_cls = providers.DelegatedThreadLocalSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedThreadLocalSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class ThreadSafeSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.ThreadSafeSingleton

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'ThreadSafeSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedThreadSafeSingletonTests(_BaseSingletonTestCase,
                                        unittest.TestCase):

    singleton_cls = providers.DelegatedThreadSafeSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedThreadSafeSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class AbstractSingletonTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.AbstractSingleton(Example),
                              providers.BaseSingleton)

    def test_call_overridden_by_singleton(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.Singleton(Example))

        self.assertIsInstance(provider(), Example)

    def test_call_overridden_by_delegated_singleton(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.DelegatedSingleton(Example))

        self.assertIsInstance(provider(), Example)

    def test_call_not_overridden(self):
        provider = providers.AbstractSingleton(object)

        with self.assertRaises(errors.Error):
            provider()

    def test_reset_overridden(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.Singleton(Example))

        instance1 = provider()

        provider.reset()

        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_reset_not_overridden(self):
        provider = providers.AbstractSingleton(object)

        with self.assertRaises(errors.Error):
            provider.reset()

    def test_override_by_not_singleton(self):
        provider = providers.AbstractSingleton(object)

        with self.assertRaises(errors.Error):
            provider.override(providers.Factory(object))

    def test_repr(self):
        provider = providers.AbstractSingleton(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'AbstractSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class SingletonDelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Singleton(Example)
        self.delegate = providers.SingletonDelegate(self.delegated)

    def test_is_delegate(self):
        self.assertIsInstance(self.delegate, providers.Delegate)

    def test_init_with_not_singleton(self):
        self.assertRaises(errors.Error,
                          providers.SingletonDelegate,
                          providers.Object(object()))
