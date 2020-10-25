"""Dependency injector resource provider unit tests."""

import sys

import unittest2 as unittest

from dependency_injector import containers, providers, resources, errors


def init_fn(*args, **kwargs):
    return args, kwargs


class ResourceTests(unittest.TestCase):

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.Resource(init_fn)))

    def test_provided_instance_provider(self):
        provider = providers.Resource(init_fn)
        self.assertIsInstance(provider.provided, providers.ProvidedInstance)

    def test_injection(self):
        resource = object()

        def _init():
            _init.counter += 1
            return resource
        _init.counter = 0

        class Container(containers.DeclarativeContainer):
            resource = providers.Resource(_init)
            dependency1 = providers.List(resource)
            dependency2 = providers.List(resource)

        container = Container()
        list1 = container.dependency1()
        list2 = container.dependency2()

        self.assertEqual(list1, [resource])
        self.assertIs(list1[0], resource)

        self.assertEqual(list2, [resource])
        self.assertIs(list2[0], resource)

        self.assertEqual(_init.counter, 1)

    def test_init_function(self):
        def _init():
            _init.counter += 1
        _init.counter = 0

        provider = providers.Resource(_init)

        result1 = provider()
        self.assertIsNone(result1)
        self.assertEqual(_init.counter, 1)

        result2 = provider()
        self.assertIsNone(result2)
        self.assertEqual(_init.counter, 1)

        provider.shutdown()

    def test_init_generator(self):
        def _init():
            _init.init_counter += 1
            yield
            _init.shutdown_counter += 1

        _init.init_counter = 0
        _init.shutdown_counter = 0

        provider = providers.Resource(_init)

        result1 = provider()
        self.assertIsNone(result1)
        self.assertEqual(_init.init_counter, 1)
        self.assertEqual(_init.shutdown_counter, 0)

        provider.shutdown()
        self.assertEqual(_init.init_counter, 1)
        self.assertEqual(_init.shutdown_counter, 1)

        result2 = provider()
        self.assertIsNone(result2)
        self.assertEqual(_init.init_counter, 2)
        self.assertEqual(_init.shutdown_counter, 1)

        provider.shutdown()
        self.assertEqual(_init.init_counter, 2)
        self.assertEqual(_init.shutdown_counter, 2)

    def test_init_class(self):
        class TestResource(resources.Resource):
            init_counter = 0
            shutdown_counter = 0

            def init(self):
                self.__class__.init_counter += 1

            def shutdown(self, _):
                self.__class__.shutdown_counter += 1

        provider = providers.Resource(TestResource)

        result1 = provider()
        self.assertIsNone(result1)
        self.assertEqual(TestResource.init_counter, 1)
        self.assertEqual(TestResource.shutdown_counter, 0)

        provider.shutdown()
        self.assertEqual(TestResource.init_counter, 1)
        self.assertEqual(TestResource.shutdown_counter, 1)

        result2 = provider()
        self.assertIsNone(result2)
        self.assertEqual(TestResource.init_counter, 2)
        self.assertEqual(TestResource.shutdown_counter, 1)

        provider.shutdown()
        self.assertEqual(TestResource.init_counter, 2)
        self.assertEqual(TestResource.shutdown_counter, 2)

    def test_init_not_callable(self):
        provider = providers.Resource(1)
        with self.assertRaises(errors.Error):
            provider.init()

    def test_init_and_shutdown(self):
        def _init():
            _init.init_counter += 1
            yield
            _init.shutdown_counter += 1

        _init.init_counter = 0
        _init.shutdown_counter = 0

        provider = providers.Resource(_init)

        result1 = provider.init()
        self.assertIsNone(result1)
        self.assertEqual(_init.init_counter, 1)
        self.assertEqual(_init.shutdown_counter, 0)

        provider.shutdown()
        self.assertEqual(_init.init_counter, 1)
        self.assertEqual(_init.shutdown_counter, 1)

        result2 = provider.init()
        self.assertIsNone(result2)
        self.assertEqual(_init.init_counter, 2)
        self.assertEqual(_init.shutdown_counter, 1)

        provider.shutdown()
        self.assertEqual(_init.init_counter, 2)
        self.assertEqual(_init.shutdown_counter, 2)

    def test_initialized(self):
        provider = providers.Resource(init_fn)
        self.assertFalse(provider.initialized)

        provider.init()
        self.assertTrue(provider.initialized)

        provider.shutdown()
        self.assertFalse(provider.initialized)

    def test_call_with_context_args(self):
        provider = providers.Resource(init_fn, 'i1', 'i2')
        self.assertEqual(provider('i3', i4=4), (('i1', 'i2', 'i3'), {'i4': 4}))

    def test_fluent_interface(self):
        provider = providers.Resource(init_fn) \
            .add_args(1, 2) \
            .add_kwargs(a3=3, a4=4)

        self.assertEqual(provider(), ((1, 2), {'a3': 3, 'a4': 4}))

    def test_set_args(self):
        provider = providers.Resource(init_fn) \
            .add_args(1, 2) \
            .set_args(3, 4)
        self.assertEqual(provider.args, tuple([3, 4]))

    def test_clear_args(self):
        provider = providers.Resource(init_fn) \
            .add_args(1, 2) \
            .clear_args()
        self.assertEqual(provider.args, tuple())

    def test_set_kwargs(self):
        provider = providers.Resource(init_fn) \
            .add_kwargs(a1='i1', a2='i2') \
            .set_kwargs(a3='i3', a4='i4')
        self.assertEqual(provider.kwargs, {'a3': 'i3', 'a4': 'i4'})

    def test_clear_kwargs(self):
        provider = providers.Resource(init_fn) \
            .add_kwargs(a1='i1', a2='i2') \
            .clear_kwargs()
        self.assertEqual(provider.kwargs, {})

    def test_call_overridden(self):
        provider = providers.Resource(init_fn, 1)
        overriding_provider1 = providers.Resource(init_fn, 2)
        overriding_provider2 = providers.Resource(init_fn, 3)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIs(instance1, instance2)
        self.assertEqual(instance1, ((3,), {}))
        self.assertEqual(instance2, ((3,), {}))

    def test_deepcopy(self):
        provider = providers.Resource(init_fn, 1, 2, a3=3, a4=4)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertEqual(provider.args, provider_copy.args)
        self.assertEqual(provider.kwargs, provider_copy.kwargs)
        self.assertIsInstance(provider, providers.Resource)

    def test_deepcopy_initialized(self):
        provider = providers.Resource(init_fn)
        provider.init()

        with self.assertRaises(errors.Error):
            providers.deepcopy(provider)

    def test_deepcopy_from_memo(self):
        provider = providers.Resource(init_fn)
        provider_copy_memo = providers.Resource(init_fn)

        provider_copy = providers.deepcopy(
            provider,
            memo={id(provider): provider_copy_memo},
        )

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_args(self):
        provider = providers.Resource(init_fn)
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

    def test_deepcopy_kwargs(self):
        provider = providers.Resource(init_fn)
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

    def test_deepcopy_overridden(self):
        provider = providers.Resource(init_fn)
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertEqual(provider.args, provider_copy.args)
        self.assertIsInstance(provider, providers.Resource)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_deepcopy_with_sys_streams(self):
        provider = providers.Resource(init_fn)
        provider.add_args(sys.stdin, sys.stdout, sys.stderr)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider_copy, providers.Resource)
        self.assertIs(provider.args[0], sys.stdin)
        self.assertIs(provider.args[1], sys.stdout)
        self.assertIs(provider.args[2], sys.stderr)

    def test_repr(self):
        provider = providers.Resource(init_fn)

        self.assertEqual(
            repr(provider),
            'Resource({0}, initialized={1})'.format(
                init_fn,
                provider.initialized,
            )
        )
