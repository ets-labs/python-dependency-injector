"""Dependency injector dynamic catalog unittests."""

import unittest2 as unittest

from dependency_injector import (
    catalogs,
    providers,
    errors,
)


class DynamicCatalogTests(unittest.TestCase):
    """Dynamic catalog tests."""

    catalog = None
    """:type: di.DynamicCatalog"""

    def setUp(self):
        """Set test environment up."""
        self.catalog = catalogs.DynamicCatalog(p1=providers.Provider(),
                                               p2=providers.Provider())

    def test_providers(self):
        """Test `di.DeclarativeCatalog.inherited_providers` contents."""
        self.assertDictEqual(self.catalog.providers,
                             dict(p1=self.catalog.p1,
                                  p2=self.catalog.p2))

    def test_bind_provider(self):
        """Test setting of provider via bind_provider() to catalog."""
        px = providers.Provider()
        py = providers.Provider()

        self.catalog.bind_provider('px', px)
        self.catalog.bind_provider('py', py)

        self.assertIs(self.catalog.px, px)
        self.assertIs(self.catalog.get_provider('px'), px)

        self.assertIs(self.catalog.py, py)
        self.assertIs(self.catalog.get_provider('py'), py)

    def test_bind_existing_provider(self):
        """Test setting of provider via bind_provider() to catalog."""
        with self.assertRaises(errors.Error):
            self.catalog.bind_provider('p1', providers.Factory(object))

    def test_force_bind_existing_provider(self):
        """Test setting of provider via bind_provider() to catalog."""
        p1 = providers.Factory(object)
        self.catalog.bind_provider('p1', p1, force=True)
        self.assertIs(self.catalog.p1, p1)

    def test_bind_provider_with_valid_provided_type(self):
        """Test setting of provider with provider type restriction."""
        class SomeProvider(providers.Provider):
            """Some provider."""

        class SomeCatalog(catalogs.DynamicCatalog):
            """Some catalog with provider type restriction."""

            provider_type = SomeProvider

        px = SomeProvider()
        py = SomeProvider()
        catalog = SomeCatalog()

        catalog.bind_provider('px', px)
        catalog.py = py

        self.assertIs(catalog.px, px)
        self.assertIs(catalog.get_provider('px'), px)

        self.assertIs(catalog.py, py)
        self.assertIs(catalog.get_provider('py'), py)

    def test_bind_provider_with_invalid_provided_type(self):
        """Test setting of provider with provider type restriction."""
        class SomeProvider(providers.Provider):
            """Some provider."""

        class SomeCatalog(catalogs.DynamicCatalog):
            """Some catalog with provider type restriction."""

            provider_type = SomeProvider

        px = providers.Provider()
        catalog = SomeCatalog()

        with self.assertRaises(errors.Error):
            catalog.bind_provider('px', px)

        with self.assertRaises(errors.Error):
            catalog.px = px

        with self.assertRaises(errors.Error):
            catalog.bind_providers(dict(px=px))

    def test_bind_providers(self):
        """Test setting of provider via bind_providers() to catalog."""
        px = providers.Provider()
        py = providers.Provider()

        self.catalog.bind_providers(dict(px=px, py=py))

        self.assertIs(self.catalog.px, px)
        self.assertIs(self.catalog.get_provider('px'), px)

        self.assertIs(self.catalog.py, py)
        self.assertIs(self.catalog.get_provider('py'), py)

    def test_bind_providers_with_existing(self):
        """Test setting of provider via bind_providers() to catalog."""
        with self.assertRaises(errors.Error):
            self.catalog.bind_providers(dict(p1=providers.Factory(object)))

    def test_bind_providers_force(self):
        """Test setting of provider via bind_providers() to catalog."""
        p1 = providers.Factory(object)
        self.catalog.bind_providers(dict(p1=p1), force=True)
        self.assertIs(self.catalog.p1, p1)

    def test_setattr(self):
        """Test setting of providers via attributes to catalog."""
        px = providers.Provider()
        py = providers.Provider()

        self.catalog.px = px
        self.catalog.py = py

        self.assertIs(self.catalog.px, px)
        self.assertIs(self.catalog.get_provider('px'), px)

        self.assertIs(self.catalog.py, py)
        self.assertIs(self.catalog.get_provider('py'), py)

    def test_unbind_provider(self):
        """Test that catalog unbinds provider correct."""
        self.catalog.px = providers.Provider()
        self.catalog.unbind_provider('px')
        self.assertFalse(self.catalog.has_provider('px'))

    def test_unbind_via_delattr(self):
        """Test that catalog unbinds provider correct."""
        self.catalog.px = providers.Provider()
        del self.catalog.px
        self.assertFalse(self.catalog.has_provider('px'))

    def test_provider_is_bound(self):
        """Test that providers are bound to the catalogs."""
        self.assertTrue(self.catalog.is_provider_bound(self.catalog.p1))
        self.assertEquals(
            self.catalog.get_provider_bind_name(self.catalog.p1), 'p1')
        self.assertTrue(self.catalog.is_provider_bound(self.catalog.p2))
        self.assertEquals(
            self.catalog.get_provider_bind_name(self.catalog.p2), 'p2')

    def test_provider_binding_to_different_catalogs(self):
        """Test that provider could be bound to different catalogs."""
        p1 = self.catalog.p1
        p2 = self.catalog.p2

        catalog_a = catalogs.DynamicCatalog(pa1=p1, pa2=p2)
        catalog_b = catalogs.DynamicCatalog(pb1=p1, pb2=p2)

        self.assertTrue(self.catalog.is_provider_bound(p1))
        self.assertTrue(catalog_a.is_provider_bound(p1))
        self.assertTrue(catalog_b.is_provider_bound(p1))
        self.assertEquals(self.catalog.get_provider_bind_name(p1), 'p1')
        self.assertEquals(catalog_a.get_provider_bind_name(p1), 'pa1')
        self.assertEquals(catalog_b.get_provider_bind_name(p1), 'pb1')

        self.assertTrue(self.catalog.is_provider_bound(p2))
        self.assertTrue(catalog_a.is_provider_bound(p2))
        self.assertTrue(catalog_b.is_provider_bound(p2))
        self.assertEquals(self.catalog.get_provider_bind_name(p2), 'p2')
        self.assertEquals(catalog_a.get_provider_bind_name(p2), 'pa2')
        self.assertEquals(catalog_b.get_provider_bind_name(p2), 'pb2')

    def test_provider_rebinding_to_the_same_catalog(self):
        """Test provider rebinding to the same catalog."""
        with self.assertRaises(errors.Error):
            self.catalog.p3 = self.catalog.p1

    def test_provider_binding_with_the_same_name(self):
        """Test binding of provider with the same name."""
        with self.assertRaises(errors.Error):
            self.catalog.bind_provider('p1', providers.Provider())

    def test_get(self):
        """Test getting of providers using get() method."""
        self.assertIs(self.catalog.get_provider('p1'), self.catalog.p1)
        self.assertIs(self.catalog.get_provider('p2'), self.catalog.p2)

    def test_get_undefined(self):
        """Test getting of undefined providers using get() method."""
        with self.assertRaises(errors.UndefinedProviderError):
            self.catalog.get_provider('undefined')

        with self.assertRaises(errors.UndefinedProviderError):
            self.catalog.undefined

    def test_has_provider(self):
        """Test checks of providers availability in catalog."""
        self.assertTrue(self.catalog.has_provider('p1'))
        self.assertTrue(self.catalog.has_provider('p2'))
        self.assertFalse(self.catalog.has_provider('undefined'))

    def test_filter_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(self.catalog.filter(providers.Provider)) == 2)
        self.assertTrue(len(self.catalog.filter(providers.Object)) == 0)

    def test_repr(self):
        """Test catalog representation."""
        representation = repr(self.catalog)

        self.assertIn('dependency_injector.catalogs.dynamic.DynamicCatalog',
                      representation)
        self.assertIn('p1', representation)
        self.assertIn('p2', representation)
