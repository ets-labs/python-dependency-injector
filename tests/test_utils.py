"""Dependency injector utils unittests."""

import unittest2 as unittest

from dependency_injector import utils
from dependency_injector import providers
from dependency_injector import errors


class IsProviderTests(unittest.TestCase):
    """`is_provider()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(utils.is_provider(providers.Provider()))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(utils.is_provider(providers.Provider))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(utils.is_provider('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(utils.is_provider(object()))

    def test_with_subclass_instance(self):
        """Test with subclass of provider instance."""
        class SomeProvider(providers.Provider):
            """Some provider for test."""

        self.assertTrue(utils.is_provider(SomeProvider()))

    def test_with_class_with_getattr(self):
        """Test with class that has __getattr__() method implementation."""
        class SomeClass(object):
            """Some test class with __getattr__() method implementation."""

            def __getattr__(self, _):
                """Test implementation that just returns False."""
                return False

        self.assertFalse(utils.is_provider(SomeClass()))


class EnsureIsProviderTests(unittest.TestCase):
    """`ensure_is_provider` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        provider = providers.Provider()
        self.assertIs(utils.ensure_is_provider(provider), provider)

    def test_with_class(self):
        """Test with class."""
        self.assertRaises(errors.Error,
                          utils.ensure_is_provider,
                          providers.Provider)

    def test_with_string(self):
        """Test with string."""
        self.assertRaises(errors.Error,
                          utils.ensure_is_provider,
                          'some_string')

    def test_with_object(self):
        """Test with object."""
        self.assertRaises(errors.Error, utils.ensure_is_provider, object())
