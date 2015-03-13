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

    def test_init(self):
        """Test creating and initialization."""
        self.assertIsInstance(Provider(), Provider)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(is_provider(Provider()))

    def test_call(self):
        """Test call."""
        self.assertRaises(NotImplementedError, Provider().__call__)

    def test_delegate(self):
        """Test creating of provider delegation."""
        provider = Provider()
        delegate = provider.delegate()

        self.assertIsInstance(delegate, ProviderDelegate)
        self.assertIs(delegate.delegated, provider)

    def test_override(self):
        """Test provider overriding."""
        provider = Provider()
        overriding_provider = Provider()
        provider.override(overriding_provider)
        self.assertTrue(provider.overridden)

    def test_override_with_not_provider(self):
        """Test provider overriding with not provider instance."""
        self.assertRaises(Error, Provider().override, object())

    def test_last_overriding(self):
        """Test getting last overriding provider."""
        provider = Provider()
        overriding_provider1 = Provider()
        overriding_provider2 = Provider()

        provider.override(overriding_provider1)
        self.assertIs(provider.last_overriding, overriding_provider1)

        provider.override(overriding_provider2)
        self.assertIs(provider.last_overriding, overriding_provider2)

    def test_last_overriding_of_not_overridden_provider(self):
        """Test getting last overriding from not overridden provider."""
        try:
            Provider().last_overriding
        except Error:
            pass
        else:
            self.fail('Got en error in {}'.format(
                str(self.test_last_overriding_of_not_overridden_provider)))
