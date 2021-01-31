import unittest

from dependency_injector import containers, providers


class TraverseTests(unittest.TestCase):

    def test_traverse_cycled_graph(self):
        provider1 = providers.Provider()

        provider2 = providers.Provider()
        provider2.override(provider1)

        provider3 = providers.Provider()
        provider3.override(provider2)

        provider1.override(provider3)  # Cycle: provider3 -> provider2 -> provider1 -> provider3

        all_providers = list(providers.traverse(provider1))

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)

    def test_traverse_types_filtering(self):
        provider1 = providers.Resource(dict)
        provider2 = providers.Resource(dict)
        provider3 = providers.Provider()

        provider = providers.Provider()

        provider.override(provider1)
        provider.override(provider2)
        provider.override(provider3)

        all_providers = list(providers.traverse(provider, types=[providers.Resource]))

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)


class ProviderTests(unittest.TestCase):

    def test_traversal_overriding(self):
        provider1 = providers.Provider()
        provider2 = providers.Provider()
        provider3 = providers.Provider()

        provider = providers.Provider()

        provider.override(provider1)
        provider.override(provider2)
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)

    def test_traversal_overriding_nested(self):
        provider1 = providers.Provider()

        provider2 = providers.Provider()
        provider2.override(provider1)

        provider3 = providers.Provider()
        provider3.override(provider2)

        provider = providers.Provider()
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)

    def test_traverse_types_filtering(self):
        provider1 = providers.Resource(dict)
        provider2 = providers.Resource(dict)
        provider3 = providers.Provider()

        provider = providers.Provider()

        provider.override(provider1)
        provider.override(provider2)
        provider.override(provider3)

        all_providers = list(provider.traverse(types=[providers.Resource]))

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)


class ObjectTests(unittest.TestCase):

    def test_traversal(self):
        provider = providers.Object('string')
        all_providers = list(provider.traverse())
        self.assertEqual(len(all_providers), 0)

    def test_traversal_provider(self):
        another_provider = providers.Provider()
        provider = providers.Object(another_provider)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 1)
        self.assertIn(another_provider, all_providers)

    def test_traversal_provider_and_overriding(self):
        another_provider_1 = providers.Provider()
        another_provider_2 = providers.Provider()
        another_provider_3 = providers.Provider()

        provider = providers.Object(another_provider_1)

        provider.override(another_provider_2)
        provider.override(another_provider_3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(another_provider_1, all_providers)
        self.assertIn(another_provider_2, all_providers)
        self.assertIn(another_provider_3, all_providers)


class DelegateTests(unittest.TestCase):

    def test_traversal_provider(self):
        another_provider = providers.Provider()
        provider = providers.Delegate(another_provider)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 1)
        self.assertIn(another_provider, all_providers)

    def test_traversal_provider_and_overriding(self):
        provider1 = providers.Provider()
        provider2 = providers.Provider()

        provider3 = providers.Provider()
        provider3.override(provider2)

        provider = providers.Delegate(provider1)

        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)


class DependencyTests(unittest.TestCase):

    def test_traversal(self):
        provider = providers.Dependency()
        all_providers = list(provider.traverse())
        self.assertEqual(len(all_providers), 0)

    def test_traversal_default(self):
        another_provider = providers.Provider()
        provider = providers.Dependency(default=another_provider)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 1)
        self.assertIn(another_provider, all_providers)

    def test_traversal_overriding(self):
        provider1 = providers.Provider()

        provider2 = providers.Provider()
        provider2.override(provider1)

        provider = providers.Dependency()
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)


class DependenciesContainerTests(unittest.TestCase):

    def test_traversal(self):
        provider = providers.DependenciesContainer()
        all_providers = list(provider.traverse())
        self.assertEqual(len(all_providers), 0)

    def test_traversal_default(self):
        another_provider = providers.Provider()
        provider = providers.DependenciesContainer(default=another_provider)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 1)
        self.assertIn(another_provider, all_providers)

    def test_traversal_fluent_interface(self):
        provider = providers.DependenciesContainer()
        provider1 = provider.provider1
        provider2 = provider.provider2

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traversal_overriding(self):
        provider1 = providers.Provider()
        provider2 = providers.Provider()
        provider3 = providers.DependenciesContainer(
            provider1=provider1,
            provider2=provider2,
        )

        provider = providers.DependenciesContainer()
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 5)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)
        self.assertIn(provider.provider1, all_providers)
        self.assertIn(provider.provider2, all_providers)


class CallableTests(unittest.TestCase):

    def test_traverse(self):
        provider = providers.Callable(dict)
        all_providers = list(provider.traverse())
        self.assertEqual(len(all_providers), 0)

    def test_traverse_args(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Callable(list, 'foo', provider1, provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_kwargs(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Callable(dict, foo='foo', bar=provider1, baz=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')

        provider = providers.Callable(dict, 'foo')
        provider.override(provider1)
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_provides(self):
        provider1 = providers.Callable(list)
        provider2 = providers.Object('bar')
        provider3 = providers.Object('baz')

        provider = providers.Callable(provider1, provider2)
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)


class ConfigurationTests(unittest.TestCase):

    def test_traverse(self):
        config = providers.Configuration(default={'option1': {'option2': 'option2'}})
        option1 = config.option1
        option2 = config.option1.option2
        option3 = config.option1[config.option1.option2]

        all_providers = list(config.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(option1, all_providers)
        self.assertIn(option2, all_providers)
        self.assertIn(option3, all_providers)

    def test_traverse_typed(self):
        config = providers.Configuration()
        option = config.option
        typed_option = config.option.as_int()

        all_providers = list(typed_option.traverse())

        self.assertEqual(len(all_providers), 1)
        self.assertIn(option, all_providers)

    def test_traverse_overridden(self):
        options = {'option1': {'option2': 'option2'}}
        config = providers.Configuration()
        config.from_dict(options)

        all_providers = list(config.traverse())

        self.assertEqual(len(all_providers), 1)
        overridden, = all_providers
        self.assertEqual(overridden(), options)
        self.assertIs(overridden, config.last_overriding)

    def test_traverse_overridden_option_1(self):
        options = {'option2': 'option2'}
        config = providers.Configuration()
        config.option1.from_dict(options)

        all_providers = list(config.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(config.option1, all_providers)
        self.assertIn(config.last_overriding, all_providers)

    def test_traverse_overridden_option_2(self):
        options = {'option2': 'option2'}
        config = providers.Configuration()
        config.option1.from_dict(options)

        all_providers = list(config.option1.traverse())

        self.assertEqual(len(all_providers), 0)


class FactoryTests(unittest.TestCase):

    def test_traverse(self):
        provider = providers.Factory(dict)
        all_providers = list(provider.traverse())
        self.assertEqual(len(all_providers), 0)

    def test_traverse_args(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Factory(list, 'foo', provider1, provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_kwargs(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Factory(dict, foo='foo', bar=provider1, baz=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_attributes(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Factory(dict)
        provider.add_attributes(foo='foo', bar=provider1, baz=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')

        provider = providers.Factory(dict, 'foo')
        provider.override(provider1)
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_provides(self):
        provider1 = providers.Callable(list)
        provider2 = providers.Object('bar')
        provider3 = providers.Object('baz')

        provider = providers.Factory(provider1, provider2)
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)


class FactoryAggregateTests(unittest.TestCase):

    def test_traverse(self):
        factory1 = providers.Factory(dict)
        factory2 = providers.Factory(list)
        provider = providers.FactoryAggregate(factory1=factory1, factory2=factory2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(factory1, all_providers)
        self.assertIn(factory2, all_providers)


class BaseSingletonTests(unittest.TestCase):

    def test_traverse(self):
        provider = providers.Singleton(dict)
        all_providers = list(provider.traverse())
        self.assertEqual(len(all_providers), 0)

    def test_traverse_args(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Singleton(list, 'foo', provider1, provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_kwargs(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Singleton(dict, foo='foo', bar=provider1, baz=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_attributes(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Singleton(dict)
        provider.add_attributes(foo='foo', bar=provider1, baz=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')

        provider = providers.Singleton(dict, 'foo')
        provider.override(provider1)
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_provides(self):
        provider1 = providers.Callable(list)
        provider2 = providers.Object('bar')
        provider3 = providers.Object('baz')

        provider = providers.Singleton(provider1, provider2)
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)


class ListTests(unittest.TestCase):

    def test_traverse_args(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.List('foo', provider1, provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider3 = providers.List(provider1, provider2)

        provider = providers.List('foo')
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)


class DictTests(unittest.TestCase):

    def test_traverse_kwargs(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Dict(foo='foo', bar=provider1, baz=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider3 = providers.Dict(bar=provider1, baz=provider2)

        provider = providers.Dict(foo='foo')
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)


class ResourceTests(unittest.TestCase):

    def test_traverse(self):
        provider = providers.Resource(dict)
        all_providers = list(provider.traverse())
        self.assertEqual(len(all_providers), 0)

    def test_traverse_args(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Resource(list, 'foo', provider1, provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_kwargs(self):
        provider1 = providers.Object('bar')
        provider2 = providers.Object('baz')
        provider = providers.Resource(dict, foo='foo', bar=provider1, baz=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Resource(list)
        provider2 = providers.Resource(tuple)

        provider = providers.Resource(dict, 'foo')
        provider.override(provider1)
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_provides(self):
        provider1 = providers.Callable(list)

        provider = providers.Resource(provider1)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 1)
        self.assertIn(provider1, all_providers)


class ContainerTests(unittest.TestCase):

    def test_traverse(self):
        class Container(containers.DeclarativeContainer):
            provider1 = providers.Callable(list)
            provider2 = providers.Callable(dict)

        provider = providers.Container(Container)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertEqual(
            {provider.provides for provider in all_providers},
            {list,  dict},
        )

    def test_traverse_overridden(self):
        class Container1(containers.DeclarativeContainer):
            provider1 = providers.Callable(list)
            provider2 = providers.Callable(dict)

        class Container2(containers.DeclarativeContainer):
            provider1 = providers.Callable(tuple)
            provider2 = providers.Callable(str)

        container2 = Container2()

        provider = providers.Container(Container1)
        provider.override(container2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 5)
        self.assertEqual(
            {
                provider.provides
                for provider in all_providers
                if isinstance(provider, providers.Callable)
            },
            {list, dict, tuple, str},
        )
        self.assertIn(provider.last_overriding, all_providers)
        self.assertIs(provider.last_overriding(), container2)


class SelectorTests(unittest.TestCase):

    def test_traverse(self):
        switch = lambda: 'provider1'
        provider1 = providers.Callable(list)
        provider2 = providers.Callable(dict)

        provider = providers.Selector(
            switch,
            provider1=provider1,
            provider2=provider2,
        )

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_switch(self):
        switch = providers.Callable(lambda: 'provider1')
        provider1 = providers.Callable(list)
        provider2 = providers.Callable(dict)

        provider = providers.Selector(
            switch,
            provider1=provider1,
            provider2=provider2,
        )

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(switch, all_providers)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Callable(list)
        provider2 = providers.Callable(dict)
        selector1 = providers.Selector(lambda: 'provider1', provider1=provider1)

        provider = providers.Selector(
            lambda: 'provider2',
            provider2=provider2,
        )
        provider.override(selector1)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(selector1, all_providers)


class ProvidedInstanceTests(unittest.TestCase):

    def test_traverse(self):
        provider1 = providers.Provider()
        provider = provider1.provided

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 1)
        self.assertIn(provider1, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Provider()
        provider2 = providers.Provider()

        provider = provider1.provided
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)


class AttributeGetterTests(unittest.TestCase):

    def test_traverse(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        provider = provided.attr

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provided, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        provider2 = providers.Provider()

        provider = provided.attr
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provided, all_providers)


class ItemGetterTests(unittest.TestCase):

    def test_traverse(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        provider = provided['item']

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 2)
        self.assertIn(provider1, all_providers)
        self.assertIn(provided, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        provider2 = providers.Provider()

        provider = provided['item']
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provided, all_providers)


class MethodCallerTests(unittest.TestCase):

    def test_traverse(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        method = provided.method
        provider = method.call()

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provided, all_providers)
        self.assertIn(method, all_providers)

    def test_traverse_args(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        method = provided.method
        provider2 = providers.Provider()
        provider = method.call('foo', provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 4)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provided, all_providers)
        self.assertIn(method, all_providers)

    def test_traverse_kwargs(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        method = provided.method
        provider2 = providers.Provider()
        provider = method.call(foo='foo', bar=provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 4)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provided, all_providers)
        self.assertIn(method, all_providers)

    def test_traverse_overridden(self):
        provider1 = providers.Provider()
        provided = provider1.provided
        method = provided.method
        provider2 = providers.Provider()

        provider = method.call()
        provider.override(provider2)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 4)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provided, all_providers)
        self.assertIn(method, all_providers)
