"""Dependency injector config providers unit tests."""

import unittest2 as unittest

from dependency_injector import providers


class ConfigTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

    def tearDown(self):
        del self.config

    def test_providers_are_providers(self):
        self.assertTrue(providers.is_provider(self.config.a))
        self.assertTrue(providers.is_provider(self.config.a.b))
        self.assertTrue(providers.is_provider(self.config.a.b.c))
        self.assertTrue(providers.is_provider(self.config.a.b.d))

    def test_providers_are_not_delegates(self):
        self.assertFalse(providers.is_delegated(self.config.a))
        self.assertFalse(providers.is_delegated(self.config.a.b))
        self.assertFalse(providers.is_delegated(self.config.a.b.c))
        self.assertFalse(providers.is_delegated(self.config.a.b.d))

    def test_providers_identity(self):
        self.assertIs(self.config.a, self.config.a)
        self.assertIs(self.config.a.b, self.config.a.b)
        self.assertIs(self.config.a.b.c, self.config.a.b.c)
        self.assertIs(self.config.a.b.d, self.config.a.b.d)

    def test_get_name(self):
        self.assertEqual(self.config.a.b.c.get_name(), 'config.a.b.c')

    def test_providers_value_setting(self):
        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.config.update({'a': {'b': {'c': 1, 'd': 2}}})

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_with_already_set_value(self):
        self.config.update({'a': {'b': {'c': 1, 'd': 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_value_override(self):
        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.config.override({'a': {'b': {'c': 1, 'd': 2}}})

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_with_already_overridden_value(self):
        self.config.override({'a': {'b': {'c': 1, 'd': 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_with_default_value(self):
        self.config = providers.Configuration(
            name='config', default={'a': {'b': {'c': 1, 'd': 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_with_default_value_overriding(self):
        self.config = providers.Configuration(
            name='config', default={'a': {'b': {'c': 1, 'd': 2}}})

        self.assertEqual(self.config.a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(self.config.a.b(), {'c': 1, 'd': 2})
        self.assertEqual(self.config.a.b.c(), 1)
        self.assertEqual(self.config.a.b.d(), 2)

        self.config.override({'a': {'b': {'c': 3, 'd': 4}}})
        self.assertEqual(self.config.a(), {'b': {'c': 3, 'd': 4}})
        self.assertEqual(self.config.a.b(), {'c': 3, 'd': 4})
        self.assertEqual(self.config.a.b.c(), 3)
        self.assertEqual(self.config.a.b.d(), 4)

        self.config.reset_override()
        self.assertEqual(self.config.a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(self.config.a.b(), {'c': 1, 'd': 2})
        self.assertEqual(self.config.a.b.c(), 1)
        self.assertEqual(self.config.a.b.d(), 2)

    def test_value_of_undefined_option(self):
        self.assertIsNone(self.config.a())

    def test_getting_of_special_attributes(self):
        with self.assertRaises(AttributeError):
            self.config.__name__

    def test_getting_of_special_attributes_from_child(self):
        a = self.config.a
        with self.assertRaises(AttributeError):
            a.__name__

    def test_deepcopy(self):
        provider = providers.Configuration('config')
        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Configuration)

    def test_deepcopy_from_memo(self):
        provider = providers.Configuration('config')
        provider_copy_memo = providers.Configuration('config')

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Configuration('config')
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Configuration)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_repr(self):
        self.assertEqual(repr(self.config),
                         '<dependency_injector.providers.'
                         'Configuration({0}) at {1}>'.format(
                             repr('config'),
                             hex(id(self.config))))

    def test_repr_child(self):
        self.assertEqual(repr(self.config.a.b.c),
                         '<dependency_injector.providers.'
                         'Configuration({0}) at {1}>'.format(
                             repr('config.a.b.c'),
                             hex(id(self.config.a.b.c))))
