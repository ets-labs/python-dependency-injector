"""Dependency injector provider utils unit tests."""

import unittest

from dependency_injector import (
    providers,
    errors,
)


class IsProviderTests(unittest.TestCase):

    def test_with_instance(self):
        self.assertTrue(providers.is_provider(providers.Provider()))

    def test_with_class(self):
        self.assertFalse(providers.is_provider(providers.Provider))

    def test_with_string(self):
        self.assertFalse(providers.is_provider('some_string'))

    def test_with_object(self):
        self.assertFalse(providers.is_provider(object()))

    def test_with_subclass_instance(self):
        class SomeProvider(providers.Provider):
            pass

        self.assertTrue(providers.is_provider(SomeProvider()))

    def test_with_class_with_getattr(self):
        class SomeClass(object):
            def __getattr__(self, _):
                return False

        self.assertFalse(providers.is_provider(SomeClass()))


class EnsureIsProviderTests(unittest.TestCase):

    def test_with_instance(self):
        provider = providers.Provider()
        self.assertIs(providers.ensure_is_provider(provider), provider)

    def test_with_class(self):
        self.assertRaises(errors.Error,
                          providers.ensure_is_provider,
                          providers.Provider)

    def test_with_string(self):
        self.assertRaises(errors.Error,
                          providers.ensure_is_provider,
                          'some_string')

    def test_with_object(self):
        self.assertRaises(errors.Error, providers.ensure_is_provider, object())
