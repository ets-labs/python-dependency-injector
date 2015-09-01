"""Dependency injector utils unittests."""

import unittest2 as unittest
import dependency_injector as di


class IsProviderTests(unittest.TestCase):

    """`is_provider()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(di.is_provider(di.Provider()))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(di.is_provider(di.Provider))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(di.is_provider('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(di.is_provider(object()))

    def test_with_subclass_instance(self):
        """Test with subclass of provider instance."""
        class SomeProvider(di.Provider):

            """Some provider for test."""

        self.assertTrue(di.is_provider(SomeProvider()))

    def test_with_class_with_getattr(self):
        """Test with class that has __getattr__() method implementation."""
        class SomeClass(object):

            """Some test class with __getattr__() method implementation."""

            def __getattr__(self, _):
                """Test implementation that just returns False."""
                return False

        self.assertFalse(di.is_provider(SomeClass()))


class EnsureIsProviderTests(unittest.TestCase):

    """`ensure_is_provider` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        provider = di.Provider()
        self.assertIs(di.ensure_is_provider(provider), provider)

    def test_with_class(self):
        """Test with class."""
        self.assertRaises(di.Error, di.ensure_is_provider, di.Provider)

    def test_with_string(self):
        """Test with string."""
        self.assertRaises(di.Error, di.ensure_is_provider, 'some_string')

    def test_with_object(self):
        """Test with object."""
        self.assertRaises(di.Error, di.ensure_is_provider, object())


class IsInjectionTests(unittest.TestCase):

    """`is_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(di.is_injection(di.Injection('name', 'value')))

    def test_with_subclass_instances(self):
        """Test with subclass instances."""
        self.assertTrue(di.is_injection(di.KwArg('name', 'value')))
        self.assertTrue(di.is_injection(di.Attribute('name', 'value')))
        self.assertTrue(di.is_injection(di.Method('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(di.is_injection(di.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(di.is_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(di.is_injection(object()))


class EnsureIsInjectionTests(unittest.TestCase):

    """`ensure_is_injection` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        injection = di.Injection('name', 'value')
        self.assertIs(di.ensure_is_injection(injection), injection)

    def test_with_class(self):
        """Test with class."""
        self.assertRaises(di.Error, di.ensure_is_injection, di.Injection)

    def test_with_string(self):
        """Test with string."""
        self.assertRaises(di.Error, di.ensure_is_injection, 'some_string')

    def test_with_object(self):
        """Test with object."""
        self.assertRaises(di.Error, di.ensure_is_injection, object())


class IsKwArgInjectionTests(unittest.TestCase):

    """`is_kwarg_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(di.is_kwarg_injection(di.KwArg('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(di.is_kwarg_injection(di.KwArg))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(di.is_kwarg_injection(di.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(di.is_kwarg_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(di.is_kwarg_injection(object()))


class IsAttributeInjectionTests(unittest.TestCase):

    """`is_attribute_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(di.is_attribute_injection(di.Attribute('name',
                                                               'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(di.is_attribute_injection(di.Attribute))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(di.is_attribute_injection(di.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(di.is_attribute_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(di.is_attribute_injection(object()))


class IsMethodInjectionTests(unittest.TestCase):

    """`is_method_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(di.is_method_injection(di.Method('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(di.is_method_injection(di.Method))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(di.is_method_injection(di.Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(di.is_method_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(di.is_method_injection(object()))
