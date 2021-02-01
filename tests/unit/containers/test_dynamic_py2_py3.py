"""Dependency injector dynamic container unit tests."""

import unittest2 as unittest

from dependency_injector import (
    containers,
    providers,
    errors,
)


class ContainerA(containers.DeclarativeContainer):
    p11 = providers.Provider()
    p12 = providers.Provider()


class DeclarativeContainerInstanceTests(unittest.TestCase):

    def test_providers_attribute(self):
        container_a1 = ContainerA()
        container_a2 = ContainerA()

        self.assertIsNot(container_a1.p11, container_a2.p11)
        self.assertIsNot(container_a1.p12, container_a2.p12)
        self.assertNotEqual(container_a1.providers, container_a2.providers)

    def test_dependencies_attribute(self):
        container = ContainerA()
        container.a1 = providers.Dependency()
        container.a2 = providers.DependenciesContainer()
        self.assertEqual(container.dependencies, {'a1': container.a1, 'a2': container.a2})

    def test_set_get_del_providers(self):
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
        container_a = ContainerA()
        container_a.provider_type = providers.Object

        with self.assertRaises(errors.Error):
            container_a.px = providers.Provider()

        self.assertIs(ContainerA.provider_type,
                      containers.DeclarativeContainer.provider_type)

    def test_set_providers(self):
        p13 = providers.Provider()
        p14 = providers.Provider()
        container_a = ContainerA()

        container_a.set_providers(p13=p13, p14=p14)

        self.assertIs(container_a.p13, p13)
        self.assertIs(container_a.p14, p14)

    def test_override(self):
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
        container = ContainerA()
        with self.assertRaises(errors.Error):
            container.override(container)

    def test_override_providers(self):
        p1 = providers.Provider()
        p2 = providers.Provider()
        container_a = ContainerA()

        container_a.override_providers(p11=p1, p12=p2)

        self.assertIs(container_a.p11.last_overriding, p1)
        self.assertIs(container_a.p12.last_overriding, p2)

    def test_override_providers_with_unknown_provider(self):
        container_a = ContainerA()

        with self.assertRaises(AttributeError):
            container_a.override_providers(unknown=providers.Provider())

    def test_reset_last_overridding(self):
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
        container = ContainerA()

        with self.assertRaises(errors.Error):
            container.reset_last_overriding()

    def test_reset_override(self):
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

    def test_init_shutdown_resources(self):
        def _init1():
            _init1.init_counter += 1
            yield
            _init1.shutdown_counter += 1

        _init1.init_counter = 0
        _init1.shutdown_counter = 0

        def _init2():
            _init2.init_counter += 1
            yield
            _init2.shutdown_counter += 1

        _init2.init_counter = 0
        _init2.shutdown_counter = 0

        class Container(containers.DeclarativeContainer):
            resource1 = providers.Resource(_init1)
            resource2 = providers.Resource(_init2)

        container = Container()
        self.assertEqual(_init1.init_counter, 0)
        self.assertEqual(_init1.shutdown_counter, 0)
        self.assertEqual(_init2.init_counter, 0)
        self.assertEqual(_init2.shutdown_counter, 0)

        container.init_resources()
        self.assertEqual(_init1.init_counter, 1)
        self.assertEqual(_init1.shutdown_counter, 0)
        self.assertEqual(_init2.init_counter, 1)
        self.assertEqual(_init2.shutdown_counter, 0)

        container.shutdown_resources()
        self.assertEqual(_init1.init_counter, 1)
        self.assertEqual(_init1.shutdown_counter, 1)
        self.assertEqual(_init2.init_counter, 1)
        self.assertEqual(_init2.shutdown_counter, 1)

        container.init_resources()
        container.shutdown_resources()
        self.assertEqual(_init1.init_counter, 2)
        self.assertEqual(_init1.shutdown_counter, 2)
        self.assertEqual(_init2.init_counter, 2)
        self.assertEqual(_init2.shutdown_counter, 2)

    def test_init_shutdown_nested_resources(self):
        def _init1():
            _init1.init_counter += 1
            yield
            _init1.shutdown_counter += 1

        _init1.init_counter = 0
        _init1.shutdown_counter = 0

        def _init2():
            _init2.init_counter += 1
            yield
            _init2.shutdown_counter += 1

        _init2.init_counter = 0
        _init2.shutdown_counter = 0

        class Container(containers.DeclarativeContainer):

            service = providers.Factory(
                dict,
                resource1=providers.Resource(_init1),
                resource2=providers.Resource(_init2),
            )

        container = Container()
        self.assertEqual(_init1.init_counter, 0)
        self.assertEqual(_init1.shutdown_counter, 0)
        self.assertEqual(_init2.init_counter, 0)
        self.assertEqual(_init2.shutdown_counter, 0)

        container.init_resources()
        self.assertEqual(_init1.init_counter, 1)
        self.assertEqual(_init1.shutdown_counter, 0)
        self.assertEqual(_init2.init_counter, 1)
        self.assertEqual(_init2.shutdown_counter, 0)

        container.shutdown_resources()
        self.assertEqual(_init1.init_counter, 1)
        self.assertEqual(_init1.shutdown_counter, 1)
        self.assertEqual(_init2.init_counter, 1)
        self.assertEqual(_init2.shutdown_counter, 1)

        container.init_resources()
        container.shutdown_resources()
        self.assertEqual(_init1.init_counter, 2)
        self.assertEqual(_init1.shutdown_counter, 2)
        self.assertEqual(_init2.init_counter, 2)
        self.assertEqual(_init2.shutdown_counter, 2)
