"""Dependency injector utils unittests."""

import unittest2 as unittest

from dependency_injector import utils
from dependency_injector import providers
from dependency_injector import injections
from dependency_injector import catalogs
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


class IsInjectionTests(unittest.TestCase):
    """`is_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(utils.is_injection(injections.Injection('value')))

    def test_with_subclass_instances(self):
        """Test with subclass instances."""
        self.assertTrue(utils.is_injection(injections.Arg('value')))
        self.assertTrue(utils.is_injection(injections.KwArg('name',
                                                            'value')))
        self.assertTrue(utils.is_injection(injections.Attribute('name',
                                                                'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(utils.is_injection(injections.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(utils.is_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(utils.is_injection(object()))


class EnsureIsInjectionTests(unittest.TestCase):
    """`ensure_is_injection` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        injection = injections.Injection('value')
        self.assertIs(utils.ensure_is_injection(injection), injection)

    def test_with_class(self):
        """Test with class."""
        self.assertRaises(errors.Error,
                          utils.ensure_is_injection,
                          injections.Injection)

    def test_with_string(self):
        """Test with string."""
        self.assertRaises(errors.Error,
                          utils.ensure_is_injection,
                          'some_string')

    def test_with_object(self):
        """Test with object."""
        self.assertRaises(errors.Error,
                          utils.ensure_is_injection,
                          object())


class IsArgInjectionTests(unittest.TestCase):
    """`is_arg_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(utils.is_arg_injection(injections.Arg('value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(utils.is_arg_injection(injections.Arg))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(utils.is_arg_injection(injections.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(utils.is_arg_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(utils.is_arg_injection(object()))


class IsKwArgInjectionTests(unittest.TestCase):
    """`is_kwarg_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(utils.is_kwarg_injection(injections.KwArg('name',
                                                                  'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(utils.is_kwarg_injection(injections.KwArg))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(utils.is_kwarg_injection(injections.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(utils.is_kwarg_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(utils.is_kwarg_injection(object()))


class IsAttributeInjectionTests(unittest.TestCase):
    """`is_attribute_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(utils.is_attribute_injection(
            injections.Attribute('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(utils.is_attribute_injection(injections.Attribute))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(utils.is_attribute_injection(injections.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(utils.is_attribute_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(utils.is_attribute_injection(object()))


class IsCatalogTests(unittest.TestCase):
    """`is_catalog()` test cases."""

    def test_with_declarative_catalog(self):
        """Test with class."""
        self.assertTrue(utils.is_catalog(catalogs.DeclarativeCatalog))

    def test_with_dynamic_catalog(self):
        """Test with class."""
        self.assertTrue(utils.is_catalog(catalogs.DynamicCatalog()))

    def test_with_child_class(self):
        """Test with parent class."""
        class Catalog(catalogs.DeclarativeCatalog):
            """Example catalog child class."""

        self.assertTrue(utils.is_catalog(Catalog))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(utils.is_catalog('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(utils.is_catalog(object()))


class IsDynamicCatalogTests(unittest.TestCase):
    """`is_dynamic_catalog()` test cases."""

    def test_with_declarative_catalog(self):
        """Test with declarative catalog."""
        self.assertFalse(utils.is_dynamic_catalog(catalogs.DeclarativeCatalog))

    def test_with_dynamic_catalog(self):
        """Test with dynamic catalog."""
        self.assertTrue(utils.is_dynamic_catalog(catalogs.DynamicCatalog()))


class IsDeclarativeCatalogTests(unittest.TestCase):
    """`is_declarative_catalog()` test cases."""

    def test_with_declarative_catalog(self):
        """Test with declarative catalog."""
        self.assertTrue(utils.is_declarative_catalog(
            catalogs.DeclarativeCatalog))

    def test_with_dynamic_catalog(self):
        """Test with dynamic catalog."""
        self.assertFalse(utils.is_declarative_catalog(
            catalogs.DynamicCatalog()))
