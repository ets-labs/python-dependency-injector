"""Dependency injector selector provider unit tests."""

import functools
import itertools
import sys

import unittest

from dependency_injector import providers, errors


class SelectorTests(unittest.TestCase):

    selector = providers.Configuration()

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.Selector(self.selector)))

    def test_init_optional(self):
        one = providers.Object(1)
        two = providers.Object(2)

        provider = providers.Selector()
        provider.set_selector(self.selector)
        provider.set_providers(one=one, two=two)

        self.assertEqual(provider.providers, {'one': one, 'two': two})
        with self.selector.override('one'):
            self.assertEqual(provider(), one())
        with self.selector.override('two'):
            self.assertEqual(provider(), two())

    def test_set_selector_returns_self(self):
        provider = providers.Selector()
        self.assertIs(provider.set_selector(self.selector), provider)

    def test_set_providers_returns_self(self):
        provider = providers.Selector()
        self.assertIs(provider.set_providers(one=providers.Provider()), provider)

    def test_provided_instance_provider(self):
        provider = providers.Selector(self.selector)
        self.assertIsInstance(provider.provided, providers.ProvidedInstance)

    def test_call(self):
        provider = providers.Selector(
            self.selector,
            one=providers.Object(1),
            two=providers.Object(2),
        )

        with self.selector.override('one'):
            self.assertEqual(provider(), 1)

        with self.selector.override('two'):
            self.assertEqual(provider(), 2)

    def test_call_undefined_provider(self):
        provider = providers.Selector(
            self.selector,
            one=providers.Object(1),
            two=providers.Object(2),
        )

        with self.selector.override('three'):
            with self.assertRaises(errors.Error):
                provider()

    def test_call_selector_is_none(self):
        provider = providers.Selector(
            self.selector,
            one=providers.Object(1),
            two=providers.Object(2),
        )

        with self.selector.override(None):
            with self.assertRaises(errors.Error):
                provider()

    def test_call_any_callable(self):
        provider = providers.Selector(
            functools.partial(next, itertools.cycle(['one', 'two'])),
            one=providers.Object(1),
            two=providers.Object(2),
        )

        self.assertEqual(provider(), 1)
        self.assertEqual(provider(), 2)
        self.assertEqual(provider(), 1)
        self.assertEqual(provider(), 2)

    def test_call_with_context_args(self):
        provider = providers.Selector(
            self.selector,
            one=providers.Callable(lambda *args, **kwargs: (args, kwargs)),
        )

        with self.selector.override('one'):
            args, kwargs = provider(1, 2, three=3, four=4)

        self.assertEqual(args, (1, 2))
        self.assertEqual(kwargs, {'three': 3, 'four': 4})

    def test_getattr(self):
        provider_one = providers.Object(1)
        provider_two = providers.Object(2)

        provider = providers.Selector(
            self.selector,
            one=provider_one,
            two=provider_two,
        )

        self.assertIs(provider.one, provider_one)
        self.assertIs(provider.two, provider_two)

    def test_getattr_attribute_error(self):
        provider_one = providers.Object(1)
        provider_two = providers.Object(2)

        provider = providers.Selector(
            self.selector,
            one=provider_one,
            two=provider_two,
        )

        with self.assertRaises(AttributeError):
            _ = provider.provider_three

    def test_call_overridden(self):
        provider = providers.Selector(self.selector, sample=providers.Object(1))
        overriding_provider1 = providers.Selector(self.selector, sample=providers.Object(2))
        overriding_provider2 = providers.Selector(self.selector, sample=providers.Object(3))

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        with self.selector.override('sample'):
            self.assertEqual(provider(), 3)

    def test_providers_attribute(self):
        provider_one = providers.Object(1)
        provider_two = providers.Object(2)

        provider = providers.Selector(
            self.selector,
            one=provider_one,
            two=provider_two,
        )

        self.assertEqual(provider.providers, {'one': provider_one, 'two': provider_two})

    def test_deepcopy(self):
        provider = providers.Selector(self.selector)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Selector)

    def test_deepcopy_from_memo(self):
        provider = providers.Selector(self.selector)
        provider_copy_memo = providers.Selector(self.selector)

        provider_copy = providers.deepcopy(
            provider,
            memo={id(provider): provider_copy_memo},
        )

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Selector(self.selector)
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Selector)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_deepcopy_with_sys_streams(self):
        provider = providers.Selector(
            self.selector,
            stdin=providers.Object(sys.stdin),
            stdout=providers.Object(sys.stdout),
            stderr=providers.Object(sys.stderr),

        )

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider_copy, providers.Selector)

        with self.selector.override('stdin'):
            self.assertIs(provider(), sys.stdin)

        with self.selector.override('stdout'):
            self.assertIs(provider(), sys.stdout)

        with self.selector.override('stderr'):
            self.assertIs(provider(), sys.stderr)

    def test_repr(self):
        provider = providers.Selector(
            self.selector,
            one=providers.Object(1),
            two=providers.Object(2),
        )

        self.assertIn(
            '<dependency_injector.providers.Selector({0}'.format(repr(self.selector)),
            repr(provider),
        )
        self.assertIn('one={0}'.format(repr(provider.one)), repr(provider))
        self.assertIn('two={0}'.format(repr(provider.two)), repr(provider))
        self.assertIn('at {0}'.format(hex(id(provider))), repr(provider))
