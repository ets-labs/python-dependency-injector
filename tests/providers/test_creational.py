"""Dependency injector creational providers unittests."""

import unittest2 as unittest

from dependency_injector import providers
from dependency_injector import injections
from dependency_injector import utils
from dependency_injector import errors


class Example(object):
    """Example class for Factory provider tests."""

    def __init__(self, init_arg1=None, init_arg2=None, init_arg3=None,
                 init_arg4=None):
        """Initializer."""
        self.init_arg1 = init_arg1
        self.init_arg2 = init_arg2
        self.init_arg3 = init_arg3
        self.init_arg4 = init_arg4

        self.attribute1 = None
        self.attribute2 = None

        self.method1_value = None
        self.method2_value = None

    def method1(self, value):
        """Setter method 1."""
        self.method1_value = value

    def method2(self, value):
        """Setter method 2."""
        self.method2_value = value


class FactoryTests(unittest.TestCase):
    """Factory test cases."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(providers.Factory(Example)))

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(providers.Factory(credits))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(errors.Error, providers.Factory, 123)

    def test_init_with_valid_provided_type(self):
        """Test creation with not valid provided type."""
        class ExampleProvider(providers.Factory):
            """Example provider."""

            provided_type = Example

        example_provider = ExampleProvider(Example, 1, 2)

        self.assertIsInstance(example_provider(), Example)

    def test_init_with_valid_provided_subtype(self):
        """Test creation with not valid provided type."""
        class ExampleProvider(providers.Factory):
            """Example provider."""

            provided_type = Example

        class NewExampe(Example):
            """Example class subclass."""

        example_provider = ExampleProvider(NewExampe, 1, 2)

        self.assertIsInstance(example_provider(), NewExampe)

    def test_init_with_invalid_provided_type(self):
        """Test creation with not valid provided type."""
        class ExampleProvider(providers.Factory):
            """Example provider."""

            provided_type = Example

        with self.assertRaises(errors.Error):
            ExampleProvider(list)

    def test_call(self):
        """Test creation of new instances."""
        provider = providers.Factory(Example)
        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_args(self):
        """Test creation of new instances with init positional args.

        New simplified syntax.
        """
        provider = providers.Factory(Example, 'i1', 'i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_keyword_args(self):
        """Test creation of new instances with init keyword args.

        New simplified syntax.
        """
        provider = providers.Factory(Example, init_arg1='i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_and_keyword_args(self):
        """Test creation of new instances with init positional and keyword args.

        Simplified syntax of positional and keyword arg injections.
        """
        provider = providers.Factory(Example, 'i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_and_keyword_args_extended_syntax(self):
        """Test creation of new instances with init positional and keyword args.

        Extended syntax of positional and keyword arg injections.
        """
        provider = providers.Factory(Example,
                                     injections.Arg('i1'),
                                     injections.KwArg('init_arg2', 'i2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_attributes(self):
        """Test creation of new instances with attribute injections."""
        provider = providers.Factory(Example,
                                     injections.Attribute('attribute1', 'a1'),
                                     injections.Attribute('attribute2', 'a2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.attribute1, 'a1')
        self.assertEqual(instance1.attribute2, 'a2')

        self.assertEqual(instance2.attribute1, 'a1')
        self.assertEqual(instance2.attribute2, 'a2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_methods(self):
        """Test creation of new instances with method injections."""
        provider = providers.Factory(Example,
                                     injections.Method('method1', 'm1'),
                                     injections.Method('method2', 'm2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.method1_value, 'm1')
        self.assertEqual(instance1.method2_value, 'm2')

        self.assertEqual(instance2.method1_value, 'm1')
        self.assertEqual(instance2.method2_value, 'm2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_context_args(self):
        """Test creation of new instances with context args."""
        provider = providers.Factory(Example, 11, 22)
        instance = provider(33, 44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_call_with_context_kwargs(self):
        """Test creation of new instances with context kwargs."""
        provider = providers.Factory(Example,
                                     injections.KwArg('init_arg1', 1))

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        instance2 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance2.init_arg1, 11)
        self.assertEqual(instance2.init_arg2, 22)

    def test_call_with_context_args_and_kwargs(self):
        """Test creation of new instances with context args and kwargs."""
        provider = providers.Factory(Example, 11)
        instance = provider(22, init_arg3=33, init_arg4=44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = providers.Factory(Example)
        overriding_provider1 = providers.Factory(dict)
        overriding_provider2 = providers.Factory(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, list)
        self.assertIsInstance(instance2, list)

    def test_injections(self):
        """Test getting a full list of injections using injections property."""
        provider = providers.Factory(Example,
                                     injections.Arg(1),
                                     injections.KwArg('init_arg2', 2),
                                     injections.Attribute('attribute1', 3),
                                     injections.Attribute('attribute2', 4),
                                     injections.Method('method1', 5),
                                     injections.Method('method2', 6))
        self.assertEquals(len(provider.injections), 6)

    def test_repr(self):
        """Test representation of provider."""
        provider = providers.Factory(Example,
                                     injections.KwArg('init_arg1',
                                                      providers.Factory(dict)),
                                     injections.KwArg('init_arg2',
                                                      providers.Factory(list)))
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.creational.'
                         'Factory({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedFactoryTests(unittest.TestCase):
    """DelegatedFactory test cases."""

    def test_inheritance(self):
        """Test inheritance."""
        self.assertIsInstance(providers.DelegatedFactory(object),
                              providers.Factory)

    def test_is_provider(self):
        """Test is_provider."""
        self.assertTrue(utils.is_provider(providers.DelegatedFactory(object)))

    def test_is_delegated_provider(self):
        """Test is_delegated_provider."""
        self.assertTrue(utils.is_delegated_provider(
            providers.DelegatedFactory(object)))
        self.assertFalse(utils.is_delegated_provider(
            providers.Factory(object)))


class SingletonTests(unittest.TestCase):
    """Singleton test cases."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(providers.Singleton(Example)))

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(providers.Singleton(credits))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(errors.Error, providers.Singleton, 123)

    def test_init_with_valid_provided_type(self):
        """Test creation with not valid provided type."""
        class ExampleProvider(providers.Singleton):
            """Example provider."""

            provided_type = Example

        example_provider = ExampleProvider(Example, 1, 2)

        self.assertIsInstance(example_provider(), Example)

    def test_init_with_valid_provided_subtype(self):
        """Test creation with not valid provided type."""
        class ExampleProvider(providers.Singleton):
            """Example provider."""

            provided_type = Example

        class NewExampe(Example):
            """Example class subclass."""

        example_provider = ExampleProvider(NewExampe, 1, 2)

        self.assertIsInstance(example_provider(), NewExampe)

    def test_init_with_invalid_provided_type(self):
        """Test creation with not valid provided type."""
        class ExampleProvider(providers.Singleton):
            """Example provider."""

            provided_type = Example

        with self.assertRaises(errors.Error):
            ExampleProvider(list)

    def test_call(self):
        """Test getting of instances."""
        provider = providers.Singleton(Example)
        instance1 = provider()
        instance2 = provider()

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_args(self):
        """Test getting of instances with init positional args.

        New simplified syntax.
        """
        provider = providers.Singleton(Example, 'i1', 'i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_keyword_args(self):
        """Test getting of instances with init keyword args.

        New simplified syntax.
        """
        provider = providers.Singleton(Example, init_arg1='i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_and_keyword_args(self):
        """Test getting of instances with init positional and keyword args.

        Simplified syntax of positional and keyword arg injections.
        """
        provider = providers.Singleton(Example, 'i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_and_keyword_args_extended_syntax(self):
        """Test getting of instances with init positional and keyword args.

        Extended syntax of positional and keyword arg injections.
        """
        provider = providers.Singleton(Example,
                                       injections.Arg('i1'),
                                       injections.KwArg('init_arg2', 'i2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_attributes(self):
        """Test getting of instances with attribute injections."""
        provider = providers.Singleton(Example,
                                       injections.Attribute('attribute1',
                                                            'a1'),
                                       injections.Attribute('attribute2',
                                                            'a2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.attribute1, 'a1')
        self.assertEqual(instance1.attribute2, 'a2')

        self.assertEqual(instance2.attribute1, 'a1')
        self.assertEqual(instance2.attribute2, 'a2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_methods(self):
        """Test getting of instances with method injections."""
        provider = providers.Singleton(Example,
                                       injections.Method('method1', 'm1'),
                                       injections.Method('method2', 'm2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.method1_value, 'm1')
        self.assertEqual(instance1.method2_value, 'm2')

        self.assertEqual(instance2.method1_value, 'm1')
        self.assertEqual(instance2.method2_value, 'm2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_context_args(self):
        """Test getting of instances with context args."""
        provider = providers.Singleton(Example)
        instance = provider(11, 22)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)

    def test_call_with_context_kwargs(self):
        """Test getting of instances with context kwargs."""
        provider = providers.Singleton(Example,
                                       injections.KwArg('init_arg1', 1))

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        # Instance is created earlier
        instance1 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

    def test_call_with_context_args_and_kwargs(self):
        """Test getting of instances with context args and kwargs."""
        provider = providers.Singleton(Example, 11)
        instance = provider(22, init_arg3=33, init_arg4=44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_call_overridden(self):
        """Test getting of instances on overridden provider."""
        provider = providers.Singleton(Example)
        overriding_provider1 = providers.Singleton(dict)
        overriding_provider2 = providers.Singleton(object)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, object)
        self.assertIsInstance(instance2, object)

    def test_provides_attr(self):
        """Test provides attribute."""
        provider = providers.Singleton(Example)
        self.assertIs(provider.provides, Example)

    def test_args_attr(self):
        """Test args attribute."""
        provider = providers.Singleton(Example, 1, 2)
        self.assertEquals(len(provider.args), 2)

    def test_kwargs_attr(self):
        """Test kwargs attribute."""
        provider = providers.Singleton(Example, init_arg1=1, init_arg2=2)
        self.assertEquals(len(provider.kwargs), 2)

    def test_attributes_attr(self):
        """Test attributes attribute."""
        provider = providers.Singleton(Example,
                                       injections.Attribute('attribute1', 1),
                                       injections.Attribute('attribute2', 2))
        self.assertEquals(len(provider.attributes), 2)

    def test_methods_attr(self):
        """Test methods attribute."""
        provider = providers.Singleton(Example,
                                       injections.Method('method1', 1),
                                       injections.Method('method2', 2))
        self.assertEquals(len(provider.methods), 2)

    def test_injections(self):
        """Test getting a full list of injections using injections property."""
        provider = providers.Singleton(Example,
                                       injections.Arg(1),
                                       injections.KwArg('init_arg2', 2),
                                       injections.Attribute('attribute1', 3),
                                       injections.Attribute('attribute2', 4),
                                       injections.Method('method1', 5),
                                       injections.Method('method2', 6))
        self.assertEquals(len(provider.injections), 6)

    def test_reset(self):
        """Test creation and reset of single object."""
        provider = providers.Singleton(object)

        instance1 = provider()
        self.assertIsInstance(instance1, object)

        provider.reset()

        instance2 = provider()
        self.assertIsInstance(instance1, object)

        self.assertIsNot(instance1, instance2)

    def test_repr(self):
        """Test representation of provider."""
        provider = providers.Singleton(Example,
                                       injections.KwArg(
                                           'init_arg1',
                                           providers.Factory(dict)),
                                       injections.KwArg(
                                           'init_arg2',
                                           providers.Factory(list)))
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.creational.'
                         'Singleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedSingletonTests(unittest.TestCase):
    """DelegatedSingleton test cases."""

    def test_inheritance(self):
        """Test inheritance."""
        self.assertIsInstance(providers.DelegatedSingleton(object),
                              providers.Singleton)

    def test_is_provider(self):
        """Test is_provider."""
        self.assertTrue(utils.is_provider(
            providers.DelegatedSingleton(object)))

    def test_is_delegated_provider(self):
        """Test is_delegated_provider."""
        self.assertTrue(utils.is_delegated_provider(
            providers.DelegatedSingleton(object)))
        self.assertFalse(utils.is_delegated_provider(
            providers.Singleton(object)))


class FactoryAsDecoratorTests(unittest.TestCase):
    """Factory as decorator tests."""

    def test_decoration(self):
        """Test decoration of some class with Factory provider."""
        @providers.Factory
        class AuthService(object):
            """Auth service."""

        @providers.Factory
        @injections.inject(auth_service=AuthService)
        class UsersService(object):
            """Users service."""

            def __init__(self, auth_service):
                """Initializer."""
                self.auth_service = auth_service

        users_service = UsersService()

        self.assertIsInstance(users_service, UsersService.cls)
        self.assertIsInstance(users_service.auth_service, AuthService.cls)

    def test_decoration_and_overriding(self):
        """Test decoration of some class with Factory provider."""
        @providers.Factory
        class AuthService(object):
            """Auth service."""

        @providers.override(AuthService)
        @providers.Factory
        class ExtAuthService(AuthService.cls):
            """Extended auth service."""

        auth_service = AuthService()

        self.assertIsInstance(auth_service, ExtAuthService.cls)
