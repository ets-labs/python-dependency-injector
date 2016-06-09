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

        self.assertEqual(_Container.overridden,
                         (_OverridingContainer1,
                          _OverridingContainer2))
        self.assertEqual(_Container.p11.overridden,
                         (_OverridingContainer1.p11,
                          _OverridingContainer2.p11))

    def test_override_with_itself(self):
        """Test override with itself."""
        with self.assertRaises(errors.Error):
            ContainerA.override(ContainerA)

    def test_override_with_parent(self):
        """Test override with parent."""
        with self.assertRaises(errors.Error):
            ContainerB.override(ContainerA)

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

        self.assertEqual(_Container.overridden,
                         (_OverridingContainer1,
                          _OverridingContainer2))
        self.assertEqual(_Container.p11.overridden,
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

        self.assertEqual(_Container.overridden,
                         (_OverridingContainer1,))
        self.assertEqual(_Container.p11.overridden,
                         (_OverridingContainer1.p11,))

    def test_reset_last_overridding_when_not_overridden(self):
        """Test reset of last overriding."""
        with self.assertRaises(errors.Error):
            ContainerA.reset_last_overriding()

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

        self.assertEqual(_Container.overridden, tuple())
        self.assertEqual(_Container.p11.overridden, tuple())

    def test_copy(self):
        """Test copy decorator."""
        @containers.copy(ContainerA)
        class _Container1(ContainerA):
            pass

        @containers.copy(ContainerA)
        class _Container2(ContainerA):
            pass

        self.assertIsNot(ContainerA.p11, _Container1.p11)
        self.assertIsNot(ContainerA.p12, _Container1.p12)

        self.assertIsNot(ContainerA.p11, _Container2.p11)
        self.assertIsNot(ContainerA.p12, _Container2.p12)

        self.assertIsNot(_Container1.p11, _Container2.p11)
        self.assertIsNot(_Container1.p12, _Container2.p12)

    def test_copy_with_replacing(self):
        """Test copy decorator with providers replacement."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Object(0)
            p12 = providers.Factory(dict, p11=p11)

        @containers.copy(_Container)
        class _Container1(_Container):
            p11 = providers.Object(1)
            p13 = providers.Object(11)

        @containers.copy(_Container)
        class _Container2(_Container):
            p11 = providers.Object(2)
            p13 = providers.Object(22)

        self.assertIsNot(_Container.p11, _Container1.p11)
        self.assertIsNot(_Container.p12, _Container1.p12)

        self.assertIsNot(_Container.p11, _Container2.p11)
        self.assertIsNot(_Container.p12, _Container2.p12)

        self.assertIsNot(_Container1.p11, _Container2.p11)
        self.assertIsNot(_Container1.p12, _Container2.p12)

        self.assertIs(_Container.p12.kwargs['p11'], _Container.p11)
        self.assertIs(_Container1.p12.kwargs['p11'], _Container1.p11)
        self.assertIs(_Container2.p12.kwargs['p11'], _Container2.p11)

        self.assertEqual(_Container.p12(), dict(p11=0))
        self.assertEqual(_Container1.p12(), dict(p11=1))
        self.assertEqual(_Container2.p12(), dict(p11=2))

        self.assertEqual(_Container1.p13(), 11)
        self.assertEqual(_Container2.p13(), 22)


class DeclarativeContainerInstanceTests(unittest.TestCase):
    """Declarative container instance tests."""

    def test_providers_attribute(self):
        """Test providers attribute."""
        container_a1 = ContainerA()
        container_a2 = ContainerA()

        self.assertIsNot(container_a1.p11, container_a2.p11)
        self.assertIsNot(container_a1.p12, container_a2.p12)
        self.assertNotEqual(container_a1.providers, container_a2.providers)

    def test_set_get_del_providers(self):
        """Test set/get/del provider attributes."""
        p13 = providers.Provider()

        container_a1 = ContainerA()
        container_a2 = ContainerA()

        container_a1.p13 = p13
        container_a2.p13 = p13

        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))
        self.assertEqual(ContainerA.cls_providers, dict(p11=ContainerA.p11,
                                                        p12=ContainerA.p12))

        self.assertEqual(container_a1.providers, dict(p11=container_a1.p11,
                                                      p12=container_a1.p12,
                                                      p13=p13))
        self.assertEqual(container_a2.providers, dict(p11=container_a2.p11,
                                                      p12=container_a2.p12,
                                                      p13=p13))

        del container_a1.p13
        self.assertEqual(container_a1.providers, dict(p11=container_a1.p11,
                                                      p12=container_a1.p12))

        del container_a2.p13
        self.assertEqual(container_a2.providers, dict(p11=container_a2.p11,
                                                      p12=container_a2.p12))

        del container_a1.p11
        del container_a1.p12
        self.assertEqual(container_a1.providers, dict())
        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))

        del container_a2.p11
        del container_a2.p12
        self.assertEqual(container_a2.providers, dict())
        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))

    def test_set_invalid_provider_type(self):
        """Test setting of invalid provider."""
        container_a = ContainerA()
        container_a.provider_type = providers.Object

        with self.assertRaises(errors.Error):
            container_a.px = providers.Provider()

        self.assertIs(ContainerA.provider_type,
                      containers.DeclarativeContainer.provider_type)

    def test_override(self):
        """Test override."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        container = _Container()
        overriding_container1 = _OverridingContainer1()
        overriding_container2 = _OverridingContainer2()

        container.override(overriding_container1)
        container.override(overriding_container2)

        self.assertEqual(container.overridden,
                         (overriding_container1,
                          overriding_container2))
        self.assertEqual(container.p11.overridden,
                         (overriding_container1.p11,
                          overriding_container2.p11))

        self.assertEqual(_Container.overridden, tuple())
        self.assertEqual(_Container.p11.overridden, tuple())

    def test_override_with_itself(self):
        """Test override container with itself."""
        container = ContainerA()
        with self.assertRaises(errors.Error):
            container.override(container)

    def test_reset_last_overridding(self):
        """Test reset of last overriding."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        container = _Container()
        overriding_container1 = _OverridingContainer1()
        overriding_container2 = _OverridingContainer2()

        container.override(overriding_container1)
        container.override(overriding_container2)
        container.reset_last_overriding()

        self.assertEqual(container.overridden,
                         (overriding_container1,))
        self.assertEqual(container.p11.overridden,
                         (overriding_container1.p11,))

    def test_reset_last_overridding_when_not_overridden(self):
        """Test reset of last overriding."""
        container = ContainerA()

        with self.assertRaises(errors.Error):
            container.reset_last_overriding()

    def test_reset_override(self):
        """Test reset all overridings."""
        class _Container(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer1(containers.DeclarativeContainer):
            p11 = providers.Provider()

        class _OverridingContainer2(containers.DeclarativeContainer):
            p11 = providers.Provider()
            p12 = providers.Provider()

        container = _Container()
        overriding_container1 = _OverridingContainer1()
        overriding_container2 = _OverridingContainer2()

        container.override(overriding_container1)
        container.override(overriding_container2)
        container.reset_override()

        self.assertEqual(container.overridden, tuple())
        self.assertEqual(container.p11.overridden, tuple())


if __name__ == '__main__':
    unittest.main()
