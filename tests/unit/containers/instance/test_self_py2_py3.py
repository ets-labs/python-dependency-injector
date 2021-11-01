"""Tests for container self provider."""

from dependency_injector import containers, providers, errors
from pytest import raises


def test_self():
    def call_bar(container):
        return container.bar()

    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()
        foo = providers.Callable(call_bar, __self__)
        bar = providers.Object("hello")

    container = Container()
    assert container.foo() is "hello"


def test_self_attribute_implicit():
    class Container(containers.DeclarativeContainer):
        pass

    container = Container()
    assert container.__self__() is container


def test_self_attribute_explicit():
    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()

    container = Container()
    assert container.__self__() is container


def test_single_self():
    with raises(errors.Error):
        class Container(containers.DeclarativeContainer):
            self1 = providers.Self()
            self2 = providers.Self()


def test_self_attribute_alt_name_implicit():
    class Container(containers.DeclarativeContainer):
        foo = providers.Self()

    container = Container()

    assert container.__self__ is container.foo
    assert set(container.__self__.alt_names) == {"foo"}


def test_self_attribute_alt_name_explicit_1():
    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()
        foo = __self__
        bar = __self__

    container = Container()

    assert container.__self__ is container.foo
    assert container.__self__ is container.bar
    assert set(container.__self__.alt_names) == {"foo", "bar"}


def test_self_attribute_alt_name_explicit_2():
    class Container(containers.DeclarativeContainer):
        foo = providers.Self()
        bar = foo

    container = Container()

    assert container.__self__ is container.foo
    assert container.__self__ is container.bar
    assert set(container.__self__.alt_names) == {"foo", "bar"}


def test_providers_attribute_1():
    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()
        foo = __self__
        bar = __self__

    container = Container()

    assert container.providers == {}
    assert Container.providers == {}


def test_providers_attribute_2():
    class Container(containers.DeclarativeContainer):
        foo = providers.Self()
        bar = foo

    container = Container()

    assert container.providers == {}
    assert Container.providers == {}


def test_container_multiple_instances():
    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()

    container1 = Container()
    container2 = Container()

    assert container1 is not container2
    assert container1.__self__() is container1
    assert container2.__self__() is container2


def test_deepcopy():
    def call_bar(container):
        return container.bar()

    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()
        foo = providers.Callable(call_bar, __self__)
        bar = providers.Object("hello")

    container1 = Container()
    container2 = providers.deepcopy(container1)
    container1.bar.override("bye")

    assert container1.foo() == "bye"
    assert container2.foo() == "hello"


def test_deepcopy_alt_names_1():
    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()
        foo = __self__
        bar = foo

    container1 = Container()
    container2 = providers.deepcopy(container1)

    assert container2.__self__() is container2
    assert container2.foo() is container2
    assert container2.bar() is container2


def test_deepcopy_alt_names_2():
    class Container(containers.DeclarativeContainer):
        self = providers.Self()

    container1 = Container()
    container2 = providers.deepcopy(container1)

    assert container2.__self__() is container2
    assert container2.self() is container2


def test_deepcopy_no_self_dependencies():
    class Container(containers.DeclarativeContainer):
        __self__ = providers.Self()

    container1 = Container()
    container2 = providers.deepcopy(container1)

    assert container1 is not container2
    assert container1.__self__ is not container2.__self__
    assert container1.__self__() is container1
    assert container2.__self__() is container2


def test_with_container_provider():
    def call_bar(container):
        return container.bar()

    class SubContainer(containers.DeclarativeContainer):
        __self__ = providers.Self()
        foo = providers.Callable(call_bar, __self__)
        bar = providers.Object("hello")

    class Container(containers.DeclarativeContainer):
        sub_container = providers.Container(SubContainer)

        baz = providers.Callable(lambda value: value, sub_container.foo)

    container = Container()
    assert container.baz() == "hello"


def test_with_container_provider_overriding():
    def call_bar(container):
        return container.bar()

    class SubContainer(containers.DeclarativeContainer):
        __self__ = providers.Self()
        foo = providers.Callable(call_bar, __self__)
        bar = providers.Object("hello")

    class Container(containers.DeclarativeContainer):
        sub_container = providers.Container(SubContainer, bar="bye")

        baz = providers.Callable(lambda value: value, sub_container.foo)

    container = Container()
    assert container.baz() == "bye"


def test_with_container_provider_self():
    class SubContainer(containers.DeclarativeContainer):
        __self__ = providers.Self()

    class Container(containers.DeclarativeContainer):
        sub_container = providers.Container(SubContainer)

    container = Container()

    assert container.__self__() is container
    assert container.sub_container().__self__() is container.sub_container()

