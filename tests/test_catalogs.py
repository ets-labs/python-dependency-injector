"""Dependency injector catalogs unittests."""

import unittest2 as unittest

from dependency_injector import catalogs
from dependency_injector import providers
from dependency_injector import errors


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


class DynamicCatalogTests(unittest.TestCase):
    """Dynamic catalog tests."""

    catalog = None
    """:type: di.DynamicCatalog"""

    def setUp(self):
        """Set test environment up."""
        self.catalog = catalogs.DynamicCatalog(p1=providers.Provider(),
                                               p2=providers.Provider())
        self.catalog.name = 'TestCatalog'

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

    def test_bind_providers(self):
        """Test setting of provider via bind_providers() to catalog."""
        px = providers.Provider()
        py = providers.Provider()

        self.catalog.bind_providers(dict(px=px, py=py))

        self.assertIs(self.catalog.px, px)
        self.assertIs(self.catalog.get_provider('px'), px)

        self.assertIs(self.catalog.py, py)
        self.assertIs(self.catalog.get_provider('py'), py)

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
        self.assertTrue(len(self.catalog.filter(providers.Value)) == 0)

    def test_repr(self):
        """Test catalog representation."""
        self.assertIn('TestCatalog', repr(self.catalog))
        self.assertIn('p1', repr(self.catalog))
        self.assertIn('p2', repr(self.catalog))


class DeclarativeCatalogTests(unittest.TestCase):
    """Declarative catalog tests."""

    def test_cls_providers(self):
        """Test `di.DeclarativeCatalog.cls_providers` contents."""
        self.assertDictEqual(CatalogA.cls_providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12))
        self.assertDictEqual(CatalogB.cls_providers,
                             dict(p21=CatalogB.p21,
                                  p22=CatalogB.p22))

    def test_inherited_providers(self):
        """Test `di.DeclarativeCatalog.inherited_providers` contents."""
        self.assertDictEqual(CatalogA.inherited_providers, dict())
        self.assertDictEqual(CatalogB.inherited_providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12))

    def test_providers(self):
        """Test `di.DeclarativeCatalog.inherited_providers` contents."""
        self.assertDictEqual(CatalogA.providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12))
        self.assertDictEqual(CatalogB.providers,
                             dict(p11=CatalogA.p11,
                                  p12=CatalogA.p12,
                                  p21=CatalogB.p21,
                                  p22=CatalogB.p22))

    def test_bind_provider(self):
        """Test setting of provider via bind_provider() to catalog."""
        px = providers.Provider()
        py = providers.Provider()

        CatalogA.bind_provider('px', px)
        CatalogA.bind_provider('py', py)

        self.assertIs(CatalogA.px, px)
        self.assertIs(CatalogA.get_provider('px'), px)

        self.assertIs(CatalogA.py, py)
        self.assertIs(CatalogA.get_provider('py'), py)

        del CatalogA.px
        del CatalogA.py

    def test_bind_providers(self):
        """Test setting of provider via bind_providers() to catalog."""
        px = providers.Provider()
        py = providers.Provider()

        CatalogB.bind_providers(dict(px=px, py=py))

        self.assertIs(CatalogB.px, px)
        self.assertIs(CatalogB.get_provider('px'), px)

        self.assertIs(CatalogB.py, py)
        self.assertIs(CatalogB.get_provider('py'), py)

        del CatalogB.px
        del CatalogB.py

    def test_setattr(self):
        """Test setting of providers via attributes to catalog."""
        px = providers.Provider()
        py = providers.Provider()

        CatalogB.px = px
        CatalogB.py = py

        self.assertIs(CatalogB.px, px)
        self.assertIs(CatalogB.get_provider('px'), px)

        self.assertIs(CatalogB.py, py)
        self.assertIs(CatalogB.get_provider('py'), py)

        del CatalogB.px
        del CatalogB.py

    def test_unbind_provider(self):
        """Test that catalog unbinds provider correct."""
        CatalogB.px = providers.Provider()
        CatalogB.unbind_provider('px')
        self.assertFalse(CatalogB.has_provider('px'))

    def test_unbind_via_delattr(self):
        """Test that catalog unbinds provider correct."""
        CatalogB.px = providers.Provider()
        del CatalogB.px
        self.assertFalse(CatalogB.has_provider('px'))

    def test_provider_is_bound(self):
        """Test that providers are bound to the catalogs."""
        self.assertTrue(CatalogA.is_provider_bound(CatalogA.p11))
        self.assertEquals(CatalogA.get_provider_bind_name(CatalogA.p11), 'p11')

        self.assertTrue(CatalogA.is_provider_bound(CatalogA.p12))
        self.assertEquals(CatalogA.get_provider_bind_name(CatalogA.p12), 'p12')

    def test_provider_binding_to_different_catalogs(self):
        """Test that provider could be bound to different catalogs."""
        p11 = CatalogA.p11
        p12 = CatalogA.p12

        class CatalogD(catalogs.DeclarativeCatalog):
            """Test catalog."""

            pd1 = p11
            pd2 = p12

        class CatalogE(catalogs.DeclarativeCatalog):
            """Test catalog."""

            pe1 = p11
            pe2 = p12

        self.assertTrue(CatalogA.is_provider_bound(p11))
        self.assertTrue(CatalogD.is_provider_bound(p11))
        self.assertTrue(CatalogE.is_provider_bound(p11))
        self.assertEquals(CatalogA.get_provider_bind_name(p11), 'p11')
        self.assertEquals(CatalogD.get_provider_bind_name(p11), 'pd1')
        self.assertEquals(CatalogE.get_provider_bind_name(p11), 'pe1')

        self.assertTrue(CatalogA.is_provider_bound(p12))
        self.assertTrue(CatalogD.is_provider_bound(p12))
        self.assertTrue(CatalogE.is_provider_bound(p12))
        self.assertEquals(CatalogA.get_provider_bind_name(p12), 'p12')
        self.assertEquals(CatalogD.get_provider_bind_name(p12), 'pd2')
        self.assertEquals(CatalogE.get_provider_bind_name(p12), 'pe2')

    def test_provider_rebinding_to_the_same_catalog(self):
        """Test provider rebinding to the same catalog."""
        with self.assertRaises(errors.Error):
            class TestCatalog(catalogs.DeclarativeCatalog):
                """Test catalog."""

                p1 = providers.Provider()
                p2 = p1

    def test_provider_rebinding_to_the_same_catalogs_hierarchy(self):
        """Test provider rebinding to the same catalogs hierarchy."""
        class TestCatalog1(catalogs.DeclarativeCatalog):
            """Test catalog."""

            p1 = providers.Provider()

        with self.assertRaises(errors.Error):
            class TestCatalog2(TestCatalog1):
                """Test catalog."""

                p2 = TestCatalog1.p1

    def test_get(self):
        """Test getting of providers using get() method."""
        self.assertIs(CatalogB.get('p11'), CatalogB.p11)
        self.assertIs(CatalogB.get('p12'), CatalogB.p12)
        self.assertIs(CatalogB.get('p22'), CatalogB.p22)
        self.assertIs(CatalogB.get('p22'), CatalogB.p22)

        self.assertIs(CatalogB.get_provider('p11'), CatalogB.p11)
        self.assertIs(CatalogB.get_provider('p12'), CatalogB.p12)
        self.assertIs(CatalogB.get_provider('p22'), CatalogB.p22)
        self.assertIs(CatalogB.get_provider('p22'), CatalogB.p22)

    def test_get_undefined(self):
        """Test getting of undefined providers using get() method."""
        with self.assertRaises(errors.UndefinedProviderError):
            CatalogB.get('undefined')

        with self.assertRaises(errors.UndefinedProviderError):
            CatalogB.get_provider('undefined')

        with self.assertRaises(errors.UndefinedProviderError):
            CatalogB.undefined

    def test_has(self):
        """Test checks of providers availability in catalog."""
        self.assertTrue(CatalogB.has('p11'))
        self.assertTrue(CatalogB.has('p12'))
        self.assertTrue(CatalogB.has('p21'))
        self.assertTrue(CatalogB.has('p22'))
        self.assertFalse(CatalogB.has('undefined'))

        self.assertTrue(CatalogB.has_provider('p11'))
        self.assertTrue(CatalogB.has_provider('p12'))
        self.assertTrue(CatalogB.has_provider('p21'))
        self.assertTrue(CatalogB.has_provider('p22'))
        self.assertFalse(CatalogB.has_provider('undefined'))

    def test_filter_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(CatalogB.filter(providers.Provider)) == 4)
        self.assertTrue(len(CatalogB.filter(providers.Value)) == 0)

    def test_repr(self):
        """Test catalog representation."""
        self.assertIn('CatalogA', repr(CatalogA))
        self.assertIn('p11', repr(CatalogA))
        self.assertIn('p12', repr(CatalogA))

        self.assertIn('CatalogB', repr(CatalogB))
        self.assertIn('p11', repr(CatalogB))
        self.assertIn('p12', repr(CatalogB))
        self.assertIn('p21', repr(CatalogB))
        self.assertIn('p22', repr(CatalogB))

    def test_abstract_catalog_backward_compatibility(self):
        """Test that di.AbstractCatalog is available."""
        self.assertIs(catalogs.DeclarativeCatalog, catalogs.AbstractCatalog)


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


class CatalogModuleBackwardCompatibility(unittest.TestCase):
    """Backward compatibility test of catalog module."""

    def test_import_catalog(self):
        """Test that module `catalog` is the same as `catalogs`."""
        from dependency_injector import catalog
        from dependency_injector import catalogs

        self.assertIs(catalog, catalogs)
