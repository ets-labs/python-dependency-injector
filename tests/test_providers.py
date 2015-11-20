"""Dependency injector providers unittests."""

import unittest2 as unittest
import dependency_injector as di


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
        self.provider = di.Provider()

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.provider))

    def test_call(self):
        """Test call."""
        self.assertRaises(NotImplementedError, self.provider.__call__)

    def test_delegate(self):
        """Test creating of provider delegation."""
        delegate1 = self.provider.delegate()

        self.assertIsInstance(delegate1, di.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, di.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_override(self):
        """Test provider overriding."""
        overriding_provider = di.Provider()
        self.provider.override(overriding_provider)
        self.assertTrue(self.provider.is_overridden)

    def test_override_with_itself(self):
        """Test provider overriding with itself."""
        self.assertRaises(di.Error, self.provider.override, self.provider)

    def test_override_with_not_provider(self):
        """Test provider overriding with not provider instance."""
        self.assertRaises(di.Error, self.provider.override, object())

    def test_last_overriding(self):
        """Test getting last overriding provider."""
        overriding_provider1 = di.Provider()
        overriding_provider2 = di.Provider()

        self.provider.override(overriding_provider1)
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.override(overriding_provider2)
        self.assertIs(self.provider.last_overriding, overriding_provider2)

    def test_last_overriding_of_not_overridden_provider(self):
        """Test getting last overriding from not overridden provider."""
        try:
            self.provider.last_overriding
        except di.Error:
            pass
        else:
            self.fail('Got en error in {}'.format(
                str(self.test_last_overriding_of_not_overridden_provider)))

    def test_reset_last_overriding(self):
        """Test reseting of last overriding provider."""
        overriding_provider1 = di.Provider()
        overriding_provider2 = di.Provider()

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        self.assertIs(self.provider.last_overriding, overriding_provider2)

        self.provider.reset_last_overriding()
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.reset_last_overriding()
        self.assertFalse(self.provider.is_overridden)

    def test_reset_last_overriding_of_not_overridden_provider(self):
        """Test resetting of last overriding on not overridden provier."""
        self.assertRaises(di.Error, self.provider.reset_last_overriding)

    def test_reset_override(self):
        """Test reset of provider's override."""
        overriding_provider = di.Provider()
        self.provider.override(overriding_provider)

        self.assertTrue(self.provider.is_overridden)
        self.assertIs(self.provider.last_overriding, overriding_provider)

        self.provider.reset_override()

        self.assertFalse(self.provider.is_overridden)
        try:
            self.provider.last_overriding
        except di.Error:
            pass
        else:
            self.fail('Got en error in {}'.format(
                str(self.test_last_overriding_of_not_overridden_provider)))


class DelegateTests(unittest.TestCase):
    """Delegate test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.delegated = di.Provider()
        self.delegate = di.Delegate(delegated=self.delegated)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.delegate))

    def test_init_with_not_provider(self):
        """Test that delegate accepts only another provider as delegated."""
        self.assertRaises(di.Error, di.Delegate, delegated=object())

    def test_call(self):
        """Test returning of delegated provider."""
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        self.assertIs(delegated1, self.delegated)
        self.assertIs(delegated2, self.delegated)


class FactoryTests(unittest.TestCase):
    """Factory test cases."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(di.Factory(Example)))

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(di.Factory(credits))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(di.Error, di.Factory, 123)

    def test_call(self):
        """Test creation of new instances."""
        provider = di.Factory(Example)
        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_args(self):
        """Test creation of new instances with init positional args.

        New simplified syntax.
        """
        provider = di.Factory(Example, 'i1', 'i2')

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
        provider = di.Factory(Example, init_arg1='i1', init_arg2='i2')

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
        provider = di.Factory(Example, 'i1', init_arg2='i2')

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
        provider = di.Factory(Example,
                              di.Arg('i1'),
                              di.KwArg('init_arg2', 'i2'))

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
        provider = di.Factory(Example,
                              di.Attribute('attribute1', 'a1'),
                              di.Attribute('attribute2', 'a2'))

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
        provider = di.Factory(Example,
                              di.Method('method1', 'm1'),
                              di.Method('method2', 'm2'))

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
        provider = di.Factory(Example, 11, 22)
        instance = provider(33, 44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_call_with_context_kwargs(self):
        """Test creation of new instances with context kwargs."""
        provider = di.Factory(Example,
                              di.KwArg('init_arg1', 1))

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        instance2 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance2.init_arg1, 11)
        self.assertEqual(instance2.init_arg2, 22)

    def test_call_with_context_args_and_kwargs(self):
        """Test creation of new instances with context args and kwargs."""
        provider = di.Factory(Example, 11)
        instance = provider(22, init_arg3=33, init_arg4=44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = di.Factory(Example)
        overriding_provider1 = di.Factory(dict)
        overriding_provider2 = di.Factory(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, list)
        self.assertIsInstance(instance2, list)

    def test_injections(self):
        """Test getting a full list of injections using injections property."""
        provider = di.Factory(Example,
                              di.Arg(1),
                              di.KwArg('init_arg2', 2),
                              di.Attribute('attribute1', 3),
                              di.Attribute('attribute2', 4),
                              di.Method('method1', 5),
                              di.Method('method2', 6))

        injections = provider.injections

        self.assertEquals(len(injections), 6)


class SingletonTests(unittest.TestCase):
    """Singleton test cases."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(di.Singleton(Example)))

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(di.Singleton(credits))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(di.Error, di.Singleton, 123)

    def test_call(self):
        """Test getting of instances."""
        provider = di.Singleton(Example)
        instance1 = provider()
        instance2 = provider()

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_args(self):
        """Test getting of instances with init positional args.

        New simplified syntax.
        """
        provider = di.Singleton(Example, 'i1', 'i2')

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
        provider = di.Singleton(Example, init_arg1='i1', init_arg2='i2')

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
        provider = di.Singleton(Example, 'i1', init_arg2='i2')

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
        provider = di.Singleton(Example,
                                di.Arg('i1'),
                                di.KwArg('init_arg2', 'i2'))

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
        provider = di.Singleton(Example,
                                di.Attribute('attribute1', 'a1'),
                                di.Attribute('attribute2', 'a2'))

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
        provider = di.Singleton(Example,
                                di.Method('method1', 'm1'),
                                di.Method('method2', 'm2'))

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
        provider = di.Singleton(Example)
        instance = provider(11, 22)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)

    def test_call_with_context_kwargs(self):
        """Test getting of instances with context kwargs."""
        provider = di.Singleton(Example,
                                di.KwArg('init_arg1', 1))

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        # Instance is created earlier
        instance1 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

    def test_call_with_context_args_and_kwargs(self):
        """Test getting of instances with context args and kwargs."""
        provider = di.Singleton(Example, 11)
        instance = provider(22, init_arg3=33, init_arg4=44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_call_overridden(self):
        """Test getting of instances on overridden provider."""
        provider = di.Singleton(Example)
        overriding_provider1 = di.Singleton(dict)
        overriding_provider2 = di.Singleton(object)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, object)
        self.assertIsInstance(instance2, object)

    def test_injections(self):
        """Test getting a full list of injections using injections property."""
        provider = di.Singleton(Example,
                                di.Arg(1),
                                di.KwArg('init_arg2', 2),
                                di.Attribute('attribute1', 3),
                                di.Attribute('attribute2', 4),
                                di.Method('method1', 5),
                                di.Method('method2', 6))

        injections = provider.injections

        self.assertEquals(len(injections), 6)

    def test_reset(self):
        """Test creation and reset of single object."""
        provider = di.Singleton(object)

        instance1 = provider()
        self.assertIsInstance(instance1, object)

        provider.reset()

        instance2 = provider()
        self.assertIsInstance(instance1, object)

        self.assertIsNot(instance1, instance2)


class ExternalDependencyTests(unittest.TestCase):
    """ExternalDependency test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.provider = di.ExternalDependency(instance_of=list)

    def test_init_with_not_class(self):
        """Test creation with not a class."""
        self.assertRaises(di.Error, di.ExternalDependency, object())

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.provider))

    def test_call_overridden(self):
        """Test call of overridden external dependency."""
        self.provider.provided_by(di.Factory(list))
        self.assertIsInstance(self.provider(), list)

    def test_call_overridden_but_not_instance_of(self):
        """Test call of overridden external dependency, but not instance of."""
        self.provider.provided_by(di.Factory(dict))
        self.assertRaises(di.Error, self.provider)

    def test_call_not_overridden(self):
        """Test call of not satisfied external dependency."""
        self.assertRaises(di.Error, self.provider)


class StaticProvidersTests(unittest.TestCase):
    """Static providers test cases."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(di.Class(object)))
        self.assertTrue(di.is_provider(di.Object(object())))
        self.assertTrue(di.is_provider(di.Function(map)))
        self.assertTrue(di.is_provider(di.Value(123)))

    def test_call_class_provider(self):
        """Test Class provider call."""
        self.assertIs(di.Class(dict)(), dict)

    def test_call_object_provider(self):
        """Test Object provider call."""
        obj = object()
        self.assertIs(di.Object(obj)(), obj)

    def test_call_function_provider(self):
        """Test Function provider call."""
        self.assertIs(di.Function(map)(), map)

    def test_call_value_provider(self):
        """Test Value provider call."""
        self.assertEqual(di.Value(123)(), 123)

    def test_call_overridden_class_provider(self):
        """Test overridden Class provider call."""
        cls_provider = di.Class(dict)
        cls_provider.override(di.Object(list))
        self.assertIs(cls_provider(), list)

    def test_call_overridden_object_provider(self):
        """Test overridden Object provider call."""
        obj1 = object()
        obj2 = object()
        obj_provider = di.Object(obj1)
        obj_provider.override(di.Object(obj2))
        self.assertIs(obj_provider(), obj2)

    def test_call_overridden_function_provider(self):
        """Test overridden Function provider call."""
        function_provider = di.Function(len)
        function_provider.override(di.Function(sum))
        self.assertIs(function_provider(), sum)

    def test_call_overridden_value_provider(self):
        """Test overridden Value provider call."""
        value_provider = di.Value(123)
        value_provider.override(di.Value(321))
        self.assertEqual(value_provider(), 321)


class CallableTests(unittest.TestCase):
    """Callable test cases."""

    def example(self, arg1, arg2, arg3, arg4):
        """Example callback."""
        return arg1, arg2, arg3, arg4

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(di.Callable(self.example))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(di.Error, di.Callable, 123)

    def test_call(self):
        """Test call."""
        provider = di.Callable(lambda: True)
        self.assertTrue(provider())

    def test_call_with_positional_args(self):
        """Test call with positional args.

        New simplified syntax.
        """
        provider = di.Callable(self.example, 1, 2, 3, 4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_keyword_args(self):
        """Test call with keyword args.

        New simplified syntax.
        """
        provider = di.Callable(self.example, arg1=1, arg2=2, arg3=3, arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args(self):
        """Test call with positional and keyword args.

        Simplified syntax of positional and keyword arg injections.
        """
        provider = di.Callable(self.example, 1, 2, arg3=3, arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args_extended_syntax(self):
        """Test call with positional and keyword args.

        Extended syntax of positional and keyword arg injections.
        """
        provider = di.Callable(self.example,
                               di.Arg(1),
                               di.Arg(2),
                               di.KwArg('arg3', 3),
                               di.KwArg('arg4', 4))
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_context_args(self):
        """Test call with context args."""
        provider = di.Callable(self.example, 1, 2)
        self.assertTupleEqual(provider(3, 4), (1, 2, 3, 4))

    def test_call_with_context_kwargs(self):
        """Test call with context kwargs."""
        provider = di.Callable(self.example,
                               di.KwArg('arg1', 1))
        self.assertTupleEqual(provider(arg2=2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_with_context_args_and_kwargs(self):
        """Test call with context args and kwargs."""
        provider = di.Callable(self.example, 1)
        self.assertTupleEqual(provider(2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = di.Callable(self.example)
        provider.override(di.Value((4, 3, 2, 1)))
        provider.override(di.Value((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_injections(self):
        """Test getting a full list of injections using injections property."""
        provider = di.Callable(self.example, 1, 2, arg3=3, arg4=4)
        self.assertEquals(len(provider.injections), 4)


class ConfigTests(unittest.TestCase):
    """Config test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.initial_data = dict(key='value',
                                 category=dict(setting='setting_value'))
        self.provider = di.Config(self.initial_data)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.provider))

    def test_init_without_initial_value(self):
        """Test provider's creation with no initial value."""
        self.assertEqual(di.Config()(), dict())

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

        self.assertTrue(di.is_provider(category))
        self.assertTrue(di.is_provider(category_setting))

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_and_update_from(self):
        """Test returning of deferred child config values."""
        self.provider = di.Config()
        category = self.provider.category
        category_setting = self.provider.category.setting

        self.assertTrue(di.is_provider(category))
        self.assertTrue(di.is_provider(category_setting))

        self.provider.update_from(self.initial_data)

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_with_empty_value(self):
        """Test returning of deferred child config values."""
        self.provider = di.Config()
        category_setting = self.provider.category.setting
        self.assertRaises(di.Error, category_setting)
