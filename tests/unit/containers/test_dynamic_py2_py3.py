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

    def test_reset_last_overriding(self):
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

    def test_reset_last_overriding_when_not_overridden(self):
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

    def test_reset_singletons(self):
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

        self.assertIs(obj11, obj21)
        self.assertIs(obj12, obj22)
        self.assertIs(obj13, obj23)

        container.reset_singletons()

        obj31 = container.singleton()
        obj32 = container.sub_container().singleton()
        obj33 = container.sub_container().sub_sub_container().singleton()

        obj41 = container.singleton()
        obj42 = container.sub_container().singleton()
        obj43 = container.sub_container().sub_sub_container().singleton()

        self.assertIsNot(obj11, obj31)
        self.assertIsNot(obj12, obj32)
        self.assertIsNot(obj13, obj33)

        self.assertIsNot(obj21, obj31)
        self.assertIsNot(obj22, obj32)
        self.assertIsNot(obj23, obj33)

        self.assertIs(obj31, obj41)
        self.assertIs(obj32, obj42)
        self.assertIs(obj33, obj43)

    def test_check_dependencies(self):
        class SubContainer(containers.DeclarativeContainer):
            dependency = providers.Dependency()

        class Container(containers.DeclarativeContainer):
            dependency = providers.Dependency()
            dependencies_container = providers.DependenciesContainer()
            provider = providers.List(dependencies_container.dependency)
            sub_container = providers.Container(SubContainer)

        container = Container()

        with self.assertRaises(errors.Error) as context:
            container.check_dependencies()

        self.assertIn('Container "Container" has undefined dependencies:', str(context.exception))
        self.assertIn('"Container.dependency"', str(context.exception))
        self.assertIn('"Container.dependencies_container.dependency"', str(context.exception))
        self.assertIn('"Container.sub_container.dependency"', str(context.exception))

    def test_check_dependencies_all_defined(self):
        class Container(containers.DeclarativeContainer):
            dependency = providers.Dependency()

        container = Container(dependency='provided')
        result = container.check_dependencies()

        self.assertIsNone(result)

    def test_assign_parent(self):
        parent = providers.DependenciesContainer()
        container = ContainerA()

        container.assign_parent(parent)

        self.assertIs(container.parent, parent)

    def test_parent_name_declarative_parent(self):
        container = ContainerA()
        self.assertEqual(container.parent_name, 'ContainerA')

    def test_parent_name(self):
        container = ContainerA()
        self.assertEqual(container.parent_name, 'ContainerA')

    def test_parent_name_with_deep_parenting(self):
        class Container2(containers.DeclarativeContainer):

            name = providers.Container(ContainerA)

        class Container1(containers.DeclarativeContainer):

            container = providers.Container(Container2)

        container = Container1()
        self.assertEqual(container.container().name.parent_name, 'Container1.container.name')

    def test_parent_name_is_none(self):
        container = containers.DynamicContainer()
        self.assertIsNone(container.parent_name)

    def test_parent_deepcopy(self):
        class Container(containers.DeclarativeContainer):
            container = providers.Container(ContainerA)

        container = Container()

        copied = providers.deepcopy(container)

        self.assertIs(container.container.parent, container)
        self.assertIs(copied.container.parent, copied)

        self.assertIsNot(container, copied)
        self.assertIsNot(container.container, copied.container)
        self.assertIsNot(container.container.parent, copied.container.parent)

    def test_resolve_provider_name(self):
        container = ContainerA()
        self.assertEqual(container.resolve_provider_name(container.p11), 'p11')

    def test_resolve_provider_name_no_provider(self):
        container = ContainerA()
        with self.assertRaises(errors.Error):
            container.resolve_provider_name(providers.Provider())


class SelfTests(unittest.TestCase):

    def test_self(self):
        def call_bar(container):
            return container.bar()

        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()
            foo = providers.Callable(call_bar, __self__)
            bar = providers.Object('hello')

        container = Container()

        self.assertIs(container.foo(), 'hello')

    def test_self_attribute_implicit(self):
        class Container(containers.DeclarativeContainer):
            pass

        container = Container()

        self.assertIs(container.__self__(), container)

    def test_self_attribute_explicit(self):
        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()

        container = Container()

        self.assertIs(container.__self__(), container)

    def test_single_self(self):
        with self.assertRaises(errors.Error):
            class Container(containers.DeclarativeContainer):
                self1 = providers.Self()
                self2 = providers.Self()

    def test_self_attribute_alt_name_implicit(self):
        class Container(containers.DeclarativeContainer):
            foo = providers.Self()

        container = Container()

        self.assertIs(container.__self__, container.foo)
        self.assertEqual(set(container.__self__.alt_names), {'foo'})

    def test_self_attribute_alt_name_explicit_1(self):
        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()
            foo = __self__
            bar = __self__

        container = Container()

        self.assertIs(container.__self__, container.foo)
        self.assertIs(container.__self__, container.bar)
        self.assertEqual(set(container.__self__.alt_names), {'foo', 'bar'})

    def test_self_attribute_alt_name_explicit_2(self):
        class Container(containers.DeclarativeContainer):
            foo = providers.Self()
            bar = foo

        container = Container()

        self.assertIs(container.__self__, container.foo)
        self.assertIs(container.__self__, container.bar)
        self.assertEqual(set(container.__self__.alt_names), {'foo', 'bar'})

    def test_providers_attribute_1(self):
        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()
            foo = __self__
            bar = __self__

        container = Container()

        self.assertEqual(container.providers, {})
        self.assertEqual(Container.providers, {})

    def test_providers_attribute_2(self):
        class Container(containers.DeclarativeContainer):
            foo = providers.Self()
            bar = foo

        container = Container()

        self.assertEqual(container.providers, {})
        self.assertEqual(Container.providers, {})

    def test_container_multiple_instances(self):
        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()

        container1 = Container()
        container2 = Container()

        self.assertIsNot(container1, container2)
        self.assertIs(container1.__self__(), container1)
        self.assertIs(container2.__self__(), container2)

    def test_deepcopy(self):
        def call_bar(container):
            return container.bar()

        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()
            foo = providers.Callable(call_bar, __self__)
            bar = providers.Object('hello')

        container1 = Container()
        container2 = providers.deepcopy(container1)
        container1.bar.override('bye')

        self.assertIs(container1.foo(), 'bye')
        self.assertIs(container2.foo(), 'hello')

    def test_deepcopy_alt_names_1(self):
        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()
            foo = __self__
            bar = foo

        container1 = Container()
        container2 = providers.deepcopy(container1)

        self.assertIs(container2.__self__(), container2)
        self.assertIs(container2.foo(), container2)
        self.assertIs(container2.bar(), container2)

    def test_deepcopy_alt_names_2(self):
        class Container(containers.DeclarativeContainer):
            self = providers.Self()

        container1 = Container()
        container2 = providers.deepcopy(container1)

        self.assertIs(container2.__self__(), container2)
        self.assertIs(container2.self(), container2)

    def test_deepcopy_no_self_dependencies(self):
        class Container(containers.DeclarativeContainer):
            __self__ = providers.Self()

        container1 = Container()
        container2 = providers.deepcopy(container1)

        self.assertIsNot(container1, container2)
        self.assertIsNot(container1.__self__, container2.__self__)
        self.assertIs(container1.__self__(), container1)
        self.assertIs(container2.__self__(), container2)

    def test_with_container_provider(self):
        def call_bar(container):
            return container.bar()

        class SubContainer(containers.DeclarativeContainer):
            __self__ = providers.Self()
            foo = providers.Callable(call_bar, __self__)
            bar = providers.Object('hello')

        class Container(containers.DeclarativeContainer):
            sub_container = providers.Container(SubContainer)

            baz = providers.Callable(lambda value: value, sub_container.foo)

        container = Container()

        self.assertIs(container.baz(), 'hello')

    def test_with_container_provider_overriding(self):
        def call_bar(container):
            return container.bar()

        class SubContainer(containers.DeclarativeContainer):
            __self__ = providers.Self()
            foo = providers.Callable(call_bar, __self__)
            bar = providers.Object('hello')

        class Container(containers.DeclarativeContainer):
            sub_container = providers.Container(SubContainer, bar='bye')

            baz = providers.Callable(lambda value: value, sub_container.foo)

        container = Container()

        self.assertIs(container.baz(), 'bye')

    def test_with_container_provider_self(self):
        class SubContainer(containers.DeclarativeContainer):
            __self__ = providers.Self()

        class Container(containers.DeclarativeContainer):
            sub_container = providers.Container(SubContainer)

        container = Container()

        self.assertIs(container.__self__(), container)
        self.assertIs(container.sub_container().__self__(), container.sub_container())
