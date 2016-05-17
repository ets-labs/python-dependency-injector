"""Dependency injector static providers unittests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    utils,
)


class ObjectProviderTests(unittest.TestCase):
    """Object provider tests."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(providers.Object(object())))

    def test_call_object_provider(self):
        """Test provider call."""
        obj = object()
        self.assertIs(providers.Object(obj)(), obj)

    def test_call_overridden_object_provider(self):
        """Test overridden provider call."""
        obj1 = object()
        obj2 = object()
        provider = providers.Object(obj1)
        provider.override(providers.Object(obj2))
        self.assertIs(provider(), obj2)

    def test_repr(self):
        """Test representation of provider."""
        some_object = object()
        provider = providers.Object(some_object)
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.base.'
                         'Object({0}) at {1}>'.format(
                             repr(some_object),
                             hex(id(provider))))
