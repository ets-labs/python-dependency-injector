import unittest

from dependency_injector import providers


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

    def test_traversal_overriding_cycled(self):
        provider1 = providers.Provider()

        provider2 = providers.Provider()
        provider2.override(provider1)

        provider3 = providers.Provider()
        provider3.override(provider2)

        provider1.override(provider3)  # Cycle: provider3 -> provider2 -> provider1 -> provider3

        provider = providers.Provider()
        provider.override(provider3)

        all_providers = list(provider.traverse())

        self.assertEqual(len(all_providers), 3)
        self.assertIn(provider1, all_providers)
        self.assertIn(provider2, all_providers)
        self.assertIn(provider3, all_providers)


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

