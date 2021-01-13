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
        # See: https://github.com/ets-labs/python-dependency-injector/issues/354

    def test_override_by_not_a_container(self):
        provider = providers.Container(TestCore)

        with self.assertRaises(errors.Error):
            provider.override(providers.Object('foo'))

    def test_lazy_overriding(self):
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
        # See: https://github.com/ets-labs/python-dependency-injector/issues/354
