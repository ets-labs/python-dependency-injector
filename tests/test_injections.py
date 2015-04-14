"""Objects injections unittests."""

import unittest2 as unittest

from objects.injections import Injection
from objects.injections import KwArg
from objects.injections import Attribute
from objects.injections import Method

from objects.providers import NewInstance


class InjectionTests(unittest.TestCase):

    """Injection test cases."""

    def test_init(self):
        """Test Injection creation and initialization."""
        injection = Injection('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')

    def test_value_with_scalar_injectable(self):
        """Test Injection value property with scalar value."""
        injection = Injection('some_arg_name', 'some_value')
        self.assertEqual(injection.value, 'some_value')

    def test_value_with_provider_injectable(self):
        """Test Injection value property with provider."""
        injection = Injection('some_arg_name', NewInstance(object))
        self.assertIsInstance(injection.value, object)


class KwArgTests(unittest.TestCase):

    """Keyword arg injection test cases."""

    def test_init(self):
        """Test KwArg creation and initialization."""
        injection = KwArg('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class AttributeTests(unittest.TestCase):

    """Attribute injection test cases."""

    def test_init(self):
        """Test Attribute creation and initialization."""
        injection = Attribute('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class MethodTests(unittest.TestCase):

    """Method injection test cases."""

    def test_init(self):
        """Test Method creation and initialization."""
        injection = Method('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')
