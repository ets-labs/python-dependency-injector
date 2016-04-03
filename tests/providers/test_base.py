"""Dependency injector base providers unittests."""

import unittest2 as unittest

from dependency_injector import providers
from dependency_injector import errors
from dependency_injector import utils


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

    def test_overriding_context(self):
        """Test provider overriding context."""
        overriding_provider = providers.Provider()
        with self.provider.override(overriding_provider):
            self.assertTrue(self.provider.is_overridden)
        self.assertFalse(self.provider.is_overridden)

    def test_override_with_itself(self):
        """Test provider overriding with itself."""
        self.assertRaises(errors.Error, self.provider.override, self.provider)

    def test_override_with_not_provider(self):
        """Test provider overriding with not provider instance."""
        obj = object()
        self.provider.override(obj)
        self.assertIs(self.provider(), obj)

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
                         '<dependency_injector.providers.base.'
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
                         '<dependency_injector.providers.base.'
                         'Delegate({0}) at {1}>'.format(
                             repr(self.delegated),
                             hex(id(self.delegate))))


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
                         '<dependency_injector.providers.base.'
                         'ExternalDependency({0}) at {1}>'.format(
                             repr(list),
                             hex(id(self.provider))))
