"""Dependency injector list provider unit tests."""

import sys

import unittest2 as unittest

from dependency_injector import providers


class ListTests(unittest.TestCase):

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.List()))

    def test_provided_instance_provider(self):
        provider = providers.List()
        self.assertIsInstance(provider.provided, providers.ProvidedInstance)

    def test_call_with_init_positional_args(self):
        provider = providers.List('i1', 'i2')

        list1 = provider()
        list2 = provider()

        self.assertEqual(list1, ['i1', 'i2'])
        self.assertEqual(list2, ['i1', 'i2'])

        self.assertIsNot(list1, list2)

    def test_call_with_context_args(self):
        provider = providers.List('i1', 'i2')

        self.assertEqual(provider('i3', 'i4'), ['i1', 'i2', 'i3', 'i4'])

    def test_fluent_interface(self):
        provider = providers.List() \
            .add_args(1, 2)

        self.assertEqual(provider(), [1, 2])

    def test_set_args(self):
        provider = providers.List() \
            .add_args(1, 2) \
            .set_args(3, 4)
        self.assertEqual(provider.args, tuple([3, 4]))

    def test_clear_args(self):
        provider = providers.List() \
            .add_args(1, 2) \
            .clear_args()
        self.assertEqual(provider.args, tuple())

    def test_call_overridden(self):
        provider = providers.List(1, 2)
        overriding_provider1 = providers.List(2, 3)
        overriding_provider2 = providers.List(3, 4)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertEqual(instance1, [3, 4])
        self.assertEqual(instance2, [3, 4])

    def test_deepcopy(self):
        provider = providers.List(1, 2)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertEqual(provider.args, provider_copy.args)
        self.assertIsInstance(provider, providers.List)

    def test_deepcopy_from_memo(self):
        provider = providers.List(1, 2)
        provider_copy_memo = providers.List(1, 2)

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_args(self):
        provider = providers.List()
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

        provider.add_args(dependent_provider1, dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.args[0]
        dependent_provider_copy2 = provider_copy.args[1]

        self.assertNotEqual(provider.args, provider_copy.args)

        self.assertIs(dependent_provider1.cls, dependent_provider_copy1.cls)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.cls, dependent_provider_copy2.cls)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_overridden(self):
        provider = providers.List()
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertEqual(provider.args, provider_copy.args)
        self.assertIsInstance(provider, providers.List)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_deepcopy_with_sys_streams(self):
        provider = providers.List()
        provider.add_args(sys.stdin, sys.stdout, sys.stderr)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider_copy, providers.List)
        self.assertIs(provider.args[0], sys.stdin)
        self.assertIs(provider.args[1], sys.stdout)
        self.assertIs(provider.args[2], sys.stderr)

    def test_repr(self):
        provider = providers.List(1, 2)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'List({0}) at {1}>'.format(
                             repr(list(provider.args)),
                             hex(id(provider))))
