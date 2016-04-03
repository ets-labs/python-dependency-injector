"""Dependency injector catalog bundles unittests."""

import unittest2 as unittest

from dependency_injector import (
    catalogs,
    providers,
    errors,
)


class CatalogA(catalogs.DeclarativeCatalog):
    """Test catalog A."""

    p11 = providers.Provider()
    p12 = providers.Provider()


class CatalogB(CatalogA):
    """Test catalog B."""

    p21 = providers.Provider()
    p22 = providers.Provider()


class CatalogBundleTests(unittest.TestCase):
    """Catalog bundle test cases."""

    def setUp(self):
        """Set test environment up."""
        self.bundle = CatalogB.Bundle(CatalogB.p11,
                                      CatalogB.p12)

    def test_get_attr_from_bundle(self):
        """Test get providers (attribute) from catalog bundle."""
        self.assertIs(self.bundle.p11, CatalogA.p11)
        self.assertIs(self.bundle.p12, CatalogA.p12)

    def test_get_attr_not_from_bundle(self):
        """Test get providers (attribute) that are not in bundle."""
        self.assertRaises(errors.Error, getattr, self.bundle, 'p21')
        self.assertRaises(errors.Error, getattr, self.bundle, 'p22')

    def test_get_method_from_bundle(self):
        """Test get providers (get() method) from bundle."""
        self.assertIs(self.bundle.get_provider('p11'), CatalogB.p11)
        self.assertIs(self.bundle.get_provider('p12'), CatalogB.p12)

    def test_get_method_not_from_bundle(self):
        """Test get providers (get() method) that are not in bundle."""
        self.assertRaises(errors.Error, self.bundle.get_provider, 'p21')
        self.assertRaises(errors.Error, self.bundle.get_provider, 'p22')

    def test_has(self):
        """Test checks of providers availability in bundle."""
        self.assertTrue(self.bundle.has_provider('p11'))
        self.assertTrue(self.bundle.has_provider('p12'))

        self.assertFalse(self.bundle.has_provider('p21'))
        self.assertFalse(self.bundle.has_provider('p22'))

    def test_hasattr(self):
        """Test checks of providers availability in bundle."""
        self.assertTrue(hasattr(self.bundle, 'p11'))
        self.assertTrue(hasattr(self.bundle, 'p12'))

        self.assertFalse(hasattr(self.bundle, 'p21'))
        self.assertFalse(hasattr(self.bundle, 'p22'))

    def test_create_bundle_with_unbound_provider(self):
        """Test that bundle is not created with unbound provider."""
        self.assertRaises(errors.Error, CatalogB.Bundle, providers.Provider())

    def test_create_bundle_with_another_catalog_provider(self):
        """Test that bundle can not contain another catalog's provider."""
        class TestCatalog(catalogs.DeclarativeCatalog):
            """Test catalog."""

            provider = providers.Provider()

        self.assertRaises(errors.Error,
                          CatalogB.Bundle, CatalogB.p21, TestCatalog.provider)

    def test_create_bundle_with_another_catalog_provider_with_same_name(self):
        """Test that bundle can not contain another catalog's provider."""
        class TestCatalog(catalogs.DeclarativeCatalog):
            """Test catalog."""

            p21 = providers.Provider()

        self.assertRaises(errors.Error,
                          CatalogB.Bundle, CatalogB.p21, TestCatalog.p21)

    def test_is_bundle_owner(self):
        """Test that catalog bundle is owned by catalog."""
        self.assertTrue(CatalogB.is_bundle_owner(self.bundle))
        self.assertFalse(CatalogA.is_bundle_owner(self.bundle))

    def test_is_bundle_owner_with_not_bundle_instance(self):
        """Test that check of bundle ownership raises error with not bundle."""
        self.assertRaises(errors.Error, CatalogB.is_bundle_owner, object())
