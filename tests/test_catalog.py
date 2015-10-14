"""Dependency injector catalog unittests."""

import unittest2 as unittest
import dependency_injector as di


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


class CatalogsInheritanceTests(unittest.TestCase):
    """Catalogs inheritance tests."""

    def test_cls_providers(self):
        """Test `di.AbstractCatalog.cls_providers` contents."""
        self.assertDictEqual(CatalogA.cls_providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12))
        self.assertDictEqual(CatalogB.cls_providers,
                             dict(p21=CatalogB.p21,
                                  p22=CatalogB.p22))
        self.assertDictEqual(CatalogC.cls_providers,
                             dict(p31=CatalogC.p31,
                                  p32=CatalogC.p32))

    def test_inherited_providers(self):
        """Test `di.AbstractCatalog.inherited_providers` contents."""
        self.assertDictEqual(CatalogA.inherited_providers, dict())
        self.assertDictEqual(CatalogB.inherited_providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12))
        self.assertDictEqual(CatalogC.inherited_providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12,
                                  p21=CatalogB.p21,
                                  p22=CatalogB.p22))

    def test_providers(self):
        """Test `di.AbstractCatalog.inherited_providers` contents."""
        self.assertDictEqual(CatalogA.providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12))
        self.assertDictEqual(CatalogB.providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12,
                                  p21=CatalogB.p21,
                                  p22=CatalogB.p22))
        self.assertDictEqual(CatalogC.providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12,
                                  p21=CatalogB.p21,
                                  p22=CatalogB.p22,
                                  p31=CatalogC.p31,
                                  p32=CatalogC.p32))


class _BasicSubsetTests(object):
    """Catalog subset test cases."""

    def test_get_attr_from_subset(self):
        """Test get providers (attribute) from subset."""
        self.assertIs(self.subset.p11, CatalogC.p11)
        self.assertIs(self.subset.p12, CatalogC.p12)

    def test_get_attr_not_from_subset(self):
        """Test get providers (attribute) that are not in subset."""
        self.assertRaises(di.Error, getattr, self.subset, 'p21')
        self.assertRaises(di.Error, getattr, self.subset, 'p22')
        self.assertRaises(di.Error, getattr, self.subset, 'p31')
        self.assertRaises(di.Error, getattr, self.subset, 'p32')

    def test_get_method_from_subset(self):
        """Test get providers (get() method) from subset."""
        self.assertIs(self.subset.get('p11'), CatalogC.p11)
        self.assertIs(self.subset.get('p12'), CatalogC.p12)

    def test_get_method_not_from_subset(self):
        """Test get providers (get() method) that are not in subset."""
        self.assertRaises(di.Error, self.subset.get, 'p21')
        self.assertRaises(di.Error, self.subset.get, 'p22')
        self.assertRaises(di.Error, self.subset.get, 'p31')
        self.assertRaises(di.Error, self.subset.get, 'p32')

    def test_has(self):
        """Test checks of providers availability in subsets."""
        self.assertTrue(self.subset.has('p11'))
        self.assertTrue(self.subset.has('p12'))

        self.assertFalse(self.subset.has('p21'))
        self.assertFalse(self.subset.has('p22'))
        self.assertFalse(self.subset.has('p31'))
        self.assertFalse(self.subset.has('p32'))


class SubsetCatalogFactoryTests(_BasicSubsetTests, unittest.TestCase):
    """Subset, that is created by catalog factory method, tests."""

    def setUp(self):
        """Set test environment up."""
        self.subset = CatalogC.subset('p11', 'p12')


class SubsetProvidersAggregationTests(_BasicSubsetTests, unittest.TestCase):
    """Subset, that is created catalog providers aggregation method, tests."""

    def setUp(self):
        """Set test environment up."""
        self.subset = di.Subset(CatalogC.p11,
                                CatalogC.p12)


class CatalogTests(unittest.TestCase):
    """Catalog test cases."""

    def test_get(self):
        """Test getting of providers using get() method."""
        self.assertIs(CatalogC.get('p11'), CatalogC.p11)
        self.assertIs(CatalogC.get('p12'), CatalogC.p12)
        self.assertIs(CatalogC.get('p22'), CatalogC.p22)
        self.assertIs(CatalogC.get('p22'), CatalogC.p22)
        self.assertIs(CatalogC.get('p32'), CatalogC.p32)
        self.assertIs(CatalogC.get('p32'), CatalogC.p32)

    def test_get_undefined(self):
        """Test getting of undefined providers using get() method."""
        self.assertRaises(di.Error, CatalogC.get, 'undefined')

    def test_has(self):
        """Test checks of providers availability in subsets."""
        self.assertTrue(CatalogC.has('p11'))
        self.assertTrue(CatalogC.has('p12'))
        self.assertTrue(CatalogC.has('p21'))
        self.assertTrue(CatalogC.has('p22'))
        self.assertTrue(CatalogC.has('p31'))
        self.assertTrue(CatalogC.has('p32'))
        self.assertFalse(CatalogC.has('undefined'))

    def test_is_subset_owner(self):
        """Test that catalog is subset owner."""
        subset1 = CatalogA.subset('p11')
        self.assertTrue(CatalogA.is_subset_owner(subset1))
        self.assertFalse(CatalogB.is_subset_owner(subset1))
        self.assertFalse(CatalogC.is_subset_owner(subset1))

        subset2 = di.Subset(CatalogA.p11)
        self.assertTrue(CatalogA.is_subset_owner(subset2))
        self.assertFalse(CatalogB.is_subset_owner(subset2))
        self.assertFalse(CatalogC.is_subset_owner(subset2))

    def test_filter_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(CatalogC.filter(di.Provider)) == 6)
        self.assertTrue(len(CatalogC.filter(di.Value)) == 0)


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
