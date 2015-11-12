"""Dependency injector catalogs unittests."""

import unittest2 as unittest
import dependency_injector as di


class CatalogA(di.DeclarativeCatalog):
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


class CatalogBundleTests(unittest.TestCase):
    """Catalog bundle test cases."""

    def setUp(self):
        """Set test environment up."""
        self.bundle = CatalogC.Bundle(CatalogC.p11,
                                      CatalogC.p12)

    def test_get_attr_from_bundle(self):
        """Test get providers (attribute) from catalog bundle."""
        self.assertIs(self.bundle.p11, CatalogC.p11)
        self.assertIs(self.bundle.p12, CatalogC.p12)

    def test_get_attr_not_from_bundle(self):
        """Test get providers (attribute) that are not in bundle."""
        self.assertRaises(di.Error, getattr, self.bundle, 'p21')
        self.assertRaises(di.Error, getattr, self.bundle, 'p22')
        self.assertRaises(di.Error, getattr, self.bundle, 'p31')
        self.assertRaises(di.Error, getattr, self.bundle, 'p32')

    def test_get_method_from_bundle(self):
        """Test get providers (get() method) from bundle."""
        self.assertIs(self.bundle.get_provider('p11'), CatalogC.p11)
        self.assertIs(self.bundle.get_provider('p12'), CatalogC.p12)

    def test_get_method_not_from_bundle(self):
        """Test get providers (get() method) that are not in bundle."""
        self.assertRaises(di.Error, self.bundle.get_provider, 'p21')
        self.assertRaises(di.Error, self.bundle.get_provider, 'p22')
        self.assertRaises(di.Error, self.bundle.get_provider, 'p31')
        self.assertRaises(di.Error, self.bundle.get_provider, 'p32')

    def test_has(self):
        """Test checks of providers availability in bundle."""
        self.assertTrue(self.bundle.has_provider('p11'))
        self.assertTrue(self.bundle.has_provider('p12'))

        self.assertFalse(self.bundle.has_provider('p21'))
        self.assertFalse(self.bundle.has_provider('p22'))
        self.assertFalse(self.bundle.has_provider('p31'))
        self.assertFalse(self.bundle.has_provider('p32'))

    def test_hasattr(self):
        """Test checks of providers availability in bundle."""
        self.assertTrue(hasattr(self.bundle, 'p11'))
        self.assertTrue(hasattr(self.bundle, 'p12'))

        self.assertFalse(hasattr(self.bundle, 'p21'))
        self.assertFalse(hasattr(self.bundle, 'p22'))
        self.assertFalse(hasattr(self.bundle, 'p31'))
        self.assertFalse(hasattr(self.bundle, 'p31'))

    def test_create_bundle_with_unbound_provider(self):
        """Test that bundle is not created with unbound provider."""
        self.assertRaises(di.Error, CatalogC.Bundle, di.Provider())

    def test_create_bundle_with_another_catalog_provider(self):
        """Test that bundle can not contain another catalog's provider."""
        class TestCatalog(di.DeclarativeCatalog):
            """Test catalog."""

            provider = di.Provider()

        self.assertRaises(di.Error,
                          CatalogC.Bundle, CatalogC.p31, TestCatalog.provider)

    def test_create_bundle_with_another_catalog_provider_with_same_name(self):
        """Test that bundle can not contain another catalog's provider."""
        class TestCatalog(di.DeclarativeCatalog):
            """Test catalog."""

            p31 = di.Provider()

        self.assertRaises(di.Error,
                          CatalogC.Bundle, CatalogC.p31, TestCatalog.p31)

    def test_is_bundle_owner(self):
        """Test that catalog bundle is owned by catalog."""
        self.assertTrue(CatalogC.is_bundle_owner(self.bundle))
        self.assertFalse(CatalogB.is_bundle_owner(self.bundle))
        self.assertFalse(CatalogA.is_bundle_owner(self.bundle))

    def test_is_bundle_owner_with_not_bundle_instance(self):
        """Test that check of bundle ownership raises error with not bundle."""
        self.assertRaises(di.Error, CatalogC.is_bundle_owner, object())


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
        self.assertDictEqual(CatalogC.cls_providers,
                             dict(p31=CatalogC.p31,
                                  p32=CatalogC.p32))

    def test_inherited_providers(self):
        """Test `di.DeclarativeCatalog.inherited_providers` contents."""
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
        """Test `di.DeclarativeCatalog.inherited_providers` contents."""
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

    def test_bind_provider(self):
        """Test setting of provider via bind_provider() to catalog."""
        px = di.Provider()
        py = di.Provider()

        CatalogC.bind_provider('px', px)
        CatalogC.bind_provider('py', py)

        self.assertIs(CatalogC.px, px)
        self.assertIs(CatalogC.get_provider('px'), px)
        self.assertIs(CatalogC.catalog.px, px)

        self.assertIs(CatalogC.py, py)
        self.assertIs(CatalogC.get_provider('py'), py)
        self.assertIs(CatalogC.catalog.py, py)

        del CatalogC.px
        del CatalogC.py

    def test_bind_providers(self):
        """Test setting of provider via bind_providers() to catalog."""
        px = di.Provider()
        py = di.Provider()

        CatalogC.bind_providers(dict(px=px, py=py))

        self.assertIs(CatalogC.px, px)
        self.assertIs(CatalogC.get_provider('px'), px)
        self.assertIs(CatalogC.catalog.px, px)

        self.assertIs(CatalogC.py, py)
        self.assertIs(CatalogC.get_provider('py'), py)
        self.assertIs(CatalogC.catalog.py, py)

        del CatalogC.px
        del CatalogC.py

    def test_setattr(self):
        """Test setting of providers via attributes to catalog."""
        px = di.Provider()
        py = di.Provider()

        CatalogC.px = px
        CatalogC.py = py

        self.assertIs(CatalogC.px, px)
        self.assertIs(CatalogC.get_provider('px'), px)
        self.assertIs(CatalogC.catalog.px, px)

        self.assertIs(CatalogC.py, py)
        self.assertIs(CatalogC.get_provider('py'), py)
        self.assertIs(CatalogC.catalog.py, py)

        del CatalogC.px
        del CatalogC.py

    def test_unbind_provider(self):
        """Test that catalog unbinds provider correct."""
        CatalogC.px = di.Provider()
        CatalogC.unbind_provider('px')
        self.assertFalse(CatalogC.has_provider('px'))

    def test_unbind_via_delattr(self):
        """Test that catalog unbinds provider correct."""
        CatalogC.px = di.Provider()
        del CatalogC.px
        self.assertFalse(CatalogC.has_provider('px'))

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

        class CatalogD(di.DeclarativeCatalog):
            """Test catalog."""

            pd1 = p11
            pd2 = p12

        class CatalogE(di.DeclarativeCatalog):
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
        with self.assertRaises(di.Error):
            class TestCatalog(di.DeclarativeCatalog):
                """Test catalog."""

                p1 = di.Provider()
                p2 = p1

    def test_provider_rebinding_to_the_same_catalogs_hierarchy(self):
        """Test provider rebinding to the same catalogs hierarchy."""
        class TestCatalog1(di.DeclarativeCatalog):
            """Test catalog."""

            p1 = di.Provider()

        with self.assertRaises(di.Error):
            class TestCatalog2(TestCatalog1):
                """Test catalog."""

                p2 = TestCatalog1.p1

    def test_get(self):
        """Test getting of providers using get() method."""
        self.assertIs(CatalogC.get('p11'), CatalogC.p11)
        self.assertIs(CatalogC.get('p12'), CatalogC.p12)
        self.assertIs(CatalogC.get('p22'), CatalogC.p22)
        self.assertIs(CatalogC.get('p22'), CatalogC.p22)
        self.assertIs(CatalogC.get('p32'), CatalogC.p32)
        self.assertIs(CatalogC.get('p32'), CatalogC.p32)

        self.assertIs(CatalogC.get_provider('p11'), CatalogC.p11)
        self.assertIs(CatalogC.get_provider('p12'), CatalogC.p12)
        self.assertIs(CatalogC.get_provider('p22'), CatalogC.p22)
        self.assertIs(CatalogC.get_provider('p22'), CatalogC.p22)
        self.assertIs(CatalogC.get_provider('p32'), CatalogC.p32)
        self.assertIs(CatalogC.get_provider('p32'), CatalogC.p32)

    def test_get_undefined(self):
        """Test getting of undefined providers using get() method."""
        with self.assertRaises(di.UndefinedProviderError):
            CatalogC.get('undefined')

        with self.assertRaises(di.UndefinedProviderError):
            CatalogC.get_provider('undefined')

        with self.assertRaises(di.UndefinedProviderError):
            CatalogC.undefined

    def test_has(self):
        """Test checks of providers availability in catalog."""
        self.assertTrue(CatalogC.has('p11'))
        self.assertTrue(CatalogC.has('p12'))
        self.assertTrue(CatalogC.has('p21'))
        self.assertTrue(CatalogC.has('p22'))
        self.assertTrue(CatalogC.has('p31'))
        self.assertTrue(CatalogC.has('p32'))
        self.assertFalse(CatalogC.has('undefined'))

        self.assertTrue(CatalogC.has_provider('p11'))
        self.assertTrue(CatalogC.has_provider('p12'))
        self.assertTrue(CatalogC.has_provider('p21'))
        self.assertTrue(CatalogC.has_provider('p22'))
        self.assertTrue(CatalogC.has_provider('p31'))
        self.assertTrue(CatalogC.has_provider('p32'))
        self.assertFalse(CatalogC.has_provider('undefined'))

    def test_filter_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(CatalogC.filter(di.Provider)) == 6)
        self.assertTrue(len(CatalogC.filter(di.Value)) == 0)

    def test_repr(self):
        """Test declarative catalog representation."""
        self.assertIn('CatalogA', repr(CatalogA))
        self.assertIn('p11', repr(CatalogA))
        self.assertIn('p12', repr(CatalogA))

        self.assertIn('CatalogB', repr(CatalogB))
        self.assertIn('p11', repr(CatalogB))
        self.assertIn('p12', repr(CatalogB))
        self.assertIn('p21', repr(CatalogB))
        self.assertIn('p22', repr(CatalogB))

        self.assertIn('CatalogC', repr(CatalogC))
        self.assertIn('p11', repr(CatalogC))
        self.assertIn('p12', repr(CatalogC))
        self.assertIn('p21', repr(CatalogC))
        self.assertIn('p22', repr(CatalogC))
        self.assertIn('p31', repr(CatalogC))
        self.assertIn('p32', repr(CatalogC))

    def test_abstract_catalog_backward_compatibility(self):
        """Test that di.AbstractCatalog is available."""
        self.assertIs(di.DeclarativeCatalog, di.AbstractCatalog)


class OverrideTests(unittest.TestCase):
    """Catalog overriding and override decorator test cases."""

    def tearDown(self):
        """Tear test environment down."""
        CatalogA.reset_override()

    def test_overriding(self):
        """Test catalog overriding with another catalog."""
        @di.override(CatalogA)
        class OverridingCatalog(di.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = di.Value(1)
            p12 = di.Value(2)

        self.assertEqual(CatalogA.p11(), 1)
        self.assertEqual(CatalogA.p12(), 2)
        self.assertEqual(len(CatalogA.overridden_by), 1)

    def test_overriding_with_dynamic_catalog(self):
        """Test catalog overriding with another dynamic catalog."""
        CatalogA.override(di.DynamicCatalog(p11=di.Value(1),
                                            p12=di.Value(2)))
        self.assertEqual(CatalogA.p11(), 1)
        self.assertEqual(CatalogA.p12(), 2)
        self.assertEqual(len(CatalogA.overridden_by), 1)

    def test_is_overridden(self):
        """Test catalog is_overridden property."""
        self.assertFalse(CatalogA.is_overridden)

        @di.override(CatalogA)
        class OverridingCatalog(di.DeclarativeCatalog):
            """Overriding catalog."""

        self.assertTrue(CatalogA.is_overridden)

    def test_last_overriding(self):
        """Test catalog last_overriding property."""
        @di.override(CatalogA)
        class OverridingCatalog1(di.DeclarativeCatalog):
            """Overriding catalog."""

        @di.override(CatalogA)
        class OverridingCatalog2(di.DeclarativeCatalog):
            """Overriding catalog."""

        self.assertIs(CatalogA.last_overriding, OverridingCatalog2)

    def test_last_overriding_on_not_overridden(self):
        """Test catalog last_overriding property on not overridden catalog."""
        with self.assertRaises(di.Error):
            CatalogA.last_overriding

    def test_reset_last_overriding(self):
        """Test resetting last overriding catalog."""
        @di.override(CatalogA)
        class OverridingCatalog1(di.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = di.Value(1)
            p12 = di.Value(2)

        @di.override(CatalogA)
        class OverridingCatalog2(di.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = di.Value(3)
            p12 = di.Value(4)

        CatalogA.reset_last_overriding()

        self.assertEqual(CatalogA.p11(), 1)
        self.assertEqual(CatalogA.p12(), 2)

    def test_reset_last_overriding_when_not_overridden(self):
        """Test resetting last overriding catalog when it is not overridden."""
        with self.assertRaises(di.Error):
            CatalogA.reset_last_overriding()

    def test_reset_override(self):
        """Test resetting all catalog overrides."""
        @di.override(CatalogA)
        class OverridingCatalog1(di.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = di.Value(1)
            p12 = di.Value(2)

        @di.override(CatalogA)
        class OverridingCatalog2(di.DeclarativeCatalog):
            """Overriding catalog."""

            p11 = di.Value(3)
            p12 = di.Value(4)

        CatalogA.reset_override()

        self.assertFalse(CatalogA.p11.is_overridden)
        self.assertFalse(CatalogA.p12.is_overridden)
