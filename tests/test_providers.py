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
