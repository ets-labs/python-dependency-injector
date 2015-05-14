"""Objects decorators unittests."""

import unittest2 as unittest

from objects.decorators import override
from objects.decorators import inject

from objects.catalog import AbstractCatalog

from objects.providers import Factory
from objects.providers import Object
from objects.providers import Value

from objects.injections import KwArg

from objects.errors import Error


class OverrideTests(unittest.TestCase):

    """Override decorator test cases."""

    class Catalog(AbstractCatalog):

        """Test catalog."""

        obj = Object(object())
        another_obj = Object(object())

    def test_overriding(self):
        """Test catalog overriding with another catalog."""
        @override(self.Catalog)
        class OverridingCatalog(self.Catalog):

            """Overriding catalog."""

            obj = Value(1)
            another_obj = Value(2)

        self.assertEqual(self.Catalog.obj(), 1)
        self.assertEqual(self.Catalog.another_obj(), 2)


class InjectTests(unittest.TestCase):

    """Inject decorator test cases."""

    def test_decorated(self):
        """Test `inject()` decorated callback."""
        provider1 = Factory(object)
        provider2 = Factory(list)

        @inject(KwArg('a', provider1))
        @inject(KwArg('b', provider2))
        def test(a, b):
            return a, b

        a1, b1 = test()
        a2, b2 = test()

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIsNot(a1, a2)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_decorated_kwargs_priority(self):
        """Test `inject()` decorated callback kwargs priority."""
        provider1 = Factory(object)
        provider2 = Factory(list)
        object_a = object()

        @inject(KwArg('a', provider1))
        @inject(KwArg('b', provider2))
        def test(a, b):
            return a, b

        a1, b1 = test(a=object_a)
        a2, b2 = test(a=object_a)

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIs(a1, object_a)
        self.assertIs(a2, object_a)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_decorated_with_args(self):
        """Test `inject()` decorated callback with args."""
        provider = Factory(list)
        object_a = object()

        @inject(KwArg('b', provider))
        def test(a, b):
            return a, b

        a1, b1 = test(object_a)
        a2, b2 = test(object_a)

        self.assertIsInstance(a1, object)
        self.assertIsInstance(a2, object)
        self.assertIs(a1, object_a)
        self.assertIs(a2, object_a)

        self.assertIsInstance(b1, list)
        self.assertIsInstance(b2, list)
        self.assertIsNot(b1, b2)

    def test_decorate_with_not_injection(self):
        """Test `inject()` decorator with not an injection instance."""
        self.assertRaises(Error, inject, object)
