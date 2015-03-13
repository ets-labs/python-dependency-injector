"""Objects providers unittests."""

import unittest2 as unittest

from objects.providers import Provider
from objects.providers import ProviderDelegate
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

        self.assertIsInstance(delegate1, ProviderDelegate)
        self.assertIs(delegate1.delegated, self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, ProviderDelegate)
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


class ProviderDelegateTest(unittest.TestCase):

    """ProviderDelegate test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.delegated = Provider()
        self.delegate = ProviderDelegate(delegated=self.delegated)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(is_provider(self.delegate))

    def test_init_with_not_provider(self):
        """Test that delegate accepts only another provider as delegated."""
        self.assertRaises(Error, ProviderDelegate, delegated=object())

    def test_call(self):
        """ Test returning of delegated provider."""
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        self.assertIs(delegated1, self.delegated)
        self.assertIs(delegated2, self.delegated)
