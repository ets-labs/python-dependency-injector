"""Dependency injector providers unittests."""

import unittest2 as unittest

from dependency_injector import providers
from dependency_injector import injections
from dependency_injector import errors
from dependency_injector import utils


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


class ProviderTests(unittest.TestCase):
    """Provider test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.provider = providers.Provider()

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(self.provider))

    def test_call(self):
        """Test call."""
        self.assertRaises(NotImplementedError, self.provider.__call__)

    def test_delegate(self):
        """Test creating of provider delegation."""
        delegate1 = self.provider.delegate()

        self.assertIsInstance(delegate1, providers.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, providers.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_override(self):
        """Test provider overriding."""
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)
        self.assertTrue(self.provider.is_overridden)

    def test_override_with_itself(self):
        """Test provider overriding with itself."""
        self.assertRaises(errors.Error, self.provider.override, self.provider)

    def test_override_with_not_provider(self):
        """Test provider overriding with not provider instance."""
        self.assertRaises(errors.Error, self.provider.override, object())

    def test_last_overriding(self):
        """Test getting last overriding provider."""
        overriding_provider1 = providers.Provider()
        overriding_provider2 = providers.Provider()

        self.provider.override(overriding_provider1)
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.override(overriding_provider2)
        self.assertIs(self.provider.last_overriding, overriding_provider2)

    def test_last_overriding_of_not_overridden_provider(self):
        """Test getting last overriding from not overridden provider."""
        self.assertIsNone(self.provider.last_overriding)

    def test_reset_last_overriding(self):
        """Test reseting of last overriding provider."""
        overriding_provider1 = providers.Provider()
        overriding_provider2 = providers.Provider()

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        self.assertIs(self.provider.last_overriding, overriding_provider2)

        self.provider.reset_last_overriding()
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.reset_last_overriding()
        self.assertFalse(self.provider.is_overridden)

    def test_reset_last_overriding_of_not_overridden_provider(self):
        """Test resetting of last overriding on not overridden provier."""
        self.assertRaises(errors.Error, self.provider.reset_last_overriding)

    def test_reset_override(self):
        """Test reset of provider's override."""
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)

        self.assertTrue(self.provider.is_overridden)
        self.assertIs(self.provider.last_overriding, overriding_provider)

        self.provider.reset_override()

        self.assertFalse(self.provider.is_overridden)
        self.assertIsNone(self.provider.last_overriding)

    def test_repr(self):
        """Test representation of provider."""
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.'
                         'Provider() at {0}>'.format(hex(id(self.provider))))


class DelegateTests(unittest.TestCase):
    """Delegate test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.delegated = providers.Provider()
        self.delegate = providers.Delegate(delegated=self.delegated)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(self.delegate))

    def test_init_with_not_provider(self):
        """Test that delegate accepts only another provider as delegated."""
        self.assertRaises(errors.Error, providers.Delegate, delegated=object())

    def test_call(self):
        """Test returning of delegated provider."""
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        self.assertIs(delegated1, self.delegated)
        self.assertIs(delegated2, self.delegated)

    def test_repr(self):
        """Test representation of provider."""
        self.assertEqual(repr(self.delegate),
                         '<dependency_injector.providers.'
                         'Delegate({0}) at {1}>'.format(
                             repr(self.delegated),
                             hex(id(self.delegate))))


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
                         '<dependency_injector.providers.'
                         'Factory({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


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
                         '<dependency_injector.providers.'
                         'Singleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class CallableTests(unittest.TestCase):
    """Callable test cases."""

    def example(self, arg1, arg2, arg3, arg4):
        """Example callback."""
        return arg1, arg2, arg3, arg4

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(providers.Callable(self.example))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(errors.Error, providers.Callable, 123)

    def test_call(self):
        """Test call."""
        provider = providers.Callable(lambda: True)
        self.assertTrue(provider())

    def test_call_with_positional_args(self):
        """Test call with positional args.

        New simplified syntax.
        """
        provider = providers.Callable(self.example, 1, 2, 3, 4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_keyword_args(self):
        """Test call with keyword args.

        New simplified syntax.
        """
        provider = providers.Callable(self.example,
                                      arg1=1,
                                      arg2=2,
                                      arg3=3,
                                      arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args(self):
        """Test call with positional and keyword args.

        Simplified syntax of positional and keyword arg injections.
        """
        provider = providers.Callable(self.example, 1, 2, arg3=3, arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args_extended_syntax(self):
        """Test call with positional and keyword args.

        Extended syntax of positional and keyword arg injections.
        """
        provider = providers.Callable(self.example,
                                      injections.Arg(1),
                                      injections.Arg(2),
                                      injections.KwArg('arg3', 3),
                                      injections.KwArg('arg4', 4))
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_context_args(self):
        """Test call with context args."""
        provider = providers.Callable(self.example, 1, 2)
        self.assertTupleEqual(provider(3, 4), (1, 2, 3, 4))

    def test_call_with_context_kwargs(self):
        """Test call with context kwargs."""
        provider = providers.Callable(self.example,
                                      injections.KwArg('arg1', 1))
        self.assertTupleEqual(provider(arg2=2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_with_context_args_and_kwargs(self):
        """Test call with context args and kwargs."""
        provider = providers.Callable(self.example, 1)
        self.assertTupleEqual(provider(2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = providers.Callable(self.example)
        provider.override(providers.Value((4, 3, 2, 1)))
        provider.override(providers.Value((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_injections(self):
        """Test getting a full list of injections using injections property."""
        provider = providers.Callable(self.example, 1, 2, arg3=3, arg4=4)
        self.assertEquals(len(provider.injections), 4)

    def test_repr(self):
        """Test representation of provider."""
        provider = providers.Callable(self.example,
                                      injections.KwArg(
                                          'arg1',
                                          providers.Factory(dict)),
                                      injections.KwArg(
                                          'arg2',
                                          providers.Factory(list)),
                                      injections.KwArg(
                                          'arg3',
                                          providers.Factory(set)),
                                      injections.KwArg(
                                          'arg4',
                                          providers.Factory(tuple)))
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Callable({0}) at {1}>'.format(
                             repr(self.example),
                             hex(id(provider))))


class ExternalDependencyTests(unittest.TestCase):
    """ExternalDependency test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.provider = providers.ExternalDependency(instance_of=list)

    def test_init_with_not_class(self):
        """Test creation with not a class."""
        self.assertRaises(errors.Error, providers.ExternalDependency, object())

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(self.provider))

    def test_call_overridden(self):
        """Test call of overridden external dependency."""
        self.provider.provided_by(providers.Factory(list))
        self.assertIsInstance(self.provider(), list)

    def test_call_overridden_but_not_instance_of(self):
        """Test call of overridden external dependency, but not instance of."""
        self.provider.provided_by(providers.Factory(dict))
        self.assertRaises(errors.Error, self.provider)

    def test_call_not_overridden(self):
        """Test call of not satisfied external dependency."""
        self.assertRaises(errors.Error, self.provider)

    def test_repr(self):
        """Test representation of provider."""
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.'
                         'ExternalDependency({0}) at {1}>'.format(
                             repr(list),
                             hex(id(self.provider))))


class StaticProvidersTests(unittest.TestCase):
    """Static providers test cases."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(providers.Class(object)))
        self.assertTrue(utils.is_provider(providers.Object(object())))
        self.assertTrue(utils.is_provider(providers.Function(map)))
        self.assertTrue(utils.is_provider(providers.Value(123)))

    def test_call_class_provider(self):
        """Test Class provider call."""
        self.assertIs(providers.Class(dict)(), dict)

    def test_call_object_provider(self):
        """Test Object provider call."""
        obj = object()
        self.assertIs(providers.Object(obj)(), obj)

    def test_call_function_provider(self):
        """Test Function provider call."""
        self.assertIs(providers.Function(map)(), map)

    def test_call_value_provider(self):
        """Test Value provider call."""
        self.assertEqual(providers.Value(123)(), 123)

    def test_call_overridden_class_provider(self):
        """Test overridden Class provider call."""
        cls_provider = providers.Class(dict)
        cls_provider.override(providers.Object(list))
        self.assertIs(cls_provider(), list)

    def test_call_overridden_object_provider(self):
        """Test overridden Object provider call."""
        obj1 = object()
        obj2 = object()
        obj_provider = providers.Object(obj1)
        obj_provider.override(providers.Object(obj2))
        self.assertIs(obj_provider(), obj2)

    def test_call_overridden_function_provider(self):
        """Test overridden Function provider call."""
        function_provider = providers.Function(len)
        function_provider.override(providers.Function(sum))
        self.assertIs(function_provider(), sum)

    def test_call_overridden_value_provider(self):
        """Test overridden Value provider call."""
        value_provider = providers.Value(123)
        value_provider.override(providers.Value(321))
        self.assertEqual(value_provider(), 321)

    def test_repr(self):
        """Test representation of provider."""
        class_provider = providers.Class(object)
        self.assertEqual(repr(class_provider),
                         '<dependency_injector.providers.'
                         'Class({0}) at {1}>'.format(
                             repr(object),
                             hex(id(class_provider))))

        some_object = object()
        object_provider = providers.Object(some_object)
        self.assertEqual(repr(object_provider),
                         '<dependency_injector.providers.'
                         'Object({0}) at {1}>'.format(
                             repr(some_object),
                             hex(id(object_provider))))

        function_provider = providers.Function(map)
        self.assertEqual(repr(function_provider),
                         '<dependency_injector.providers.'
                         'Function({0}) at {1}>'.format(
                             repr(map),
                             hex(id(function_provider))))

        value_provider = providers.Value(123)
        self.assertEqual(repr(value_provider),
                         '<dependency_injector.providers.'
                         'Value({0}) at {1}>'.format(
                             repr(123),
                             hex(id(value_provider))))


class ConfigTests(unittest.TestCase):
    """Config test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.initial_data = dict(key='value',
                                 category=dict(setting='setting_value'))
        self.provider = providers.Config(self.initial_data)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(self.provider))

    def test_init_without_initial_value(self):
        """Test provider's creation with no initial value."""
        self.assertEqual(providers.Config()(), dict())

    def test_call(self):
        """Test returning of config value."""
        self.assertEqual(self.provider(), self.initial_data)

    def test_update_from(self):
        """Test update of config value."""
        self.assertEqual(self.provider(), self.initial_data)

        self.initial_data['key'] = 'other_value'
        self.provider.update_from(self.initial_data)
        self.assertEqual(self.provider(), self.initial_data)

    def test_call_child(self):
        """Test returning of child config values."""
        category = self.provider.category
        category_setting = self.provider.category.setting

        self.assertTrue(utils.is_provider(category))
        self.assertTrue(utils.is_provider(category_setting))

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_and_update_from(self):
        """Test returning of deferred child config values."""
        self.provider = providers.Config()
        category = self.provider.category
        category_setting = self.provider.category.setting

        self.assertTrue(utils.is_provider(category))
        self.assertTrue(utils.is_provider(category_setting))

        self.provider.update_from(self.initial_data)

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_with_empty_value(self):
        """Test returning of deferred child config values."""
        self.provider = providers.Config()
        category_setting = self.provider.category.setting
        self.assertRaises(errors.Error, category_setting)

    def test_repr(self):
        """Test representation of provider."""
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.'
                         'Config({0}) at {1}>'.format(
                             repr(self.initial_data),
                             hex(id(self.provider))))

        category_setting = self.provider.category.setting
        self.assertEqual(repr(category_setting),
                         '<dependency_injector.providers.'
                         'ChildConfig({0}) at {1}>'.format(
                             repr('.'.join(('category', 'setting'))),
                             hex(id(category_setting))))
