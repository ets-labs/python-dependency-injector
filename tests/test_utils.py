"""Objects utils unittests."""

import unittest2 as unittest

from objects.utils import is_provider
from objects.utils import is_injection
from objects.utils import is_init_arg_injection
from objects.utils import is_attribute_injection
from objects.utils import is_method_injection

from objects.providers import Provider

from objects.injections import Injection
from objects.injections import InitArg
from objects.injections import Attribute
from objects.injections import Method


class IsProviderTest(unittest.TestCase):

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


class IsInjectionTest(unittest.TestCase):

    """`is_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(is_injection(Injection('name', 'value')))

    def test_with_subclass_instances(self):
        """Test with subclass instances."""
        self.assertTrue(is_injection(InitArg('name', 'value')))
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


class IsInitArgInjectionTest(unittest.TestCase):

    """`is_init_arg_injection()` test cases."""

    def test_with_instance(self):
        """Test with instance."""
        self.assertTrue(is_init_arg_injection(InitArg('name', 'value')))

    def test_with_class(self):
        """Test with class."""
        self.assertFalse(is_init_arg_injection(InitArg))

    def test_with_parent_class(self):
        """Test with parent class."""
        self.assertFalse(is_init_arg_injection(Injection))

    def test_with_string(self):
        """Test with string."""
        self.assertFalse(is_init_arg_injection('some_string'))

    def test_with_object(self):
        """Test with object."""
        self.assertFalse(is_init_arg_injection(object()))


class IsAttributeInjectionTest(unittest.TestCase):

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


class IsMethodInjectionTest(unittest.TestCase):

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
