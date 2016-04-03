"""Dependency injector static providers unittests."""

import unittest2 as unittest

from dependency_injector import providers
from dependency_injector import utils


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
                         '<dependency_injector.providers.static.'
                         'Class({0}) at {1}>'.format(
                             repr(object),
                             hex(id(class_provider))))

        some_object = object()
        object_provider = providers.Object(some_object)
        self.assertEqual(repr(object_provider),
                         '<dependency_injector.providers.static.'
                         'Object({0}) at {1}>'.format(
                             repr(some_object),
                             hex(id(object_provider))))

        function_provider = providers.Function(map)
        self.assertEqual(repr(function_provider),
                         '<dependency_injector.providers.static.'
                         'Function({0}) at {1}>'.format(
                             repr(map),
                             hex(id(function_provider))))

        value_provider = providers.Value(123)
        self.assertEqual(repr(value_provider),
                         '<dependency_injector.providers.static.'
                         'Value({0}) at {1}>'.format(
                             repr(123),
                             hex(id(value_provider))))
