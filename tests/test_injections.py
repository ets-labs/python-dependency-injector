"""Dependency injector injections unittests."""

import unittest2 as unittest

from dependency_injector import injections
from dependency_injector import catalogs
from dependency_injector import providers
from dependency_injector import errors


class InjectionTests(unittest.TestCase):
    """Injection test cases."""

    def test_init(self):
        """Test Injection creation and initialization."""
        injection = injections.Injection('some_value')
        self.assertEqual(injection.injectable, 'some_value')

    def test_value_with_scalar_injectable(self):
        """Test Injection value property with scalar value."""
        injection = injections.Injection('some_value')
        self.assertEqual(injection.value, 'some_value')

    def test_value_with_provider_injectable(self):
        """Test Injection value property with provider."""
        injection = injections.Injection(providers.Factory(object))
        self.assertIsInstance(injection.value, object)

    def test_value_with_catalog_bundle_injectable(self):
        """Test Injection value property with catalog bundle."""
        class TestCatalog(catalogs.DeclarativeCatalog):
            """Test catalog."""

            provider = providers.Provider()
        injection = injections.Injection(
            TestCatalog.Bundle(TestCatalog.provider))

        self.assertIsInstance(injection.value, TestCatalog.Bundle)


class ArgTests(unittest.TestCase):
    """Positional arg injection test cases."""

    def test_init(self):
        """Test Arg creation and initialization."""
        injection = injections.Arg('some_value')
        self.assertEqual(injection.injectable, 'some_value')


class KwArgTests(unittest.TestCase):
    """Keyword arg injection test cases."""

    def test_init(self):
        """Test KwArg creation and initialization."""
        injection = injections.KwArg('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class AttributeTests(unittest.TestCase):
    """Attribute injection test cases."""

    def test_init(self):
        """Test Attribute creation and initialization."""
        injection = injections.Attribute('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class MethodTests(unittest.TestCase):
    """Method injection test cases."""

    def test_init(self):
        """Test Method creation and initialization."""
        injection = injections.Method('some_arg_name', 'some_value')
        self.assertEqual(injection.name, 'some_arg_name')
        self.assertEqual(injection.injectable, 'some_value')


class InjectTests(unittest.TestCase):
    """Inject decorator test cases."""

    def test_decorated_args(self):
        """Test `inject()` decoration with args."""
        provider1 = providers.Factory(object)
        provider2 = providers.Factory(list)

        @injections.inject(provider1, provider2)
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

    def test_decorated_args_extended_syntax(self):
        """Test `inject()` decoration with args."""
        provider1 = providers.Factory(object)
        provider2 = providers.Factory(list)

        @injections.inject(injections.Arg(provider1),
                           injections.Arg(provider2))
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

    def test_decorated_args_several_times(self):
        """Test `inject()` decoration with args several times."""
        provider1 = providers.Factory(object)
        provider2 = providers.Factory(list)

        @injections.inject(provider2)
        @injections.inject(provider1)
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

    def test_decorated_context_args(self):
        """Test `inject()` decoration with context args."""
        provider1 = providers.Factory(object)
        provider2 = providers.Factory(list)

        @injections.inject(provider1)
        def test(a, b):
            return a, b

        a1, b1 = test(provider2())
        a2, b2 = test(provider2())

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIsNot(a1, a2)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_decorated_kwargs(self):
        """Test `inject()` decoration with kwargs."""
        provider1 = providers.Factory(object)
        provider2 = providers.Factory(list)

        @injections.inject(a=provider1)
        @injections.inject(b=provider2)
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
        provider1 = providers.Factory(object)
        provider2 = providers.Factory(list)
        object_a = object()

        @injections.inject(a=provider1)
        @injections.inject(b=provider2)
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
        provider = providers.Factory(list)
        object_a = object()

        @injections.inject(b=provider)
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
        provider = providers.Factory(list)
        object_a = object()

        @injections.inject(injections.KwArg('b', provider))
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

    def test_decorate_class_method(self):
        """Test `inject()` decorator with class method."""
        class Test(object):
            """Test class."""

            @injections.inject(arg1=123)
            @injections.inject(arg2=456)
            def some_method(self, arg1, arg2):
                """Some test method."""
                return arg1, arg2

        test_object = Test()
        arg1, arg2 = test_object.some_method()

        self.assertEquals(arg1, 123)
        self.assertEquals(arg2, 456)

    def test_decorate_class_with_init(self):
        """Test `inject()` decorator that decorate class with __init__."""
        @injections.inject(arg1=123)
        @injections.inject(arg2=456)
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
        with self.assertRaises(errors.Error):
            @injections.inject(arg1=123)
            class Test(object):
                """Test class."""
