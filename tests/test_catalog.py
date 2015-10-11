"""Dependency injector catalog unittests."""

import unittest2 as unittest
import dependency_injector as di


class CatalogsInheritanceTests(unittest.TestCase):
    """Catalogs inheritance tests."""

    class CatalogA(di.AbstractCatalog):
        """Test catalog A."""

        p11 = di.Provider()
        p12 = di.Provider()

    class CatalogB(CatalogA):
        """Test catalog B."""

        p21 = di.Provider()
        p22 = di.Provider()

    class CatalogC(CatalogB):
        """Test catalog C."""

        p31 = di.Provider()
        p32 = di.Provider()

    def test_cls_providers(self):
        """Test `di.AbstractCatalog.cls_providers` contents."""
        self.assertDictEqual(self.CatalogA.cls_providers,
                             dict(p11=self.CatalogA.p11,
                                  p12=self.CatalogA.p12))
        self.assertDictEqual(self.CatalogB.cls_providers,
                             dict(p21=self.CatalogB.p21,
                                  p22=self.CatalogB.p22))
        self.assertDictEqual(self.CatalogC.cls_providers,
                             dict(p31=self.CatalogC.p31,
                                  p32=self.CatalogC.p32))

    def test_inherited_providers(self):
        """Test `di.AbstractCatalog.inherited_providers` contents."""
        self.assertDictEqual(self.CatalogA.inherited_providers, dict())
        self.assertDictEqual(self.CatalogB.inherited_providers,
                             dict(p11=self.CatalogA.p11,
                                  p12=self.CatalogA.p12))
        self.assertDictEqual(self.CatalogC.inherited_providers,
                             dict(p11=self.CatalogA.p11,
                                  p12=self.CatalogA.p12,
                                  p21=self.CatalogB.p21,
                                  p22=self.CatalogB.p22))

    def test_providers(self):
        """Test `di.AbstractCatalog.inherited_providers` contents."""
        self.assertDictEqual(self.CatalogA.providers,
                             dict(p11=self.CatalogA.p11,
                                  p12=self.CatalogA.p12))
        self.assertDictEqual(self.CatalogB.providers,
                             dict(p11=self.CatalogA.p11,
                                  p12=self.CatalogA.p12,
                                  p21=self.CatalogB.p21,
                                  p22=self.CatalogB.p22))
        self.assertDictEqual(self.CatalogC.providers,
                             dict(p11=self.CatalogA.p11,
                                  p12=self.CatalogA.p12,
                                  p21=self.CatalogB.p21,
                                  p22=self.CatalogB.p22,
                                  p31=self.CatalogC.p31,
                                  p32=self.CatalogC.p32))


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

    def test_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(self.Catalog.filter(di.Object)) == 2)
        self.assertTrue(len(self.Catalog.filter(di.Value)) == 0)


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
