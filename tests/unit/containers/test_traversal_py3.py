import unittest

from dependency_injector import containers, providers


class TraverseProviderTests(unittest.TestCase):

    def test_nested_providers(self):
        class Container(containers.DeclarativeContainer):
            obj_factory = providers.DelegatedFactory(
                dict,
                foo=providers.Resource(
                    dict,
                    foo='bar'
                ),
                bar=providers.Resource(
                    dict,
                    foo='bar'
                )
            )

        container = Container()
        all_providers = list(container.traverse())

        self.assertIn(container.obj_factory, all_providers)
        self.assertIn(container.obj_factory.kwargs['foo'], all_providers)
        self.assertIn(container.obj_factory.kwargs['bar'], all_providers)
        self.assertEqual(len(all_providers), 3)

    def test_nested_providers_with_filtering(self):
        class Container(containers.DeclarativeContainer):
            obj_factory = providers.DelegatedFactory(
                dict,
                foo=providers.Resource(
                    dict,
                    foo='bar'
                ),
                bar=providers.Resource(
                    dict,
                    foo='bar'
                )
            )

        container = Container()
        all_providers = list(container.traverse(types=[providers.Resource]))

        self.assertIn(container.obj_factory.kwargs['foo'], all_providers)
        self.assertIn(container.obj_factory.kwargs['bar'], all_providers)
        self.assertEqual(len(all_providers), 2)


class TraverseProviderDeclarativeTests(unittest.TestCase):

    def test_nested_providers(self):
        class Container(containers.DeclarativeContainer):
            obj_factory = providers.DelegatedFactory(
                dict,
                foo=providers.Resource(
                    dict,
                    foo='bar'
                ),
                bar=providers.Resource(
                    dict,
                    foo='bar'
                )
            )

        all_providers = list(Container.traverse())

        self.assertIn(Container.obj_factory, all_providers)
        self.assertIn(Container.obj_factory.kwargs['foo'], all_providers)
        self.assertIn(Container.obj_factory.kwargs['bar'], all_providers)
        self.assertEqual(len(all_providers), 3)

    def test_nested_providers_with_filtering(self):
        class Container(containers.DeclarativeContainer):
            obj_factory = providers.DelegatedFactory(
                dict,
                foo=providers.Resource(
                    dict,
                    foo='bar'
                ),
                bar=providers.Resource(
                    dict,
                    foo='bar'
                )
            )

        all_providers = list(Container.traverse(types=[providers.Resource]))

        self.assertIn(Container.obj_factory.kwargs['foo'], all_providers)
        self.assertIn(Container.obj_factory.kwargs['bar'], all_providers)
        self.assertEqual(len(all_providers), 2)
