"""Dependency injector catalog unittests."""

import unittest2 as unittest
import dependency_injector as di


class CatalogTests(unittest.TestCase):

    """Catalog test cases."""

    class Catalog(di.AbstractCatalog):

        """Test catalog."""

        obj = di.Object(object())
        another_obj = di.Object(object())

    def test_get_used(self):
        """Test retrieving used provider."""
        catalog = self.Catalog(self.Catalog.obj)
        self.assertIsInstance(catalog.obj(), object)

    def test_get_unused(self):
        """Test retrieving unused provider."""
        catalog = self.Catalog()
        self.assertRaises(di.Error, getattr, catalog, 'obj')

    def test_all_providers(self):
        """Test getting of all catalog providers."""
        self.assertTrue(len(self.Catalog.providers) == 2)

        self.assertIn('obj', self.Catalog.providers)
        self.assertIn(self.Catalog.obj, self.Catalog.providers.values())

        self.assertIn('another_obj', self.Catalog.providers)
        self.assertIn(self.Catalog.another_obj,
                      self.Catalog.providers.values())

    def test_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(self.Catalog.filter(di.Object)) == 2)
        self.assertTrue(len(self.Catalog.filter(di.Value)) == 0)

    def test_metaclass_with_several_catalogs(self):
        """Test that metaclass work well with several catalogs."""
        class Catalog1(di.AbstractCatalog):

            """Catalog1."""

            provider = di.Object(object())

        class Catalog2(di.AbstractCatalog):

            """Catalog2."""

            provider = di.Object(object())

        self.assertTrue(len(Catalog1.providers) == 1)
        self.assertIs(Catalog1.provider, Catalog1.providers['provider'])

        self.assertTrue(len(Catalog2.providers) == 1)
        self.assertIs(Catalog2.provider, Catalog2.providers['provider'])

        self.assertIsNot(Catalog1.provider, Catalog2.provider)


class OverrideTests(unittest.TestCase):

    """Override decorator test cases."""

    class Catalog(di.AbstractCatalog):

        """Test catalog."""

        obj = di.Object(object())
        another_obj = di.Object(object())

    def test_overriding(self):
        """Test catalog overriding with another catalog."""
        @di.override(self.Catalog)
        class OverridingCatalog(self.Catalog):

            """Overriding catalog."""

            obj = di.Value(1)
            another_obj = di.Value(2)

        self.assertEqual(self.Catalog.obj(), 1)
        self.assertEqual(self.Catalog.another_obj(), 2)
