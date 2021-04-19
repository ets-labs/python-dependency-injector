import unittest

from dependency_injector import providers

from .singleton_common import Example, _BaseSingletonTestCase


class ContextLocalSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.ContextLocalSingleton

    def test_repr(self):
        provider = providers.ContextLocalSingleton(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'ContextLocalSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))

    def test_reset(self):
        provider = providers.ContextLocalSingleton(Example)

        instance1 = provider()
        self.assertIsInstance(instance1, Example)

        provider.reset()

        instance2 = provider()
        self.assertIsInstance(instance2, Example)

        self.assertIsNot(instance1, instance2)

    def test_reset_clean(self):
        provider = providers.ContextLocalSingleton(Example)
        instance1 = provider()

        provider.reset()
        provider.reset()

        instance2 = provider()
        self.assertIsNot(instance1, instance2)
