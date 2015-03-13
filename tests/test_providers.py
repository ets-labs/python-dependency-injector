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

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(is_provider(NewInstance(object)))

    def test_call(self):
        """Test creation of new instances."""
        provider = NewInstance(object)
        instance1 = provider
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, object)
        self.assertIsInstance(instance2, object)

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = NewInstance(object)
        overriding_provider1 = NewInstance(dict)
        overriding_provider2 = NewInstance(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, list)
        self.assertIsInstance(instance2, list)

    # self.cls = namedtuple('Instance', ['arg1', 'arg2'])
    # self.provider = NewInstance(self.cls,
    #                             InitArg('arg1', 1),
    #                             InitArg('arg2', 2))

    # TODO: Test that NewInstance.provides takes only classes

    # TODO: Test filtering of init arg injections
    # TODO: Test filtering of attribute injections
    # TODO: Test filtering of method injections

    # TODO: Test call with applying of init arg injections
    # TODO: Test call with applying of attribute injections
    # TODO: Test call with applying of method injections

    # TODO: Test call with applying of context args
    # TODO: Test call with applying of context kwargs
    # TODO: Test call with applying of context args & kwargs
    # TODO: Test call with applying of context args & kwargs & init args
    # TODO:     injections
