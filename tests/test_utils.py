"""Objects utils unittests."""

import unittest2 as unittest

from objects.utils import is_provider
from objects.utils import ensure_is_provider
from objects.utils import is_injection
from objects.utils import ensure_is_injection
from objects.utils import is_kwarg_injection
from objects.utils import is_attribute_injection
from objects.utils import is_method_injection

from objects.providers import Provider

from objects.injections import Injection
from objects.injections import KwArg
from objects.injections import Attribute
from objects.injections import Method

from objects.errors import Error


class IsProviderTests(unittest.TestCase):

    """`is_provider()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(is_provider(Provider()))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(is_provider(Provider))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(is_provider('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(is_provider(object()))

    def test_with_subclass_instance(self):
        """Test with subclass of provider instance."""
        class SomeProvider(Provider):

            """Some provider for test."""

        self.assertTrue(is_provider(SomeProvider()))

    def test_with_class_with_getattr(self):
        """Test with class that has __getattr__() method implementation."""
        class SomeClass(object):

            """Some test class with __getattr__() method implementation."""

            def __getattr__(self, _):
                """Test implementation that just returns False."""
                return False

        self.assertFalse(is_provider(SomeClass()))


class EnsureIsProviderTests(unittest.TestCase):

    """`ensure_is_provider` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        provider = Provider()
        self.assertIs(ensure_is_provider(provider), provider)

    def test_with_class(self):
        """Test with class."""
        self.assertRaises(Error, ensure_is_provider, Provider)

    def test_with_string(self):
        """Test with string."""
        self.assertRaises(Error, ensure_is_provider, 'some_string')

    def test_with_object(self):
        """Test with object."""
        self.assertRaises(Error, ensure_is_provider, object())


class IsInjectionTests(unittest.TestCase):

    """`is_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(is_injection(Injection('name', 'value')))

    def test_with_subclass_instances(self):
        """Test with subclass instances."""
        self.assertTrue(is_injection(KwArg('name', 'value')))
        self.assertTrue(is_injection(Attribute('name', 'value')))
        self.assertTrue(is_injection(Method('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(is_injection(Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(is_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(is_injection(object()))


class EnsureIsInjectionTests(unittest.TestCase):

    """`ensure_is_injection` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        injection = Injection('name', 'value')
        self.assertIs(ensure_is_injection(injection), injection)

    def test_with_class(self):
        """Test with class."""
        self.assertRaises(Error, ensure_is_injection, Injection)

    def test_with_string(self):
        """Test with string."""
        self.assertRaises(Error, ensure_is_injection, 'some_string')

    def test_with_object(self):
        """Test with object."""
        self.assertRaises(Error, ensure_is_injection, object())


class IsKwArgInjectionTests(unittest.TestCase):

    """`is_kwarg_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(is_kwarg_injection(KwArg('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(is_kwarg_injection(KwArg))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(is_kwarg_injection(Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(is_kwarg_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(is_kwarg_injection(object()))


class IsAttributeInjectionTests(unittest.TestCase):

    """`is_attribute_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(is_attribute_injection(Attribute('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(is_attribute_injection(Attribute))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(is_attribute_injection(Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(is_attribute_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(is_attribute_injection(object()))


class IsMethodInjectionTests(unittest.TestCase):

    """`is_method_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(is_method_injection(Method('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(is_method_injection(Method))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(is_method_injection(Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(is_method_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(is_method_injection(object()))
