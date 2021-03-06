"""Dependency injector declarative container unit tests."""

import collections
import unittest

from dependency_injector import (
    containers,
    providers,
    errors,
)


class ContainerA(containers.DeclarativeContainer):
    p11 = providers.Provider()
    p12 = providers.Provider()


class ContainerB(ContainerA):
    p21 = providers.Provider()
    p22 = providers.Provider()


class ContainerC(ContainerB):
    p31 = providers.Provider()
    p32 = providers.Provider()


class DeclarativeContainerTests(unittest.TestCase):

    def test_providers_attribute(self):
        self.assertEqual(ContainerA.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12))
        self.assertEqual(ContainerB.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12,
                                                    p21=ContainerB.p21,
                                                    p22=ContainerB.p22))
        self.assertEqual(ContainerC.providers, dict(p11=ContainerA.p11,
                                                    p12=ContainerA.p12,
                                                    p21=ContainerB.p21,
                                                    p22=ContainerB.p22,
                                                    p31=ContainerC.p31,
                                                    p32=ContainerC.p32))

    def test_providers_attribute_with_redefinition(self):
        p1 = providers.Provider()
        p2 = providers.Provider()

        class ContainerA2(ContainerA):
            p11 = p1
            p12 = p2

        self.assertEqual(
            ContainerA.providers,
            {
                'p11': ContainerA.p11,
                'p12': ContainerA.p12,
            },
        )
        self.assertEqual(
            ContainerA2.providers,
            {
                'p11': p1,
                'p12': p2,
            },
        )

    def test_cls_providers_attribute(self):
        self.assertEqual(ContainerA.cls_providers, dict(p11=ContainerA.p11,
                                                        p12=ContainerA.p12))
        self.assertEqual(ContainerB.cls_providers, dict(p21=ContainerB.p21,
                                                        p22=ContainerB.p22))
        self.assertEqual(ContainerC.cls_providers, dict(p31=ContainerC.p31,
                                                        p32=ContainerC.p32))

    def test_inherited_providers_attribute(self):
        self.assertEqual(ContainerA.inherited_providers, dict())
        self.assertEqual(ContainerB.inherited_providers,
                         dict(p11=ContainerA.p11,
                              p12=ContainerA.p12))
        self.assertEqual(ContainerC.inherited_providers,
                         dict(p11=ContainerA.p11,
                              p12=ContainerA.p12,
                              p21=ContainerB.p21,
                              p22=ContainerB.p22))

    def test_dependencies_attribute(self):
        class ContainerD(ContainerC):
            p41 = providers.Dependency()
            p42 = providers.DependenciesContainer()

        class ContainerE(ContainerD):
            p51 = providers.Dependency()
            p52 = providers.DependenciesContainer()

        self.assertEqual(
            ContainerD.dependencies,
            {
                'p41': ContainerD.p41,
                'p42': ContainerD.p42,
            },
        )
        self.assertEqual(
            ContainerE.dependencies,
            {
                'p41': ContainerD.p41,
                'p42': ContainerD.p42,
                'p51': ContainerE.p51,
                'p52': ContainerE.p52,
            },
        )

    def test_set_get_del_providers(self):
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
        class _Container(containers.DeclarativeContainer):
            provider_type = providers.Object
            px = providers.Object(object())

        self.assertIsInstance(_Container.px, providers.Object)

    def test_declare_with_invalid_provider_type(self):
        with self.assertRaises(errors.Error):
            class _Container(containers.DeclarativeContainer):
                provider_type = providers.Object
                px = providers.Provider()

    def test_seth_valid_provider_type(self):
        class _Container(containers.DeclarativeContainer):
            provider_type = providers.Object

        _Container.px = providers.Object(object())

        self.assertIsInstance(_Container.px, providers.Object)

    def test_set_invalid_provider_type(self):
        class _Container(containers.DeclarativeContainer):
            provider_type = providers.Object

        with self.assertRaises(errors.Error):
            _Container.px = providers.Provider()

    def test_override(self):
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
        with self.assertRaises(errors.Error):
            ContainerA.override(ContainerA)

    def test_override_with_parent(self):
        with self.assertRaises(errors.Error):
            ContainerB.override(ContainerA)

    def test_override_decorator(self):
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

    def test_reset_last_overriding(self):
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

    def test_reset_last_overriding_when_not_overridden(self):
        with self.assertRaises(errors.Error):
            ContainerA.reset_last_overriding()

    def test_reset_override(self):
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

    def test_copy_with_replacing_subcontainer_providers(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/374
        class X(containers.DeclarativeContainer):
            foo = providers.Dependency(instance_of=str)

        def build_x():
            return X(foo='1')

        class A(containers.DeclarativeContainer):
            x = providers.DependenciesContainer(**X.providers)
            y = x.foo

        @containers.copy(A)
        class B1(A):
            x = providers.Container(build_x)

        b1 = B1()

        self.assertEqual(b1.y(), '1')

    def test_containers_attribute(self):
        class Container(containers.DeclarativeContainer):
            class Container1(containers.DeclarativeContainer):
                pass

            class Container2(containers.DeclarativeContainer):
                pass

            Container3 = containers.DynamicContainer()

        self.assertEqual(Container.containers,
                         dict(Container1=Container.Container1,
                              Container2=Container.Container2,
                              Container3=Container.Container3))

    def test_init_with_overriding_providers(self):
        p1 = providers.Provider()
        p2 = providers.Provider()

        container = ContainerA(p11=p1, p12=p2)

        self.assertIs(container.p11.last_overriding, p1)
        self.assertIs(container.p12.last_overriding, p2)

    def test_init_with_overridden_dependency(self):
        # Bug:
        # https://github.com/ets-labs/python-dependency-injector/issues/198
        class _Container(containers.DeclarativeContainer):
            p1 = providers.Dependency(instance_of=int)

            p2 = providers.Dependency(object)
            p2.override(providers.Factory(dict, p1=p1))

        container = _Container(p1=1)

        self.assertEqual(container.p2(), {'p1': 1})
        self.assertIs(
            container.p2.last_overriding.kwargs['p1'],
            container.p1,
        )
        self.assertIsNot(
            container.p2.last_overriding.kwargs['p1'],
            _Container.p1,
        )
        self.assertIs(
            _Container.p2.last_overriding.kwargs['p1'],
            _Container.p1,
        )

    def test_init_with_chained_dependency(self):
        # Bug:
        # https://github.com/ets-labs/python-dependency-injector/issues/200
        class _Container(containers.DeclarativeContainer):
            p1 = providers.Dependency(instance_of=int)
            p2 = providers.Factory(p1)

        container = _Container(p1=1)

        self.assertEqual(container.p2(), 1)
        self.assertIs(container.p2.cls, container.p1)
        self.assertIs(_Container.p2.cls, _Container.p1)
        self.assertIsNot(container.p2.cls,  _Container.p1)

    def test_init_with_dependency_delegation(self):
        # Bug:
        # https://github.com/ets-labs/python-dependency-injector/issues/235
        A = collections.namedtuple('A', [])
        B = collections.namedtuple('B', ['fa'])
        C = collections.namedtuple('B', ['a'])

        class Services(containers.DeclarativeContainer):
            a = providers.Dependency()
            c = providers.Factory(C, a=a)
            b = providers.Factory(B, fa=a.provider)

        a = providers.Factory(A)
        assert isinstance(Services(a=a).c().a, A)  # ok
        Services(a=a).b().fa()

    def test_init_with_grand_child_provider(self):
        # Bug:
        # https://github.com/ets-labs/python-dependency-injector/issues/350
        provider = providers.Provider()
        container = ContainerC(p11=provider)

        self.assertIsInstance(container.p11, providers.Provider)
        self.assertIsInstance(container.p12, providers.Provider)
        self.assertIsInstance(container.p21, providers.Provider)
        self.assertIsInstance(container.p22, providers.Provider)
        self.assertIsInstance(container.p31, providers.Provider)
        self.assertIsInstance(container.p32, providers.Provider)
        self.assertIs(container.p11.last_overriding, provider)

    def test_parent_set_in__new__(self):
        class Container(containers.DeclarativeContainer):
            dependency = providers.Dependency()
            dependencies_container = providers.DependenciesContainer()
            container = providers.Container(ContainerA)

        self.assertIs(Container.dependency.parent, Container)
        self.assertIs(Container.dependencies_container.parent, Container)
        self.assertIs(Container.container.parent, Container)

    def test_parent_set_in__setattr__(self):
        class Container(containers.DeclarativeContainer):
            pass

        Container.dependency = providers.Dependency()
        Container.dependencies_container = providers.DependenciesContainer()
        Container.container = providers.Container(ContainerA)

        self.assertIs(Container.dependency.parent, Container)
        self.assertIs(Container.dependencies_container.parent, Container)
        self.assertIs(Container.container.parent, Container)

    def test_resolve_provider_name(self):
        self.assertEqual(ContainerA.resolve_provider_name(ContainerA.p11), 'p11')

    def test_resolve_provider_name_no_provider(self):
        with self.assertRaises(errors.Error):
            ContainerA.resolve_provider_name(providers.Provider())

    def test_child_dependency_parent_name(self):
        class Container(containers.DeclarativeContainer):
            dependency = providers.Dependency()

        with self.assertRaises(errors.Error) as context:
            Container.dependency()
        self.assertEqual(
            str(context.exception),
            'Dependency "Container.dependency" is not defined',
        )

    def test_child_dependencies_container_parent_name(self):
        class Container(containers.DeclarativeContainer):
            dependencies_container = providers.DependenciesContainer()

        with self.assertRaises(errors.Error) as context:
            Container.dependencies_container.dependency()
        self.assertEqual(
            str(context.exception),
            'Dependency "Container.dependencies_container.dependency" is not defined',
        )

    def test_child_container_parent_name(self):
        class ChildContainer(containers.DeclarativeContainer):
            dependency = providers.Dependency()

        class Container(containers.DeclarativeContainer):
            child_container = providers.Container(ChildContainer)

        with self.assertRaises(errors.Error) as context:
            Container.child_container.dependency()
        self.assertEqual(
            str(context.exception),
            'Dependency "Container.child_container.dependency" is not defined',
        )
