"""Dependency injector injections unittests."""

import unittest2 as unittest

from dependency_injector.injections import Injection
from dependency_injector.injections import KwArg
from dependency_injector.injections import Attribute
from dependency_injector.injections import Method
from dependency_injector.injections import inject

from dependency_injector.providers import Factory

from dependency_injector.errors import Error


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
        injection = Injection('some_arg_name', Factory(object))
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


class InjectTests(unittest.TestCase):

    """Inject decorator test cases."""

    def test_decorated(self):
        """Test `inject()` decorated callback."""
        provider1 = Factory(object)
        provider2 = Factory(list)

        @inject(a=provider1)
        @inject(b=provider2)
        def test(a, b):
            return a, b

        a1, b1 = test()
        a2, b2 = test()

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIsNot(a1, a2)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_decorated_kwargs_priority(self):
        """Test `inject()` decorated callback kwargs priority."""
        provider1 = Factory(object)
        provider2 = Factory(list)
        object_a = object()

        @inject(a=provider1)
        @inject(b=provider2)
        def test(a, b):
            return a, b

        a1, b1 = test(a=object_a)
        a2, b2 = test(a=object_a)

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIs(a1, object_a)
        self.assertIs(a2, object_a)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_decorated_with_args(self):
        """Test `inject()` decorated callback with args."""
        provider = Factory(list)
        object_a = object()

        @inject(b=provider)
        def test(a, b):
            return a, b

        a1, b1 = test(object_a)
        a2, b2 = test(object_a)

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIs(a1, object_a)
        self.assertIs(a2, object_a)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_injection_kwarg_syntax(self):
        """Test `inject()` decorated callback with "old" style using KwArg."""
        provider = Factory(list)
        object_a = object()

        @inject(KwArg('b', provider))
        def test(a, b):
            return a, b

        a1, b1 = test(object_a)
        a2, b2 = test(object_a)

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIs(a1, object_a)
        self.assertIs(a2, object_a)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_decorate_with_not_injection(self):
        """Test `inject()` decorator with not an injection instance."""
        self.assertRaises(Error, inject, object)
