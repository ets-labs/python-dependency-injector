"""Regression tests for Self dependencies in copied containers."""

from dependency_injector import containers, providers


def test_copy_rebinds_base_self_and_preserves_source_instances():
    class Base(containers.DeclarativeContainer):
        __self__ = providers.Self()
        value = providers.Object("base")
        consumer = providers.Singleton(dict, container=__self__)

    @containers.copy(Base)
    class Copied(Base):
        value = providers.Object("copy")

    original = Base()
    first = Copied()
    second = Copied()
    for instance in (original, first, second):
        assert instance.consumer()["container"] is instance
        assert instance.__self__() is instance
    assert original.consumer()["container"].value() == "base"
    assert first.consumer()["container"].value() == "copy"
    assert first.consumer() is not second.consumer()
    assert Base.consumer()["container"] is Base
    assert Copied.consumer()["container"] is Copied


def test_copy_rebinds_target_self_and_its_aliases():
    class Base(containers.DeclarativeContainer):
        __self__ = providers.Self()
        inherited = providers.Factory(dict, container=__self__)

    @containers.copy(Base)
    class Copied(Base):
        this = providers.Self()
        also_this = this
        own = providers.Factory(dict, container=this)

    instance = Copied()
    assert instance.inherited()["container"] is instance
    assert instance.own()["container"] is instance
    assert instance.this() is instance
    assert instance.also_this is instance.this is instance.__self__
    assert "this" not in instance.providers
    assert "also_this" not in instance.providers
    assert Base.__self__() is Base


def test_copy_rebinds_self_through_delegated_and_provided_dependencies():
    class Base(containers.DeclarativeContainer):
        __self__ = providers.Self()
        value = providers.Object("base")
        delegated = providers.Factory(dict, provider=__self__.provider)
        provided = providers.Callable(str, __self__.provided.value.call())

    @containers.copy(Base)
    class Copied(Base):
        value = providers.Object("copy")

    original = Base()
    instance = Copied()
    assert instance.delegated()["provider"]() is instance
    assert instance.provided() == "copy"
    assert original.delegated()["provider"]() is original
    assert original.provided() == "base"


def test_repeated_copy_and_deepcopy_keep_the_current_container():
    class Base(containers.DeclarativeContainer):
        __self__ = providers.Self()
        consumer = providers.Factory(dict, container=__self__)

    @containers.copy(Base)
    class First(Base):
        pass

    @containers.copy(First)
    class Second(First):
        pass

    instances = [Base(), First(), Second()]
    instances.append(providers.deepcopy(instances[-1]))
    for instance in instances:
        assert instance.consumer()["container"] is instance


def test_copy_uses_self_for_resource_lifecycle():
    initialized = []
    stopped = []

    def init_resource(owner):
        initialized.append(owner)
        yield owner
        stopped.append(owner)

    class Base(containers.DeclarativeContainer):
        __self__ = providers.Self()
        resource = providers.Resource(init_resource, __self__)

    @containers.copy(Base)
    class Copied(Base):
        pass

    instance = Copied()
    instance.init_resources()
    assert initialized == [instance]
    assert instance.resource() is instance
    instance.shutdown_resources()
    assert stopped == [instance]
    assert not Base.resource.initialized


def test_copy_keeps_self_of_an_independent_nested_container():
    class Child(containers.DeclarativeContainer):
        __self__ = providers.Self()
        consumer = providers.Factory(dict, container=__self__)

    class Base(containers.DeclarativeContainer):
        __self__ = providers.Self()
        child = providers.Container(Child)
        consumer = providers.Factory(dict, container=__self__, child=child)

    @containers.copy(Base)
    class Copied(Base):
        pass

    instance = Copied()
    child = instance.child()
    assert instance.consumer()["container"] is instance
    assert instance.consumer()["child"] is child
    assert child.consumer()["container"] is child
    assert child.__self__() is child
