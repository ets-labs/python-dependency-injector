"""Dependency injector container unit tests."""

import unittest2 as unittest

from dependency_injector import (
    containers,
    providers,
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

    def test_providers_attribute_with(self):
        """Test providers attribute."""
        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))
        self.assertEqual(ContainerB.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12,
                                                    p21=ContainerB.p21,
                                                    p22=ContainerB.p22))

    def test_cls_providers_attribute_with(self):
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

    def test_set_get_del_provider_attribute(self):
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


if __name__ == '__main__':
    unittest.main()
