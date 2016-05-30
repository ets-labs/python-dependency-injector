"""Dependency injector container unit tests."""

import unittest2 as unittest

from dependency_injector import (
    containers,
    providers,
    errors,
)


class ContainerA(containers.DeclarativeContainer):
    """Declarative IoC container A."""

    p11 = providers.Provider()
    p12 = providers.Provider()


class ContainerB(ContainerA):
    """Declarative IoC container B.

    Extends container A.
    """

    p21 = providers.Provider()
    p22 = providers.Provider()


class DeclarativeContainerTests(unittest.TestCase):
    """Declarative container tests."""

    def test_providers_attribute(self):
        """Test providers attribute."""
        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))
        self.assertEqual(ContainerB.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12,
                                                    p21=ContainerB.p21,
                                                    p22=ContainerB.p22))

    def test_cls_providers_attribute(self):
        """Test cls_providers attribute."""
        self.assertEqual(ContainerA.cls_providers, dict(p11=ContainerA.p11,
                                                        p12=ContainerA.p12))
        self.assertEqual(ContainerB.cls_providers, dict(p21=ContainerB.p21,
                                                        p22=ContainerB.p22))

    def test_inherited_providers_attribute(self):
        """Test inherited_providers attribute."""
        self.assertEqual(ContainerA.inherited_providers, dict())
        self.assertEqual(ContainerB.inherited_providers,
                         dict(p11=ContainerA.p11,
                              p12=ContainerA.p12))

    def test_set_get_del_providers(self):
        """Test set/get/del provider attributes."""
        a_p13 = providers.Provider()
        b_p23 = providers.Provider()

        ContainerA.p13 = a_p13
        ContainerB.p23 = b_p23

        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12,
                                                    p13=a_p13))
        self.assertEqual(ContainerB.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12,
                                                    p21=ContainerB.p21,
                                                    p22=ContainerB.p22,
                                                    p23=b_p23))

        self.assertEqual(ContainerA.cls_providers, dict(p11=ContainerA.p11,
                                                        p12=ContainerA.p12,
                                                        p13=a_p13))
        self.assertEqual(ContainerB.cls_providers, dict(p21=ContainerB.p21,
                                                        p22=ContainerB.p22,
                                                        p23=b_p23))

        del ContainerA.p13
        del ContainerB.p23

        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))
        self.assertEqual(ContainerB.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12,
                                                    p21=ContainerB.p21,
                                                    p22=ContainerB.p22))

        self.assertEqual(ContainerA.cls_providers, dict(p11=ContainerA.p11,
                                                        p12=ContainerA.p12))
        self.assertEqual(ContainerB.cls_providers, dict(p21=ContainerB.p21,
                                                        p22=ContainerB.p22))

    def test_declare_with_valid_provider_type(self):
        """Test declaration of container with valid provider type."""
        class _Container(containers.DeclarativeContainer):
            provider_type = providers.Object
            px = providers.Object(object())

        self.assertIsInstance(_Container.px, providers.Object)

    def test_declare_with_invalid_provider_type(self):
        """Test declaration of container with invalid provider type."""
        with self.assertRaises(errors.Error):
            class _Container(containers.DeclarativeContainer):
                provider_type = providers.Object
                px = providers.Provider()

    def test_seth_valid_provider_type(self):
        """Test setting of valid provider."""
        class _Container(containers.DeclarativeContainer):
            provider_type = providers.Object

        _Container.px = providers.Object(object())

        self.assertIsInstance(_Container.px, providers.Object)

    def test_set_invalid_provider_type(self):
        """Test setting of invalid provider."""
        class _Container(containers.DeclarativeContainer):
            provider_type = providers.Object

        with self.assertRaises(errors.Error):
            _Container.px = providers.Provider()

    def test_override(self):
        """Test override."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        _Container.override(_OverridingContainer1)
        _Container.override(_OverridingContainer2)

        self.assertEqual(_Container.overridden_by,
                         (_OverridingContainer1,
                          _OverridingContainer2))
        self.assertEqual(_Container.p11.overridden_by,
                         (_OverridingContainer1.p11,
                          _OverridingContainer2.p11))

    def test_override_decorator(self):
        """Test override decorator."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        @containers.override(_Container)
        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        @containers.override(_Container)
        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        self.assertEqual(_Container.overridden_by,
                         (_OverridingContainer1,
                          _OverridingContainer2))
        self.assertEqual(_Container.p11.overridden_by,
                         (_OverridingContainer1.p11,
                          _OverridingContainer2.p11))

    def test_reset_last_overridding(self):
        """Test reset of last overriding."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        _Container.override(_OverridingContainer1)
        _Container.override(_OverridingContainer2)
        _Container.reset_last_overriding()

        self.assertEqual(_Container.overridden_by,
                         (_OverridingContainer1,))
        self.assertEqual(_Container.p11.overridden_by,
                         (_OverridingContainer1.p11,))

    def test_reset_override(self):
        """Test reset all overridings."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        _Container.override(_OverridingContainer1)
        _Container.override(_OverridingContainer2)
        _Container.reset_override()

        self.assertEqual(_Container.overridden_by, tuple())
        self.assertEqual(_Container.p11.overridden_by, tuple())

if __name__ == '__main__':
    unittest.main()
