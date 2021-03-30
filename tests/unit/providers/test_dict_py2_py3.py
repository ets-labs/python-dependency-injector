"""Dependency injector dict provider unit tests."""

import sys

import unittest

from dependency_injector import providers


class DictTests(unittest.TestCase):

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.Dict()))

    def test_provided_instance_provider(self):
        provider = providers.Dict()
        self.assertIsInstance(provider.provided, providers.ProvidedInstance)

    def test_init_with_non_string_keys(self):
        a1 = object()
        a2 = object()
        provider = providers.Dict({a1: 'i1', a2: 'i2'})

        dict1 = provider()
        dict2 = provider()

        self.assertEqual(dict1, {a1: 'i1', a2: 'i2'})
        self.assertEqual(dict2, {a1: 'i1', a2: 'i2'})

        self.assertIsNot(dict1, dict2)

    def test_init_with_string_and_non_string_keys(self):
        a1 = object()
        provider = providers.Dict({a1: 'i1'}, a2='i2')

        dict1 = provider()
        dict2 = provider()

        self.assertEqual(dict1, {a1: 'i1', 'a2': 'i2'})
        self.assertEqual(dict2, {a1: 'i1', 'a2': 'i2'})

        self.assertIsNot(dict1, dict2)

    def test_call_with_init_keyword_args(self):
        provider = providers.Dict(a1='i1', a2='i2')

        dict1 = provider()
        dict2 = provider()

        self.assertEqual(dict1, {'a1': 'i1', 'a2': 'i2'})
        self.assertEqual(dict2, {'a1': 'i1', 'a2': 'i2'})

        self.assertIsNot(dict1, dict2)

    def test_call_with_context_keyword_args(self):
        provider = providers.Dict(a1='i1', a2='i2')
        self.assertEqual(
            provider(a3='i3', a4='i4'),
            {'a1': 'i1', 'a2': 'i2', 'a3': 'i3', 'a4': 'i4'},
        )

    def test_call_with_provider(self):
        provider = providers.Dict(
            a1=providers.Factory(str, 'i1'),
            a2=providers.Factory(str, 'i2'),
        )
        self.assertEqual(provider(), {'a1': 'i1', 'a2': 'i2'})

    def test_fluent_interface(self):
        provider = providers.Dict() \
            .add_kwargs(a1='i1', a2='i2')
        self.assertEqual(provider(), {'a1': 'i1', 'a2': 'i2'})

    def test_add_kwargs(self):
        provider = providers.Dict() \
            .add_kwargs(a1='i1') \
            .add_kwargs(a2='i2')
        self.assertEqual(provider.kwargs, {'a1': 'i1', 'a2': 'i2'})

    def test_add_kwargs_non_string_keys(self):
        a1 = object()
        a2 = object()
        provider = providers.Dict() \
            .add_kwargs({a1: 'i1'}) \
            .add_kwargs({a2: 'i2'})
        self.assertEqual(provider.kwargs, {a1: 'i1', a2: 'i2'})

    def test_add_kwargs_string_and_non_string_keys(self):
        a2 = object()
        provider = providers.Dict() \
            .add_kwargs(a1='i1') \
            .add_kwargs({a2: 'i2'})
        self.assertEqual(provider.kwargs, {'a1': 'i1', a2: 'i2'})

    def test_set_kwargs(self):
        provider = providers.Dict() \
            .add_kwargs(a1='i1', a2='i2') \
            .set_kwargs(a3='i3', a4='i4')
        self.assertEqual(provider.kwargs, {'a3': 'i3', 'a4': 'i4'})

    def test_set_kwargs_non_string_keys(self):
        a3 = object()
        a4 = object()
        provider = providers.Dict() \
            .add_kwargs(a1='i1', a2='i2') \
            .set_kwargs({a3: 'i3', a4: 'i4'})
        self.assertEqual(provider.kwargs, {a3: 'i3', a4: 'i4'})

    def test_set_kwargs_string_and_non_string_keys(self):
        a3 = object()
        provider = providers.Dict() \
            .add_kwargs(a1='i1', a2='i2') \
            .set_kwargs({a3: 'i3'}, a4='i4')
        self.assertEqual(provider.kwargs, {a3: 'i3', 'a4': 'i4'})

    def test_clear_kwargs(self):
        provider = providers.Dict() \
            .add_kwargs(a1='i1', a2='i2') \
            .clear_kwargs()
        self.assertEqual(provider.kwargs, {})

    def test_call_overridden(self):
        provider = providers.Dict(a1='i1', a2='i2')
        overriding_provider1 = providers.Dict(a2='i2', a3='i3')
        overriding_provider2 = providers.Dict(a3='i3', a4='i4')

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertEqual(instance1, {'a3': 'i3', 'a4': 'i4'})
        self.assertEqual(instance2, {'a3': 'i3', 'a4': 'i4'})

    def test_deepcopy(self):
        provider = providers.Dict(a1='i1', a2='i2')

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertEqual(provider.kwargs, provider_copy.kwargs)
        self.assertIsInstance(provider, providers.Dict)

    def test_deepcopy_from_memo(self):
        provider = providers.Dict(a1='i1', a2='i2')
        provider_copy_memo = providers.Dict(a1='i1', a2='i2')

        provider_copy = providers.deepcopy(
            provider,
            memo={id(provider): provider_copy_memo},
        )

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_kwargs(self):
        provider = providers.Dict()
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

        provider.add_kwargs(d1=dependent_provider1, d2=dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.kwargs['d1']
        dependent_provider_copy2 = provider_copy.kwargs['d2']

        self.assertNotEqual(provider.kwargs, provider_copy.kwargs)

        self.assertIs(dependent_provider1.cls, dependent_provider_copy1.cls)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.cls, dependent_provider_copy2.cls)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_kwargs_non_string_keys(self):
        a1 = object()
        a2 = object()

        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

        provider = providers.Dict({a1: dependent_provider1, a2: dependent_provider2})

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.kwargs[a1]
        dependent_provider_copy2 = provider_copy.kwargs[a2]

        self.assertNotEqual(provider.kwargs, provider_copy.kwargs)

        self.assertIs(dependent_provider1.cls, dependent_provider_copy1.cls)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.cls, dependent_provider_copy2.cls)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_overridden(self):
        provider = providers.Dict()
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertEqual(provider.kwargs, provider_copy.kwargs)
        self.assertIsInstance(provider, providers.Dict)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_deepcopy_with_sys_streams(self):
        provider = providers.Dict()
        provider.add_kwargs(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider_copy, providers.Dict)
        self.assertIs(provider.kwargs['stdin'], sys.stdin)
        self.assertIs(provider.kwargs['stdout'], sys.stdout)
        self.assertIs(provider.kwargs['stderr'], sys.stderr)

    def test_repr(self):
        provider = providers.Dict(a1=1, a2=2)
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Dict({0}) at {1}>'.format(
                             repr(provider.kwargs),
                             hex(id(provider))))
