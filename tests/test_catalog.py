"""Objects catalog unittests."""

import unittest2 as unittest

from objects.catalog import AbstractCatalog
from objects.catalog import overrides

from objects.providers import Object
from objects.providers import Value

from objects.errors import Error


class CatalogTests(unittest.TestCase):

    """Catalog test cases."""

    class Catalog(AbstractCatalog):

        """Test catalog."""

        obj = Object(object())
        another_obj = Object(object())

    def test_get_used(self):
        """Test retrieving used provider."""
        catalog = self.Catalog(self.Catalog.obj)
        self.assertIsInstance(catalog.obj(), object)

    def test_get_unused(self):
        """Test retrieving unused provider."""
        catalog = self.Catalog()
        self.assertRaises(Error, getattr, catalog, 'obj')

    def test_all_providers(self):
        """Test getting of all catalog providers."""
        all_providers = self.Catalog.all_providers()
        all_providers_dict = dict(all_providers)

        self.assertIsInstance(all_providers, set)
        self.assertTrue(len(all_providers) == 2)

        self.assertIn('obj', all_providers_dict)
        self.assertIn(self.Catalog.obj, all_providers_dict.values())

        self.assertIn('another_obj', all_providers_dict)
        self.assertIn(self.Catalog.another_obj, all_providers_dict.values())

    def test_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(self.Catalog.all_providers(Object)) == 2)
        self.assertTrue(len(self.Catalog.all_providers(Value)) == 0)

    def test_overriding(self):
        """Test catalog overriding with another catalog."""
        @overrides(self.Catalog)
        class OverridingCatalog(self.Catalog):

            """Overriding catalog."""

            obj = Value(1)
            another_obj = Value(2)

        self.assertEqual(self.Catalog.obj(), 1)
        self.assertEqual(self.Catalog.another_obj(), 2)
