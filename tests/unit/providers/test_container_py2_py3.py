"""Container provider tests."""

import copy

from dependency_injector import containers, providers, errors
from pytest import raises


TEST_VALUE_1 = "core_section_value1"
TEST_CONFIG_1 = {
    "core": {
        "section": {
            "value": TEST_VALUE_1,
        },
    },
}

TEST_VALUE_2 = "core_section_value2"
TEST_CONFIG_2 = {
    "core": {
        "section": {
            "value": TEST_VALUE_2,
        },
    },
}


def _copied(value):
    return copy.deepcopy(value)


class Core(containers.DeclarativeContainer):
    config = providers.Configuration("core")
    value_getter = providers.Callable(lambda _: _, config.section.value)


class Application(containers.DeclarativeContainer):
    config = providers.Configuration("config")
    core = providers.Container(Core, config=config.core)
    dict_factory = providers.Factory(dict, value=core.value_getter)


def test():
    application = Application(config=_copied(TEST_CONFIG_1))
    assert application.dict_factory() == {"value": TEST_VALUE_1}


def test_double_override():
    application = Application()
    application.config.override(_copied(TEST_CONFIG_1))
    application.config.override(_copied(TEST_CONFIG_2))
    assert application.dict_factory() == {"value": TEST_VALUE_2}


def test_override():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/354
    class D(containers.DeclarativeContainer):
        foo = providers.Object("foo")

    class A(containers.DeclarativeContainer):
        d = providers.DependenciesContainer()
        bar = providers.Callable(lambda f: f + "++", d.foo.provided)

    class B(containers.DeclarativeContainer):
        d = providers.Container(D)

        a = providers.Container(A, d=d)

    b = B(d=D())
    result = b.a().bar()
    assert result == "foo++"


def test_override_not_root_provider():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/379
    class NestedContainer(containers.DeclarativeContainer):
        settings = providers.Configuration()

        print_settings = providers.Callable(
            lambda s: s,
            settings,
        )

    class TestContainer(containers.DeclarativeContainer):
        settings = providers.Configuration()

        root_container = providers.Container(
            NestedContainer,
            settings=settings,
        )

        not_root_container = providers.Selector(
            settings.container,
            using_factory=providers.Factory(
                NestedContainer,
                settings=settings,
            ),
            using_container=providers.Container(
                NestedContainer,
                settings=settings,
            )
        )

    container_using_factory = TestContainer(settings=dict(
        container="using_factory",
        foo="bar"
    ))
    assert container_using_factory.root_container().print_settings() == {"container": "using_factory", "foo": "bar"}
    assert container_using_factory.not_root_container().print_settings() == {"container": "using_factory", "foo": "bar"}

    container_using_container = TestContainer(settings=dict(
        container="using_container",
        foo="bar"
    ))
    assert container_using_container.root_container().print_settings() == {"container": "using_container", "foo": "bar"}
    assert container_using_container.not_root_container().print_settings() == {"container": "using_container", "foo": "bar"}


def test_override_by_not_a_container():
    provider = providers.Container(Core)

    with raises(errors.Error):
        provider.override(providers.Object("foo"))


def test_lazy_overriding():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/354
    class D(containers.DeclarativeContainer):
        foo = providers.Object("foo")

    class A(containers.DeclarativeContainer):
        d = providers.DependenciesContainer()
        bar = providers.Callable(lambda f: f + "++", d.foo.provided)

    class B(containers.DeclarativeContainer):
        d = providers.DependenciesContainer()

        a = providers.Container(A, d=d)

    b = B(d=D())
    result = b.a().bar()
    assert result == "foo++"


def test_lazy_overriding_deep():
    # Extended version of test_lazy_overriding()
    class D(containers.DeclarativeContainer):
        foo = providers.Object("foo")

    class C(containers.DeclarativeContainer):
        d = providers.DependenciesContainer()
        bar = providers.Callable(lambda f: f + "++", d.foo.provided)

    class A(containers.DeclarativeContainer):
        d = providers.DependenciesContainer()
        c = providers.Container(C, d=d)

    class B(containers.DeclarativeContainer):
        d = providers.DependenciesContainer()

        a = providers.Container(A, d=d)

    b = B(d=D())
    result = b.a().c().bar()
    assert result == "foo++"


def test_reset_last_overriding():
    application = Application(config=_copied(TEST_CONFIG_1))
    application.core.override(Core(config=_copied(TEST_CONFIG_2["core"])))

    application.core.reset_last_overriding()

    assert application.dict_factory() == {"value": TEST_VALUE_1}


def test_reset_last_overriding_only_overridden():
    application = Application(config=_copied(TEST_CONFIG_1))
    application.core.override(providers.DependenciesContainer(config=_copied(TEST_CONFIG_2["core"])))

    application.core.reset_last_overriding()

    assert application.dict_factory() == {"value": TEST_VALUE_1}


def test_override_context_manager():
    application = Application(config=_copied(TEST_CONFIG_1))
    overriding_core = Core(config=_copied(TEST_CONFIG_2["core"]))

    with application.core.override(overriding_core) as context_core:
        assert application.dict_factory() == {"value": TEST_VALUE_2}
        assert context_core() is overriding_core

    assert application.dict_factory() == {"value": TEST_VALUE_1}


def test_reset_override():
    application = Application(config=_copied(TEST_CONFIG_1))
    application.core.override(Core(config=_copied(TEST_CONFIG_2["core"])))

    application.core.reset_override()

    assert application.dict_factory() == {"value": None}


def test_reset_override_only_overridden():
    application = Application(config=_copied(TEST_CONFIG_1))
    application.core.override(providers.DependenciesContainer(config=_copied(TEST_CONFIG_2["core"])))

    application.core.reset_override()

    assert application.dict_factory() == {"value": None}


def test_assign_parent():
    parent = providers.DependenciesContainer()
    provider = providers.Container(Core)

    provider.assign_parent(parent)

    assert provider.parent is parent


def test_parent_name():
    container = containers.DynamicContainer()
    provider = providers.Container(Core)
    container.name = provider
    assert provider.parent_name == "name"


def test_parent_name_with_deep_parenting():
    provider = providers.Container(Core)
    container = providers.DependenciesContainer(name=provider)
    _ = providers.DependenciesContainer(container=container)
    assert provider.parent_name == "container.name"


def test_parent_name_is_none():
    provider = providers.Container(Core)
    assert provider.parent_name is None


def test_parent_deepcopy():
    container = containers.DynamicContainer()
    provider = providers.Container(Core)
    container.name = provider

    copied = providers.deepcopy(container)

    assert container.name.parent is container
    assert copied.name.parent is copied

    assert container is not copied
    assert container.name is not copied.name
    assert container.name.parent is not copied.name.parent


def test_resolve_provider_name():
    container = providers.Container(Core)
    assert container.resolve_provider_name(container.value_getter) == "value_getter"


def test_resolve_provider_name_no_provider():
    container = providers.Container(Core)
    with raises(errors.Error):
        container.resolve_provider_name(providers.Provider())
