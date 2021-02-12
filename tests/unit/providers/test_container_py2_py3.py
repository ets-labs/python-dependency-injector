"""Dependency injector container provider unit tests."""

import copy

import unittest2 as unittest

from dependency_injector import containers, providers, errors


TEST_VALUE_1 = 'core_section_value1'
TEST_CONFIG_1 = {
    'core': {
        'section': {
            'value': TEST_VALUE_1,
        },
    },
}

TEST_VALUE_2 = 'core_section_value2'
TEST_CONFIG_2 = {
    'core': {
        'section': {
            'value': TEST_VALUE_2,
        },
    },
}


def _copied(value):
    return copy.deepcopy(value)


class TestCore(containers.DeclarativeContainer):
    config = providers.Configuration('core')
    value_getter = providers.Callable(lambda _: _, config.section.value)


class TestApplication(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    core = providers.Container(TestCore, config=config.core)
    dict_factory = providers.Factory(dict, value=core.value_getter)


class ContainerTests(unittest.TestCase):

    def test(self):
        application = TestApplication(config=_copied(TEST_CONFIG_1))
        self.assertEqual(application.dict_factory(), {'value': TEST_VALUE_1})

    def test_double_override(self):
        application = TestApplication()
        application.config.override(_copied(TEST_CONFIG_1))
        application.config.override(_copied(TEST_CONFIG_2))
        self.assertEqual(application.dict_factory(), {'value': TEST_VALUE_2})

    def test_override(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/354
        class D(containers.DeclarativeContainer):
            foo = providers.Object('foo')

        class A(containers.DeclarativeContainer):
            d = providers.DependenciesContainer()
            bar = providers.Callable(lambda f: f + '++', d.foo.provided)

        class B(containers.DeclarativeContainer):
            d = providers.Container(D)

            a = providers.Container(A, d=d)

        b = B(d=D())
        result = b.a().bar()
        self.assertEqual(result, 'foo++')

    def test_override_not_root_provider(self):
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
            container='using_factory',
            foo='bar'
        ))
        self.assertEqual(
            container_using_factory.root_container().print_settings(),
            {'container': 'using_factory', 'foo': 'bar'},
        )
        self.assertEqual(
            container_using_factory.not_root_container().print_settings(),
            {'container': 'using_factory', 'foo': 'bar'},
        )


        container_using_container = TestContainer(settings=dict(
            container='using_container',
            foo='bar'
        ))
        self.assertEqual(
            container_using_container.root_container().print_settings(),
            {'container': 'using_container', 'foo': 'bar'},
        )
        self.assertEqual(
            container_using_container.not_root_container().print_settings(),
            {'container': 'using_container', 'foo': 'bar'},
        )

    def test_override_by_not_a_container(self):
        provider = providers.Container(TestCore)

        with self.assertRaises(errors.Error):
            provider.override(providers.Object('foo'))

    def test_lazy_overriding(self):
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
        self.assertEqual(result, 'foo++')

    def test_lazy_overriding_deep(self):
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
        self.assertEqual(result, 'foo++')

    def test_assign_parent(self):
        parent = providers.DependenciesContainer()
        provider = providers.Container(TestCore)

        provider.assign_parent(parent)

        self.assertIs(provider.parent, parent)

    def test_parent_name(self):
        container = containers.DynamicContainer()
        provider = providers.Container(TestCore)
        container.name = provider
        self.assertEqual(provider.parent_name, 'name')

    def test_parent_name_with_deep_parenting(self):
        provider = providers.Container(TestCore)
        container = providers.DependenciesContainer(name=provider)
        _ = providers.DependenciesContainer(container=container)
        self.assertEqual(provider.parent_name, 'container.name')

    def test_parent_name_is_none(self):
        provider = providers.Container(TestCore)
        self.assertIsNone(provider.parent_name)

    def test_parent_deepcopy(self):
        container = containers.DynamicContainer()
        provider = providers.Container(TestCore)
        container.name = provider

        copied = providers.deepcopy(container)

        self.assertIs(container.name.parent, container)
        self.assertIs(copied.name.parent, copied)

        self.assertIsNot(container, copied)
        self.assertIsNot(container.name, copied.name)
        self.assertIsNot(container.name.parent, copied.name.parent)

    def test_resolve_provider_name(self):
        container = providers.Container(TestCore)
        self.assertEqual(container.resolve_provider_name(container.value_getter), 'value_getter')

    def test_resolve_provider_name_no_provider(self):
        container = providers.Container(TestCore)
        with self.assertRaises(errors.Error):
            container.resolve_provider_name(providers.Provider())
