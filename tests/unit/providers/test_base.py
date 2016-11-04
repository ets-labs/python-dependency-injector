"""Dependency injector base providers unit tests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    errors,
)


class ProviderTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.Provider()

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.provider))

    def test_call(self):
        self.assertRaises(NotImplementedError, self.provider.__call__)

    def test_delegate(self):
        delegate1 = self.provider.delegate()

        self.assertIsInstance(delegate1, providers.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, providers.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)
        self.assertTrue(self.provider.overridden)

    def test_overriding_context(self):
        overriding_provider = providers.Provider()
        with self.provider.override(overriding_provider):
            self.assertTrue(self.provider.overridden)
        self.assertFalse(self.provider.overridden)

    def test_override_with_itself(self):
        self.assertRaises(errors.Error, self.provider.override, self.provider)

    def test_override_with_not_provider(self):
        obj = object()
        self.provider.override(obj)
        self.assertIs(self.provider(), obj)

    def test_reset_last_overriding(self):
        overriding_provider1 = providers.Provider()
        overriding_provider2 = providers.Provider()

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        self.assertIs(self.provider.overridden[-1], overriding_provider2)

        self.provider.reset_last_overriding()
        self.assertIs(self.provider.overridden[-1], overriding_provider1)

        self.provider.reset_last_overriding()
        self.assertFalse(self.provider.overridden)

    def test_reset_last_overriding_of_not_overridden_provider(self):
        self.assertRaises(errors.Error, self.provider.reset_last_overriding)

    def test_reset_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)

        self.assertTrue(self.provider.overridden)
        self.assertEqual(self.provider.overridden, (overriding_provider,))

        self.provider.reset_override()

        self.assertEqual(self.provider.overridden, tuple())

    def test_repr(self):
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.base.'
                         'Provider() at {0}>'.format(hex(id(self.provider))))
