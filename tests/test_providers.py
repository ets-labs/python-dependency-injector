"""Objects providers unittests."""

import unittest2 as unittest
from collections import namedtuple

from objects.providers import Provider
from objects.providers import Delegate
from objects.providers import NewInstance
from objects.providers import Singleton
from objects.providers import Scoped
from objects.providers import ExternalDependency
from objects.providers import Class
from objects.providers import Object
from objects.providers import Function
from objects.providers import Value
from objects.providers import Callable
from objects.providers import Config

from objects.injections import InitArg
from objects.injections import Attribute
from objects.injections import Method

from objects.utils import is_provider

from objects.errors import Error


class ProviderTest(unittest.TestCase):

    """Provider test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.provider = Provider()

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(is_provider(self.provider))

    def test_call(self):
        """Test call."""
        self.assertRaises(NotImplementedError, self.provider.__call__)

    def test_delegate(self):
        """Test creating of provider delegation."""
        delegate1 = self.provider.delegate()

        self.assertIsInstance(delegate1, Delegate)
        self.assertIs(delegate1.delegated, self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, Delegate)
        self.assertIs(delegate2.delegated, self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_override(self):
        """Test provider overriding."""
        overriding_provider = Provider()
        self.provider.override(overriding_provider)
        self.assertTrue(self.provider.overridden)

    def test_override_with_not_provider(self):
        """Test provider overriding with not provider instance."""
        self.assertRaises(Error, self.provider.override, object())

    def test_last_overriding(self):
        """Test getting last overriding provider."""
        overriding_provider1 = Provider()
        overriding_provider2 = Provider()

        self.provider.override(overriding_provider1)
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.override(overriding_provider2)
        self.assertIs(self.provider.last_overriding, overriding_provider2)

    def test_last_overriding_of_not_overridden_provider(self):
        """Test getting last overriding from not overridden provider."""
        try:
            self.provider.last_overriding
        except Error:
            pass
        else:
            self.fail('Got en error in {}'.format(
                str(self.test_last_overriding_of_not_overridden_provider)))


class DelegateTest(unittest.TestCase):

    """Delegate test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.delegated = Provider()
        self.delegate = Delegate(delegated=self.delegated)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(is_provider(self.delegate))

    def test_init_with_not_provider(self):
        """Test that delegate accepts only another provider as delegated."""
        self.assertRaises(Error, Delegate, delegated=object())

    def test_call(self):
        """ Test returning of delegated provider."""
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        self.assertIs(delegated1, self.delegated)
        self.assertIs(delegated2, self.delegated)


class NewInstanceTest(unittest.TestCase):

    """NewInstance test cases."""

    class Example(object):

        """Example class for NewInstance provider tests."""

        def __init__(self, init_arg1=None, init_arg2=None):
            """Initializer.

            :param init_arg1:
            :param init_arg2:
            :return:
            """
            self.init_arg1 = init_arg1
            self.init_arg2 = init_arg2

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

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(is_provider(NewInstance(self.Example)))

    def test_init_with_not_class(self):
        """Test creation of provider with not a class."""
        self.assertRaises(Error, NewInstance, 123)

    def test_call(self):
        """Test creation of new instances."""
        provider = NewInstance(self.Example)
        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_init_args(self):
        """Test creation of new instances with init args injections."""
        provider = NewInstance(self.Example,
                               InitArg('init_arg1', 'i1'),
                               InitArg('init_arg2', 'i2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_attributes(self):
        """Test creation of new instances with attribute injections."""
        provider = NewInstance(self.Example,
                               Attribute('attribute1', 'a1'),
                               Attribute('attribute2', 'a2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.attribute1, 'a1')
        self.assertEqual(instance1.attribute2, 'a2')

        self.assertEqual(instance2.attribute1, 'a1')
        self.assertEqual(instance2.attribute2, 'a2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_methods(self):
        """Test creation of new instances with method injections."""
        provider = NewInstance(self.Example,
                               Method('method1', 'm1'),
                               Method('method2', 'm2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.method1_value, 'm1')
        self.assertEqual(instance1.method2_value, 'm2')

        self.assertEqual(instance2.method1_value, 'm1')
        self.assertEqual(instance2.method2_value, 'm2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_context_args(self):
        """Test creation of new instances with context args."""
        provider = NewInstance(self.Example)
        instance = provider(11, 22)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)

    def test_call_with_context_kwargs(self):
        """Test creation of new instances with context kwargs."""
        provider = NewInstance(self.Example,
                               InitArg('init_arg1', 1))

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        instance1 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance1.init_arg1, 11)
        self.assertEqual(instance1.init_arg2, 22)

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = NewInstance(self.Example)
        overriding_provider1 = NewInstance(dict)
        overriding_provider2 = NewInstance(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, list)
        self.assertIsInstance(instance2, list)


class SingletonTest(unittest.TestCase):

    """Singleton test cases."""

    def test_call(self):
        """Test creation and returning of single object."""
        provider = Singleton(object)

        instance1 = provider()
        instance2 = provider()

        self.assertIsInstance(instance1, object)
        self.assertIsInstance(instance2, object)
        self.assertIs(instance1, instance2)

    def test_reset(self):
        """Test creation and reset of single object."""
        provider = Singleton(object)

        instance1 = provider()
        self.assertIsInstance(instance1, object)

        provider.reset()

        instance2 = provider()
        self.assertIsInstance(instance1, object)

        self.assertIsNot(instance1, instance2)
