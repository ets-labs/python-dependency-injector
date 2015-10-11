"""Dependency injector injections unittests."""

import unittest2 as unittest
import dependency_injector as di


class InjectionTests(unittest.TestCase):
    """Injection test cases."""

    def test_init(self):
        """Test Injection creation and initialization."""
        injection = di.Injection('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')

    def test_value_with_scalar_injectable(self):
        """Test Injection value property with scalar value."""
        injection = di.Injection('some_arg_name', 'some_value')
        self.assertEqual(injection.value, 'some_value')

    def test_value_with_provider_injectable(self):
        """Test Injection value property with provider."""
        injection = di.Injection('some_arg_name', di.Factory(object))
        self.assertIsInstance(injection.value, object)


class KwArgTests(unittest.TestCase):
    """Keyword arg injection test cases."""

    def test_init(self):
        """Test KwArg creation and initialization."""
        injection = di.KwArg('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class AttributeTests(unittest.TestCase):
    """Attribute injection test cases."""

    def test_init(self):
        """Test Attribute creation and initialization."""
        injection = di.Attribute('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class MethodTests(unittest.TestCase):
    """Method injection test cases."""

    def test_init(self):
        """Test Method creation and initialization."""
        injection = di.Method('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class InjectTests(unittest.TestCase):
    """Inject decorator test cases."""

    def test_decorated(self):
        """Test `inject()` decorated callback."""
        provider1 = di.Factory(object)
        provider2 = di.Factory(list)

        @di.inject(a=provider1)
        @di.inject(b=provider2)
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
        provider1 = di.Factory(object)
        provider2 = di.Factory(list)
        object_a = object()

        @di.inject(a=provider1)
        @di.inject(b=provider2)
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
        provider = di.Factory(list)
        object_a = object()

        @di.inject(b=provider)
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
        provider = di.Factory(list)
        object_a = object()

        @di.inject(di.KwArg('b', provider))
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
        self.assertRaises(di.Error, di.inject, object)

    def test_decorate_class_method(self):
        """Test `inject()` decorator with class method."""
        class Test(object):
            """Test class."""

            @di.inject(arg1=123)
            @di.inject(arg2=456)
            def some_method(self, arg1, arg2):
                """Some test method."""
                return arg1, arg2

        test_object = Test()
        arg1, arg2 = test_object.some_method()

        self.assertEquals(arg1, 123)
        self.assertEquals(arg2, 456)

    def test_decorate_class_with_init(self):
        """Test `inject()` decorator that decorate class with __init__."""
        @di.inject(arg1=123)
        @di.inject(arg2=456)
        class Test(object):
            """Test class."""

            def __init__(self, arg1, arg2):
                """Init."""
                self.arg1 = arg1
                self.arg2 = arg2

        test_object = Test()

        self.assertEquals(test_object.arg1, 123)
        self.assertEquals(test_object.arg2, 456)

    def test_decorate_class_without_init(self):
        """Test `inject()` decorator that decorate class without __init__."""
        with self.assertRaises(di.Error):
            @di.inject(arg1=123)
            class Test(object):
                """Test class."""
