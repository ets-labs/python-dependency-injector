"""Main container class tests."""

import collections

from dependency_injector import containers, providers, errors
from pytest import raises


class ContainerA(containers.DeclarativeContainer):
    p11 = providers.Provider()
    p12 = providers.Provider()


class ContainerB(ContainerA):
    p21 = providers.Provider()
    p22 = providers.Provider()


class ContainerC(ContainerB):
    p31 = providers.Provider()
    p32 = providers.Provider()


def test_providers_attribute():
    assert ContainerA.providers == dict(p11=ContainerA.p11, p12=ContainerA.p12)
    assert ContainerB.providers == dict(
        p11=ContainerA.p11,
        p12=ContainerA.p12,
        p21=ContainerB.p21,
        p22=ContainerB.p22,
    )
    assert ContainerC.providers == dict(
        p11=ContainerA.p11,
        p12=ContainerA.p12,
        p21=ContainerB.p21,
        p22=ContainerB.p22,
        p31=ContainerC.p31,
        p32=ContainerC.p32,
    )


def test_providers_attribute_with_redefinition():
    p1 = providers.Provider()
    p2 = providers.Provider()

    class ContainerA2(ContainerA):
        p11 = p1
        p12 = p2

    assert ContainerA.providers == {
        "p11": ContainerA.p11,
        "p12": ContainerA.p12,
    }
    assert ContainerA2.providers == {
        "p11": p1,
        "p12": p2,
    }


def test_cls_providers_attribute():
    assert ContainerA.cls_providers == dict(p11=ContainerA.p11, p12=ContainerA.p12)
    assert ContainerB.cls_providers == dict(p21=ContainerB.p21, p22=ContainerB.p22)
    assert ContainerC.cls_providers == dict(p31=ContainerC.p31, p32=ContainerC.p32)


def test_inherited_providers_attribute():
    assert ContainerA.inherited_providers == dict()
    assert ContainerB.inherited_providers == dict(p11=ContainerA.p11, p12=ContainerA.p12)
    assert ContainerC.inherited_providers == dict(
        p11=ContainerA.p11,
        p12=ContainerA.p12,
        p21=ContainerB.p21,
        p22=ContainerB.p22,
    )


def test_dependencies_attribute():
    class ContainerD(ContainerC):
        p41 = providers.Dependency()
        p42 = providers.DependenciesContainer()

    class ContainerE(ContainerD):
        p51 = providers.Dependency()
        p52 = providers.DependenciesContainer()

    assert ContainerD.dependencies == {
        "p41": ContainerD.p41,
        "p42": ContainerD.p42,
    }
    assert ContainerE.dependencies == {
        "p41": ContainerD.p41,
        "p42": ContainerD.p42,
        "p51": ContainerE.p51,
        "p52": ContainerE.p52,
    }


def test_set_get_del_providers():
    a_p13 = providers.Provider()
    b_p23 = providers.Provider()

    ContainerA.p13 = a_p13
    ContainerB.p23 = b_p23

    assert ContainerA.providers == dict(
        p11=ContainerA.p11,
        p12=ContainerA.p12,
        p13=a_p13,
    )
    assert ContainerB.providers == dict(
        p11=ContainerA.p11,
        p12=ContainerA.p12,
        p21=ContainerB.p21,
        p22=ContainerB.p22,
        p23=b_p23,
    )

    assert ContainerA.cls_providers == dict(
        p11=ContainerA.p11,
        p12=ContainerA.p12,
        p13=a_p13,
    )
    assert ContainerB.cls_providers == dict(
        p21=ContainerB.p21,
        p22=ContainerB.p22,
        p23=b_p23,
    )

    del ContainerA.p13
    del ContainerB.p23

    assert ContainerA.providers == dict(p11=ContainerA.p11, p12=ContainerA.p12)
    assert ContainerB.providers == dict(
        p11=ContainerA.p11,
        p12=ContainerA.p12,
        p21=ContainerB.p21,
        p22=ContainerB.p22,
    )

    assert ContainerA.cls_providers == dict(p11=ContainerA.p11, p12=ContainerA.p12)
    assert ContainerB.cls_providers == dict(p21=ContainerB.p21, p22=ContainerB.p22)


def test_declare_with_valid_provider_type():
    class _Container(containers.DeclarativeContainer):
        provider_type = providers.Object
        px = providers.Object(object())

    assert isinstance(_Container.px, providers.Object)


def test_declare_with_invalid_provider_type():
    with raises(errors.Error):
        class _Container(containers.DeclarativeContainer):
            provider_type = providers.Object
            px = providers.Provider()


def test_seth_valid_provider_type():
    class _Container(containers.DeclarativeContainer):
        provider_type = providers.Object

    _Container.px = providers.Object(object())

    assert isinstance(_Container.px, providers.Object)

def test_set_invalid_provider_type():
    class _Container(containers.DeclarativeContainer):
        provider_type = providers.Object

    with raises(errors.Error):
        _Container.px = providers.Provider()


def test_override():
    class _Container(containers.DeclarativeContainer):
        p11 = providers.Provider()

    class _OverridingContainer1(containers.DeclarativeContainer):
        p11 = providers.Provider()

    class _OverridingContainer2(containers.DeclarativeContainer):
        p11 = providers.Provider()
        p12 = providers.Provider()

    _Container.override(_OverridingContainer1)
    _Container.override(_OverridingContainer2)

    assert _Container.overridden == (_OverridingContainer1, _OverridingContainer2)
    assert _Container.p11.overridden == (_OverridingContainer1.p11, _OverridingContainer2.p11)


def test_override_with_it():
    with raises(errors.Error):
        ContainerA.override(ContainerA)


def test_override_with_parent():
    with raises(errors.Error):
        ContainerB.override(ContainerA)


def test_override_decorator():
    class _Container(containers.DeclarativeContainer):
        p11 = providers.Provider()

    @containers.override(_Container)
    class _OverridingContainer1(containers.DeclarativeContainer):
        p11 = providers.Provider()

    @containers.override(_Container)
    class _OverridingContainer2(containers.DeclarativeContainer):
        p11 = providers.Provider()
        p12 = providers.Provider()

    assert _Container.overridden == (_OverridingContainer1, _OverridingContainer2)
    assert _Container.p11.overridden == (_OverridingContainer1.p11, _OverridingContainer2.p11)


def test_reset_last_overriding():
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

    assert _Container.overridden == (_OverridingContainer1,)
    assert _Container.p11.overridden == (_OverridingContainer1.p11,)


def test_reset_last_overriding_when_not_overridden():
    with raises(errors.Error):
        ContainerA.reset_last_overriding()


def test_reset_override():
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

    assert _Container.overridden == tuple()
    assert _Container.p11.overridden == tuple()


def test_copy():
    @containers.copy(ContainerA)
    class _Container1(ContainerA):
        pass

    @containers.copy(ContainerA)
    class _Container2(ContainerA):
        pass

    assert ContainerA.p11 is not _Container1.p11
    assert ContainerA.p12 is not _Container1.p12

    assert ContainerA.p11 is not _Container2.p11
    assert ContainerA.p12 is not _Container2.p12

    assert _Container1.p11 is not _Container2.p11
    assert _Container1.p12 is not _Container2.p12


def test_copy_with_replacing():
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

    assert _Container.p11 is not _Container1.p11
    assert _Container.p12 is not _Container1.p12

    assert _Container.p11 is not _Container2.p11
    assert _Container.p12 is not _Container2.p12

    assert _Container1.p11 is not _Container2.p11
    assert _Container1.p12 is not _Container2.p12

    assert _Container.p12() == {"p11": 0}
    assert _Container1.p12() == {"p11": 1}
    assert _Container2.p12() == {"p11": 2}

    assert _Container1.p13() == 11
    assert _Container2.p13() == 22


def test_copy_with_parent_dependency():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/477
    class Base(containers.DeclarativeContainer):
        p11 = providers.Object(0)
        p12 = providers.Factory(dict, p11=p11)

    @containers.copy(Base)
    class New(Base):
        p13 = providers.Factory(dict, p12=Base.p12)

    new1 = New()
    new2 = New(p11=1)
    new3 = New(p11=2)

    assert new1.p13() == {"p12": {"p11": 0}}
    assert new2.p13() == {"p12": {"p11": 1}}
    assert new3.p13() == {"p12": {"p11": 2}}


def test_copy_with_replacing_subcontainer_providers():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/374
    class X(containers.DeclarativeContainer):
        foo = providers.Dependency(instance_of=str)

    def build_x():
        return X(foo="1")

    class A(containers.DeclarativeContainer):
        x = providers.DependenciesContainer(**X.providers)
        y = x.foo

    @containers.copy(A)
    class B1(A):
        x = providers.Container(build_x)

    b1 = B1()

    assert b1.y() == "1"


def test_containers_attribute():
    class Container(containers.DeclarativeContainer):
        class Container1(containers.DeclarativeContainer):
            pass

        class Container2(containers.DeclarativeContainer):
            pass

        Container3 = containers.DynamicContainer()

    assert Container.containers == dict(
        Container1=Container.Container1,
        Container2=Container.Container2,
        Container3=Container.Container3,
    )


def test_init_with_overriding_providers():
    p1 = providers.Provider()
    p2 = providers.Provider()

    container = ContainerA(p11=p1, p12=p2)

    assert container.p11.last_overriding is p1
    assert container.p12.last_overriding is p2


def test_init_with_overridden_dependency():
    # Bug: https://github.com/ets-labs/python-dependency-injector/issues/198
    class _Container(containers.DeclarativeContainer):
        p1 = providers.Dependency(instance_of=int)

        p2 = providers.Dependency(object)
        p2.override(providers.Factory(dict, p1=p1))

    container = _Container(p1=1)

    assert container.p2() == {"p1": 1}
    assert container.p2.last_overriding.kwargs["p1"] is container.p1
    assert container.p2.last_overriding.kwargs["p1"] is not _Container.p1
    assert _Container.p2.last_overriding.kwargs["p1"] is _Container.p1


def test_init_with_chained_dependency():
    # Bug: https://github.com/ets-labs/python-dependency-injector/issues/200
    class _Container(containers.DeclarativeContainer):
        p1 = providers.Dependency(instance_of=int)
        p2 = providers.Factory(p1)

    container = _Container(p1=1)

    assert container.p2() == 1
    assert container.p2.cls is container.p1
    assert _Container.p2.cls is _Container.p1
    assert container.p2.cls is not _Container.p1


def test_init_with_dependency_delegation():
    # Bug: https://github.com/ets-labs/python-dependency-injector/issues/235
    A = collections.namedtuple("A", [])
    B = collections.namedtuple("B", ["fa"])
    C = collections.namedtuple("B", ["a"])

    class Services(containers.DeclarativeContainer):
        a = providers.Dependency()
        c = providers.Factory(C, a=a)
        b = providers.Factory(B, fa=a.provider)

    a = providers.Factory(A)
    assert isinstance(Services(a=a).c().a, A)  # OK
    Services(a=a).b().fa()


def test_init_with_grand_child_provider():
    # Bug: https://github.com/ets-labs/python-dependency-injector/issues/350
    provider = providers.Provider()
    container = ContainerC(p11=provider)

    assert isinstance(container.p11, providers.Provider)
    assert isinstance(container.p12, providers.Provider)
    assert isinstance(container.p21, providers.Provider)
    assert isinstance(container.p22, providers.Provider)
    assert isinstance(container.p31, providers.Provider)
    assert isinstance(container.p32, providers.Provider)
    assert container.p11.last_overriding is provider


def test_parent_set_in__new__():
    class Container(containers.DeclarativeContainer):
        dependency = providers.Dependency()
        dependencies_container = providers.DependenciesContainer()
        container = providers.Container(ContainerA)

    assert Container.dependency.parent is Container
    assert Container.dependencies_container.parent is Container
    assert Container.container.parent is Container


def test_parent_set_in__setattr__():
    class Container(containers.DeclarativeContainer):
        pass

    Container.dependency = providers.Dependency()
    Container.dependencies_container = providers.DependenciesContainer()
    Container.container = providers.Container(ContainerA)

    assert Container.dependency.parent is Container
    assert Container.dependencies_container.parent is Container
    assert Container.container.parent is Container


def test_resolve_provider_name():
    assert ContainerA.resolve_provider_name(ContainerA.p11) == "p11"


def test_resolve_provider_name_no_provider():
    with raises(errors.Error):
        ContainerA.resolve_provider_name(providers.Provider())


def test_child_dependency_parent_name():
    class Container(containers.DeclarativeContainer):
        dependency = providers.Dependency()

    with raises(errors.Error, match="Dependency \"Container.dependency\" is not defined"):
        Container.dependency()


def test_child_dependencies_container_parent_name():
    class Container(containers.DeclarativeContainer):
        dependencies_container = providers.DependenciesContainer()

    with raises(errors.Error, match="Dependency \"Container.dependencies_container.dependency\" is not defined"):
        Container.dependencies_container.dependency()


def test_child_container_parent_name():
    class ChildContainer(containers.DeclarativeContainer):
        dependency = providers.Dependency()

    class Container(containers.DeclarativeContainer):
        child_container = providers.Container(ChildContainer)

    with raises(errors.Error, match="Dependency \"Container.child_container.dependency\" is not defined"):
        Container.child_container.dependency()
