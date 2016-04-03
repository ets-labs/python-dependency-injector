"""Dependency injector catalogs overriding unittests."""

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


class OverrideTests(unittest.TestCase):
    """Catalog overriding and override decorator test cases."""

    def tearDown(self):
        """Tear test environment down."""
        CatalogA.reset_override()

    def test_overriding(self):
        """Test catalog overriding with another catalog."""
        @catalogs.override(CatalogA)
        class OverridingCatalog(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = providers.Value(1)
            p12 = providers.Value(2)

        self.assertEqual(CatalogA.p11(), 1)
        self.assertEqual(CatalogA.p12(), 2)
        self.assertEqual(len(CatalogA.overridden_by), 1)

    def test_override_declarative_catalog_with_itself(self):
        """Test catalog overriding of declarative catalog with itself."""
        with self.assertRaises(errors.Error):
            CatalogA.override(CatalogA)

    def test_override_declarative_catalog_with_subclass(self):
        """Test catalog overriding of declarative catalog with subclass."""
        with self.assertRaises(errors.Error):
            CatalogB.override(CatalogA)

    def test_override_dynamic_catalog_with_itself(self):
        """Test catalog overriding of dynamic catalog with itself."""
        catalog = catalogs.DynamicCatalog(p11=providers.Value(1),
                                          p12=providers.Value(2))
        with self.assertRaises(errors.Error):
            catalog.override(catalog)

    def test_overriding_with_dynamic_catalog(self):
        """Test catalog overriding with another dynamic catalog."""
        CatalogA.override(catalogs.DynamicCatalog(p11=providers.Value(1),
                                                  p12=providers.Value(2)))
        self.assertEqual(CatalogA.p11(), 1)
        self.assertEqual(CatalogA.p12(), 2)
        self.assertEqual(len(CatalogA.overridden_by), 1)

    def test_is_overridden(self):
        """Test catalog is_overridden property."""
        self.assertFalse(CatalogA.is_overridden)

        @catalogs.override(CatalogA)
        class OverridingCatalog(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

        self.assertTrue(CatalogA.is_overridden)

    def test_last_overriding(self):
        """Test catalog last_overriding property."""
        @catalogs.override(CatalogA)
        class OverridingCatalog1(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

        @catalogs.override(CatalogA)
        class OverridingCatalog2(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

        self.assertIs(CatalogA.last_overriding, OverridingCatalog2)

    def test_last_overriding_on_not_overridden(self):
        """Test catalog last_overriding property on not overridden catalog."""
        self.assertIsNone(CatalogA.last_overriding)

    def test_reset_last_overriding(self):
        """Test resetting last overriding catalog."""
        @catalogs.override(CatalogA)
        class OverridingCatalog1(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = providers.Value(1)
            p12 = providers.Value(2)

        @catalogs.override(CatalogA)
        class OverridingCatalog2(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = providers.Value(3)
            p12 = providers.Value(4)

        CatalogA.reset_last_overriding()

        self.assertEqual(CatalogA.p11(), 1)
        self.assertEqual(CatalogA.p12(), 2)

    def test_reset_last_overriding_when_not_overridden(self):
        """Test resetting last overriding catalog when it is not overridden."""
        with self.assertRaises(errors.Error):
            CatalogA.reset_last_overriding()

    def test_reset_override(self):
        """Test resetting all catalog overrides."""
        @catalogs.override(CatalogA)
        class OverridingCatalog1(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = providers.Value(1)
            p12 = providers.Value(2)

        @catalogs.override(CatalogA)
        class OverridingCatalog2(catalogs.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = providers.Value(3)
            p12 = providers.Value(4)

        CatalogA.reset_override()

        self.assertFalse(CatalogA.p11.is_overridden)
        self.assertFalse(CatalogA.p12.is_overridden)
