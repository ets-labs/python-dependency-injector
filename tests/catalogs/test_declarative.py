"""Dependency injector declarative catalog unittests."""

import unittest2 as unittest

from dependency_injector import (
    catalogs,
    providers,
    injections,
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


class DeclarativeCatalogTests(unittest.TestCase):
    """Declarative catalog tests."""

    def test_cls_providers(self):
        """Test `di.DeclarativeCatalog.cls_providers` contents."""
        class CatalogA(catalogs.DeclarativeCatalog):
            """Test catalog A."""

            p11 = providers.Provider()
            p12 = providers.Provider()

        class CatalogB(CatalogA):
            """Test catalog B."""

            p21 = providers.Provider()
            p22 = providers.Provider()
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

    def test_bind_existing_provider(self):
        """Test setting of provider via bind_provider() to catalog."""
        with self.assertRaises(errors.Error):
            CatalogA.p11 = providers.Provider()

        with self.assertRaises(errors.Error):
            CatalogA.bind_provider('p11', providers.Provider())

    def test_bind_provider_with_valid_provided_type(self):
        """Test setting of provider with provider type restriction."""
        class SomeProvider(providers.Provider):
            """Some provider."""

        class SomeCatalog(catalogs.DeclarativeCatalog):
            """Some catalog with provider type restriction."""

            provider_type = SomeProvider

        px = SomeProvider()
        py = SomeProvider()

        SomeCatalog.bind_provider('px', px)
        SomeCatalog.py = py

        self.assertIs(SomeCatalog.px, px)
        self.assertIs(SomeCatalog.get_provider('px'), px)

        self.assertIs(SomeCatalog.py, py)
        self.assertIs(SomeCatalog.get_provider('py'), py)

    def test_bind_provider_with_invalid_provided_type(self):
        """Test setting of provider with provider type restriction."""
        class SomeProvider(providers.Provider):
            """Some provider."""

        class SomeCatalog(catalogs.DeclarativeCatalog):
            """Some catalog with provider type restriction."""

            provider_type = SomeProvider

        px = providers.Provider()

        with self.assertRaises(errors.Error):
            SomeCatalog.bind_provider('px', px)

        with self.assertRaises(errors.Error):
            SomeCatalog.px = px

        with self.assertRaises(errors.Error):
            SomeCatalog.bind_providers(dict(px=px))

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
        self.assertTrue(CatalogB.has_provider('p11'))
        self.assertTrue(CatalogB.has_provider('p12'))
        self.assertTrue(CatalogB.has_provider('p21'))
        self.assertTrue(CatalogB.has_provider('p22'))
        self.assertFalse(CatalogB.has_provider('undefined'))

    def test_filter_all_providers_by_type(self):
        """Test getting of all catalog providers of specific type."""
        self.assertTrue(len(CatalogB.filter(providers.Provider)) == 4)
        self.assertTrue(len(CatalogB.filter(providers.Object)) == 0)

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


class TestCatalogWithProvidingCallbacks(unittest.TestCase):
    """Catalog with providing callback tests."""

    def test_concept(self):
        """Test concept."""
        class UsersService(object):
            """Users service, that has dependency on database."""

        class AuthService(object):
            """Auth service, that has dependencies on users service."""

            def __init__(self, users_service):
                """Initializer."""
                self.users_service = users_service

        class Services(catalogs.DeclarativeCatalog):
            """Catalog of service providers."""

            @providers.Factory
            def users():
                """Provide users service.

                :rtype: providers.Provider -> UsersService
                """
                return UsersService()

            @providers.Factory
            @injections.inject(users_service=users)
            def auth(**kwargs):
                """Provide users service.

                :rtype: providers.Provider -> AuthService
                """
                return AuthService(**kwargs)

        # Retrieving catalog providers:
        users_service = Services.users()
        auth_service = Services.auth()

        # Making some asserts:
        self.assertIsInstance(auth_service.users_service, UsersService)
        self.assertIsNot(users_service, Services.users())
        self.assertIsNot(auth_service, Services.auth())

        # Overriding auth service provider and making some asserts:
        class ExtendedAuthService(AuthService):
            """Extended version of auth service."""

            def __init__(self, users_service, ttl):
                """Initializer."""
                self.ttl = ttl
                super(ExtendedAuthService, self).__init__(
                    users_service=users_service)

        class OverriddenServices(Services):
            """Catalog of service providers."""

            @providers.override(Services.auth)
            @providers.Factory
            @injections.inject(users_service=Services.users)
            @injections.inject(ttl=3600)
            def auth(**kwargs):
                """Provide users service.

                :rtype: providers.Provider -> AuthService
                """
                return ExtendedAuthService(**kwargs)

        auth_service = Services.auth()

        self.assertIsInstance(auth_service, ExtendedAuthService)


class CopyingTests(unittest.TestCase):
    """Declarative catalogs copying tests."""

    def test_copy(self):
        """Test catalog providers copying."""
        @catalogs.copy(CatalogA)
        class CatalogA1(CatalogA):
            pass

        @catalogs.copy(CatalogA)
        class CatalogA2(CatalogA):
            pass

        self.assertIsNot(CatalogA.p11, CatalogA1.p11)
        self.assertIsNot(CatalogA.p12, CatalogA1.p12)

        self.assertIsNot(CatalogA.p11, CatalogA2.p11)
        self.assertIsNot(CatalogA.p12, CatalogA2.p12)

        self.assertIsNot(CatalogA1.p11, CatalogA2.p11)
        self.assertIsNot(CatalogA1.p12, CatalogA2.p12)

    def test_copy_with_replacing(self):
        """Test catalog providers copying."""
        class CatalogA(catalogs.DeclarativeCatalog):
            p11 = providers.Object(0)
            p12 = providers.Factory(dict) \
                .kwargs(p11=p11)

        @catalogs.copy(CatalogA)
        class CatalogA1(CatalogA):
            p11 = providers.Object(1)
            p13 = providers.Object(11)

        @catalogs.copy(CatalogA)
        class CatalogA2(CatalogA):
            p11 = providers.Object(2)
            p13 = providers.Object(22)

        self.assertIsNot(CatalogA.p11, CatalogA1.p11)
        self.assertIsNot(CatalogA.p12, CatalogA1.p12)

        self.assertIsNot(CatalogA.p11, CatalogA2.p11)
        self.assertIsNot(CatalogA.p12, CatalogA2.p12)

        self.assertIsNot(CatalogA1.p11, CatalogA2.p11)
        self.assertIsNot(CatalogA1.p12, CatalogA2.p12)

        self.assertIs(CatalogA.p12.injections[0].injectable, CatalogA.p11)
        self.assertIs(CatalogA1.p12.injections[0].injectable, CatalogA1.p11)
        self.assertIs(CatalogA2.p12.injections[0].injectable, CatalogA2.p11)

        self.assertEqual(CatalogA.p12(), dict(p11=0))
        self.assertEqual(CatalogA1.p12(), dict(p11=1))
        self.assertEqual(CatalogA2.p12(), dict(p11=2))

        self.assertEqual(CatalogA1.p13(), 11)
        self.assertEqual(CatalogA2.p13(), 22)


class InstantiationTests(unittest.TestCase):
    """Declarative catalogs instantiation tests."""

    def setUp(self):
        """Set test environment up."""
        self.catalog = CatalogA()

    def tearDown(self):
        """Tear test environment down."""
        self.catalog = None

    def test_access_instance_attributes(self):
        """Test accessing declarative catalog instance attributes."""
        self.assertEqual(self.catalog.name,
                         CatalogA.name)
        self.assertEqual(self.catalog.providers,
                         CatalogA.providers)
        self.assertEqual(self.catalog.cls_providers,
                         CatalogA.cls_providers)
        self.assertEqual(self.catalog.inherited_providers,
                         CatalogA.inherited_providers)
        self.assertEqual(self.catalog.overridden_by,
                         CatalogA.overridden_by)
        self.assertEqual(self.catalog.is_overridden,
                         CatalogA.is_overridden)
        self.assertEqual(self.catalog.last_overriding,
                         CatalogA.last_overriding)
