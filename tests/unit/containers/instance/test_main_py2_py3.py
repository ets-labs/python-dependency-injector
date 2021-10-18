"""Main container instance tests."""

from dependency_injector import containers, providers, errors
from pytest import raises


class Container(containers.DeclarativeContainer):
    p11 = providers.Provider()
    p12 = providers.Provider()


def test_providers_attribute():
    container_1 = Container()
    container_2 = Container()

    assert container_1.p11 is not container_2.p11
    assert container_1.p12 is not container_2.p12
    assert container_1.providers != container_2.providers


def test_dependencies_attribute():
    container = Container()
    container.a1 = providers.Dependency()
    container.a2 = providers.DependenciesContainer()
    assert container.dependencies == {"a1": container.a1, "a2": container.a2}


def test_set_get_del_providers():
    p13 = providers.Provider()

    container_1 = Container()
    container_2 = Container()

    container_1.p13 = p13
    container_2.p13 = p13

    assert Container.providers == dict(p11=Container.p11, p12=Container.p12)
    assert Container.cls_providers, dict(p11=Container.p11, p12=Container.p12)

    assert container_1.providers == dict(p11=container_1.p11, p12=container_1.p12, p13=p13)
    assert container_2.providers == dict(p11=container_2.p11, p12=container_2.p12, p13=p13)

    del container_1.p13
    assert container_1.providers == dict(p11=container_1.p11, p12=container_1.p12)

    del container_2.p13
    assert container_2.providers == dict(p11=container_2.p11, p12=container_2.p12)

    del container_1.p11
    del container_1.p12
    assert container_1.providers == dict()
    assert Container.providers == dict(p11=Container.p11, p12=Container.p12)

    del container_2.p11
    del container_2.p12
    assert container_2.providers == dict()
    assert Container.providers == dict(p11=Container.p11, p12=Container.p12)


def test_set_invalid_provider_type():
    container = Container()
    container.provider_type = providers.Object

    with raises(errors.Error):
        container.px = providers.Provider()

    assert Container.provider_type is containers.DeclarativeContainer.provider_type


def test_set_providers():
    p13 = providers.Provider()
    p14 = providers.Provider()
    container = Container()

    container.set_providers(p13=p13, p14=p14)

    assert container.p13 is p13
    assert container.p14 is p14


def test_override():
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

    assert container.overridden == (overriding_container1, overriding_container2)
    assert container.p11.overridden == (overriding_container1.p11, overriding_container2.p11)

    assert _Container.overridden == tuple()
    assert _Container.p11.overridden == tuple()


def test_override_with_it():
    container = Container()
    with raises(errors.Error):
        container.override(container)


def test_override_providers():
    p1 = providers.Provider()
    p2 = providers.Provider()
    container = Container()

    container.override_providers(p11=p1, p12=p2)

    assert container.p11.last_overriding is p1
    assert container.p12.last_overriding is p2


def test_override_providers_context_manager():
    p1 = providers.Provider()
    p2 = providers.Provider()
    container = Container()

    with container.override_providers(p11=p1, p12=p2) as context_container:
        assert container is context_container
        assert container.p11.last_overriding is p1
        assert container.p12.last_overriding is p2

    assert container.p11.last_overriding is None
    assert container.p12.last_overriding is None


def test_override_providers_with_unknown_provider():
    container = Container()
    with raises(AttributeError):
        container.override_providers(unknown=providers.Provider())


def test_reset_last_overriding():
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

    assert container.overridden == (overriding_container1,)
    assert container.p11.overridden, (overriding_container1.p11,)


def test_reset_last_overriding_when_not_overridden():
    container = Container()
    with raises(errors.Error):
        container.reset_last_overriding()


def test_reset_override():
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

    assert container.overridden == tuple()
    assert container.p11.overridden == tuple()


def test_init_and_shutdown_resources_ordering():
    """Test init and shutdown resources.

    Methods .init_resources() and .shutdown_resources() should respect resources dependencies.
    Initialization should first initialize resources without dependencies and then provide
    these resources to other resources. Resources shutdown should follow the same rule: first
    shutdown resources without initialized dependencies and then continue correspondingly
    until all resources are shutdown.
    """
    initialized_resources = []
    shutdown_resources = []

    def _resource(name, **_):
        initialized_resources.append(name)
        yield name
        shutdown_resources.append(name)

    class Container(containers.DeclarativeContainer):
        resource1 = providers.Resource(
            _resource,
            name="r1",
        )
        resource2 = providers.Resource(
            _resource,
            name="r2",
            r1=resource1,
        )
        resource3 = providers.Resource(
            _resource,
            name="r3",
            r2=resource2,
        )

    container = Container()

    container.init_resources()
    assert initialized_resources == ["r1", "r2", "r3"]
    assert shutdown_resources == []

    container.shutdown_resources()
    assert initialized_resources == ["r1", "r2", "r3"]
    assert shutdown_resources == ["r3", "r2", "r1"]

    container.init_resources()
    assert initialized_resources == ["r1", "r2", "r3", "r1", "r2", "r3"]
    assert shutdown_resources == ["r3", "r2", "r1"]

    container.shutdown_resources()
    assert initialized_resources == ["r1", "r2", "r3", "r1", "r2", "r3"]
    assert shutdown_resources == ["r3", "r2", "r1", "r3", "r2", "r1"]


def test_shutdown_resources_circular_dependencies_breaker():
    def _resource(name, **_):
        yield name

    class Container(containers.DeclarativeContainer):
        resource1 = providers.Resource(
            _resource,
            name="r1",
        )
        resource2 = providers.Resource(
            _resource,
            name="r2",
            r1=resource1,
        )
        resource3 = providers.Resource(
            _resource,
            name="r3",
            r2=resource2,
        )

    container = Container()
    container.init_resources()

    # Create circular dependency after initialization (r3 -> r2 -> r1 -> r3 -> ...)
    container.resource1.add_kwargs(r3=container.resource3)

    with raises(RuntimeError, match="Unable to resolve resources shutdown order"):
        container.shutdown_resources()


def test_init_shutdown_nested_resources():
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
    assert _init1.init_counter == 0
    assert _init1.shutdown_counter == 0
    assert _init2.init_counter == 0
    assert _init2.shutdown_counter == 0

    container.init_resources()
    assert _init1.init_counter == 1
    assert _init1.shutdown_counter == 0
    assert _init2.init_counter == 1
    assert _init2.shutdown_counter == 0

    container.shutdown_resources()
    assert _init1.init_counter == 1
    assert _init1.shutdown_counter == 1
    assert _init2.init_counter == 1
    assert _init2.shutdown_counter == 1

    container.init_resources()
    container.shutdown_resources()
    assert _init1.init_counter == 2
    assert _init1.shutdown_counter == 2
    assert _init2.init_counter == 2
    assert _init2.shutdown_counter == 2


def test_reset_singletons():
    class SubSubContainer(containers.DeclarativeContainer):
        singleton = providers.Singleton(object)

    class SubContainer(containers.DeclarativeContainer):
        singleton = providers.Singleton(object)
        sub_sub_container = providers.Container(SubSubContainer)

    class Container(containers.DeclarativeContainer):
        singleton = providers.Singleton(object)
        sub_container = providers.Container(SubContainer)

    container = Container()

    obj11 = container.singleton()
    obj12 = container.sub_container().singleton()
    obj13 = container.sub_container().sub_sub_container().singleton()

    obj21 = container.singleton()
    obj22 = container.sub_container().singleton()
    obj23 = container.sub_container().sub_sub_container().singleton()

    assert obj11 is obj21
    assert obj12 is obj22
    assert obj13 is obj23

    container.reset_singletons()

    obj31 = container.singleton()
    obj32 = container.sub_container().singleton()
    obj33 = container.sub_container().sub_sub_container().singleton()

    obj41 = container.singleton()
    obj42 = container.sub_container().singleton()
    obj43 = container.sub_container().sub_sub_container().singleton()

    assert obj11 is not obj31
    assert obj12 is not obj32
    assert obj13 is not obj33

    assert obj21 is not obj31
    assert obj22 is not obj32
    assert obj23 is not obj33

    assert obj31 is obj41
    assert obj32 is obj42
    assert obj33 is obj43


def test_reset_singletons_context_manager():
    class Item:
        def __init__(self, dependency):
            self.dependency = dependency

    class Container(containers.DeclarativeContainer):
        dependent = providers.Singleton(object)
        singleton = providers.Singleton(Item, dependency=dependent)

    container = Container()

    instance1 = container.singleton()
    with container.reset_singletons():
        instance2 = container.singleton()
    instance3 = container.singleton()

    assert len({instance1, instance2, instance3}) == 3
    assert len({instance1.dependency, instance2.dependency, instance3.dependency}) == 3


def test_reset_singletons_context_manager_as_attribute():
    container = containers.DeclarativeContainer()
    with container.reset_singletons() as alias:
        pass
    assert container is alias


def test_check_dependencies():
    class SubContainer(containers.DeclarativeContainer):
        dependency = providers.Dependency()

    class Container(containers.DeclarativeContainer):
        dependency = providers.Dependency()
        dependencies_container = providers.DependenciesContainer()
        provider = providers.List(dependencies_container.dependency)
        sub_container = providers.Container(SubContainer)

    container = Container()

    with raises(errors.Error) as exception_info:
        container.check_dependencies()

    assert "Container \"Container\" has undefined dependencies:" in str(exception_info.value)
    assert "\"Container.dependency\"" in str(exception_info.value)
    assert "\"Container.dependencies_container.dependency\"" in str(exception_info.value)
    assert "\"Container.sub_container.dependency\"" in str(exception_info.value)


def test_check_dependencies_all_defined():
    class Container(containers.DeclarativeContainer):
        dependency = providers.Dependency()

    container = Container(dependency="provided")
    result = container.check_dependencies()

    assert result is None


def test_assign_parent():
    parent = providers.DependenciesContainer()
    container = Container()

    container.assign_parent(parent)

    assert container.parent is parent


def test_parent_name_declarative_parent():
    container = Container()
    assert container.parent_name == "Container"


def test_parent_name():
    container = Container()
    assert container.parent_name == "Container"


def test_parent_name_with_deep_parenting():
    class Container2(containers.DeclarativeContainer):
        name = providers.Container(Container)

    class Container1(containers.DeclarativeContainer):
        container = providers.Container(Container2)

    container = Container1()
    assert container.container().name.parent_name == "Container1.container.name"


def test_parent_name_is_none():
    container = containers.DynamicContainer()
    assert container.parent_name is None


def test_parent_deepcopy():
    class ParentContainer(containers.DeclarativeContainer):
        child = providers.Container(Container)

    container = ParentContainer()
    copied = providers.deepcopy(container)

    assert container.child.parent is container
    assert copied.child.parent is copied

    assert container is not copied
    assert container.child is not copied.child
    assert container.child.parent is not copied.child.parent


def test_resolve_provider_name():
    container = Container()
    assert container.resolve_provider_name(container.p11) == "p11"


def test_resolve_provider_name_no_provider():
    container = Container()
    with raises(errors.Error):
        container.resolve_provider_name(providers.Provider())
