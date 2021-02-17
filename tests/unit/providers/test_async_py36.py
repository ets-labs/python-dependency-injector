import asyncio
import random
import unittest

from dependency_injector import containers, providers, errors

# Runtime import to get asyncutils module
import os
_TOP_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../',
    )),
)
import sys
sys.path.append(_TOP_DIR)

from asyncutils import AsyncTestCase


RESOURCE1 = object()
RESOURCE2 = object()


async def init_resource(resource):
    await asyncio.sleep(random.randint(1, 10) / 1000)
    yield resource
    await asyncio.sleep(random.randint(1, 10) / 1000)


class Client:
    def __init__(self, resource1: object, resource2: object) -> None:
        self.resource1 = resource1
        self.resource2 = resource2


class Service:
    def __init__(self, client: Client) -> None:
        self.client = client


class Container(containers.DeclarativeContainer):
    resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))
    resource2 = providers.Resource(init_resource, providers.Object(RESOURCE2))

    client = providers.Factory(
        Client,
        resource1=resource1,
        resource2=resource2,
    )

    service = providers.Factory(
        Service,
        client=client,
    )


class FactoryTests(AsyncTestCase):

    def test_args_injection(self):
        class ContainerWithArgs(containers.DeclarativeContainer):
            resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))
            resource2 = providers.Resource(init_resource, providers.Object(RESOURCE2))

            client = providers.Factory(
                Client,
                resource1,
                resource2,
            )

            service = providers.Factory(
                Service,
                client,
            )

        container = ContainerWithArgs()

        client1 = self._run(container.client())
        client2 = self._run(container.client())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

        service1 = self._run(container.service())
        service2 = self._run(container.service())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIsNot(service1.client, service2.client)

    def test_kwargs_injection(self):
        container = Container()

        client1 = self._run(container.client())
        client2 = self._run(container.client())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

        service1 = self._run(container.service())
        service2 = self._run(container.service())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIsNot(service1.client, service2.client)

    def test_context_kwargs_injection(self):
        resource2_extra = object()

        container = Container()

        client1 = self._run(container.client(resource2=resource2_extra))
        client2 = self._run(container.client(resource2=resource2_extra))

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, resource2_extra)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, resource2_extra)

    def test_args_kwargs_injection(self):
        class ContainerWithArgsAndKwArgs(containers.DeclarativeContainer):
            resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))
            resource2 = providers.Resource(init_resource, providers.Object(RESOURCE2))

            client = providers.Factory(
                Client,
                resource1,
                resource2=resource2,
            )

            service = providers.Factory(
                Service,
                client=client,
            )

        container = ContainerWithArgsAndKwArgs()

        client1 = self._run(container.client())
        client2 = self._run(container.client())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

        service1 = self._run(container.service())
        service2 = self._run(container.service())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIsNot(service1.client, service2.client)

    def test_injection_error(self):
        async def init_resource():
            raise Exception('Something went wrong')

        class Container(containers.DeclarativeContainer):
            resource_with_error = providers.Resource(init_resource)

            client = providers.Factory(
                Client,
                resource1=resource_with_error,
                resource2=None,
            )

        container = Container()

        with self.assertRaises(Exception) as context:
            self._run(container.client())
        self.assertEqual(str(context.exception), 'Something went wrong')

    def test_injection_runtime_error_async_provides(self):
        async def create_client(*args,  **kwargs):
            raise Exception('Something went wrong')

        class Container(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource, providers.Object(RESOURCE1))

            client = providers.Factory(
                create_client,
                resource1=resource,
                resource2=None,
            )

        container = Container()

        with self.assertRaises(Exception) as context:
            self._run(container.client())
        self.assertEqual(str(context.exception), 'Something went wrong')

    def test_injection_call_error_async_provides(self):
        async def create_client():  # <-- no args defined
            ...

        class Container(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource, providers.Object(RESOURCE1))

            client = providers.Factory(
                create_client,
                resource1=resource,
                resource2=None,
            )

        container = Container()

        with self.assertRaises(TypeError) as context:
            self._run(container.client())
        self.assertIn("create_client() got", str(context.exception))
        self.assertIn("unexpected keyword argument", str(context.exception))

    def test_attributes_injection(self):
        class ContainerWithAttributes(containers.DeclarativeContainer):
            resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))
            resource2 = providers.Resource(init_resource, providers.Object(RESOURCE2))

            client = providers.Factory(
                Client,
                resource1,
                resource2=None,
            )
            client.add_attributes(resource2=resource2)

            service = providers.Factory(
                Service,
                client=None,
            )
            service.add_attributes(client=client)

        container = ContainerWithAttributes()

        client1 = self._run(container.client())
        client2 = self._run(container.client())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

        service1 = self._run(container.service())
        service2 = self._run(container.service())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIsNot(service1.client, service2.client)

    def test_attributes_injection_attribute_error(self):
        class ClientWithException(Client):
            @property
            def attribute_set_error(self):
                return None

            @attribute_set_error.setter
            def attribute_set_error(self, value):
                raise Exception('Something went wrong')

        class Container(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource, providers.Object(RESOURCE1))

            client = providers.Factory(
                ClientWithException,
                resource1=resource,
                resource2=resource,
            )
            client.add_attributes(attribute_set_error=123)

        container = Container()

        with self.assertRaises(Exception) as context:
            self._run(container.client())
        self.assertEqual(str(context.exception), 'Something went wrong')

    def test_attributes_injection_runtime_error(self):
        async def init_resource():
            raise Exception('Something went wrong')

        class Container(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource)

            client = providers.Factory(
                Client,
                resource1=None,
                resource2=None,
            )
            client.add_attributes(resource1=resource)
            client.add_attributes(resource2=resource)

        container = Container()

        with self.assertRaises(Exception) as context:
            self._run(container.client())
        self.assertEqual(str(context.exception), 'Something went wrong')

    def test_async_instance_and_sync_attributes_injection(self):
        class ContainerWithAttributes(containers.DeclarativeContainer):
            resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))

            client = providers.Factory(
                Client,
                resource1,
                resource2=None,
            )
            client.add_attributes(resource2=providers.Object(RESOURCE2))

            service = providers.Factory(
                Service,
                client=None,
            )
            service.add_attributes(client=client)

        container = ContainerWithAttributes()

        client1 = self._run(container.client())
        client2 = self._run(container.client())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

        service1 = self._run(container.service())
        service2 = self._run(container.service())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIsNot(service1.client, service2.client)


class FactoryAggregateTests(AsyncTestCase):

    def test_async_mode(self):
        object1 = object()
        object2 = object()

        async def _get_object1():
            return object1

        def _get_object2():
            return object2

        provider = providers.FactoryAggregate(
            object1=providers.Factory(_get_object1),
            object2=providers.Factory(_get_object2),
        )

        self.assertTrue(provider.is_async_mode_undefined())

        created_object1 = self._run(provider('object1'))
        self.assertIs(created_object1, object1)
        self.assertTrue(provider.is_async_mode_enabled())

        created_object2 = self._run(provider('object2'))
        self.assertIs(created_object2, object2)


class SingletonTests(AsyncTestCase):

    def test_injections(self):
        class ContainerWithSingletons(containers.DeclarativeContainer):
            resource1 = providers.Resource(init_resource, providers.Object(RESOURCE1))
            resource2 = providers.Resource(init_resource, providers.Object(RESOURCE2))

            client = providers.Singleton(
                Client,
                resource1=resource1,
                resource2=resource2,
            )

            service = providers.Singleton(
                Service,
                client=client,
            )

        container = ContainerWithSingletons()

        client1 = self._run(container.client())
        client2 = self._run(container.client())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

        service1 = self._run(container.service())
        service2 = self._run(container.service())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIs(service1, service2)
        self.assertIs(service1.client, service2.client)
        self.assertIs(service1.client, client1)

        self.assertIs(service2.client, client2)
        self.assertIs(client1, client2)

    def test_async_mode(self):
        instance = object()

        async def create_instance():
            return instance

        provider = providers.Singleton(create_instance)

        instance1 = self._run(provider())
        instance2 = self._run(provider())

        self.assertIs(instance1, instance2)
        self.assertIs(instance, instance)

    def test_async_init_with_error(self):
        # Disable default exception handling to prevent output
        asyncio.get_event_loop().set_exception_handler(lambda loop, context: ...)

        async def create_instance():
            create_instance.counter += 1
            raise RuntimeError()

        create_instance.counter = 0

        provider = providers.Singleton(create_instance)


        future = provider()
        self.assertTrue(provider.is_async_mode_enabled())

        with self.assertRaises(RuntimeError):
            self._run(future)

        self.assertEqual(create_instance.counter, 1)
        self.assertTrue(provider.is_async_mode_enabled())

        with self.assertRaises(RuntimeError):
            self._run(provider())

        self.assertEqual(create_instance.counter, 2)
        self.assertTrue(provider.is_async_mode_enabled())

        # Restore default exception handling
        asyncio.get_event_loop().set_exception_handler(None)


class DelegatedSingletonTests(AsyncTestCase):

    def test_async_mode(self):
        instance = object()

        async def create_instance():
            return instance

        provider = providers.DelegatedSingleton(create_instance)

        instance1 = self._run(provider())
        instance2 = self._run(provider())

        self.assertIs(instance1, instance2)
        self.assertIs(instance, instance)


class ThreadSafeSingletonTests(AsyncTestCase):

    def test_async_mode(self):
        instance = object()

        async def create_instance():
            return instance

        provider = providers.ThreadSafeSingleton(create_instance)

        instance1 = self._run(provider())
        instance2 = self._run(provider())

        self.assertIs(instance1, instance2)
        self.assertIs(instance, instance)


class DelegatedThreadSafeSingletonTests(AsyncTestCase):

    def test_async_mode(self):
        instance = object()

        async def create_instance():
            return instance

        provider = providers.DelegatedThreadSafeSingleton(create_instance)

        instance1 = self._run(provider())
        instance2 = self._run(provider())

        self.assertIs(instance1, instance2)
        self.assertIs(instance, instance)


class ThreadLocalSingletonTests(AsyncTestCase):

    def test_async_mode(self):
        instance = object()

        async def create_instance():
            return instance

        provider = providers.ThreadLocalSingleton(create_instance)

        instance1 = self._run(provider())
        instance2 = self._run(provider())

        self.assertIs(instance1, instance2)
        self.assertIs(instance, instance)


    def test_async_init_with_error(self):
        # Disable default exception handling to prevent output
        asyncio.get_event_loop().set_exception_handler(lambda loop, context: ...)

        async def create_instance():
            create_instance.counter += 1
            raise RuntimeError()
        create_instance.counter = 0

        provider = providers.ThreadLocalSingleton(create_instance)

        future = provider()
        self.assertTrue(provider.is_async_mode_enabled())

        with self.assertRaises(RuntimeError):
            self._run(future)

        self.assertEqual(create_instance.counter, 1)
        self.assertTrue(provider.is_async_mode_enabled())

        with self.assertRaises(RuntimeError):
            self._run(provider())

        self.assertEqual(create_instance.counter, 2)
        self.assertTrue(provider.is_async_mode_enabled())

        # Restore default exception handling
        asyncio.get_event_loop().set_exception_handler(None)


class DelegatedThreadLocalSingletonTests(AsyncTestCase):

    def test_async_mode(self):
        instance = object()

        async def create_instance():
            return instance

        provider = providers.DelegatedThreadLocalSingleton(create_instance)

        instance1 = self._run(provider())
        instance2 = self._run(provider())

        self.assertIs(instance1, instance2)
        self.assertIs(instance, instance)


class ProvidedInstanceTests(AsyncTestCase):

    def test_provided_attribute(self):
        class TestClient:
            def __init__(self, resource):
                self.resource = resource

        class TestService:
            def __init__(self, resource):
                self.resource = resource

        class TestContainer(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
            client = providers.Factory(TestClient, resource=resource)
            service = providers.Factory(TestService, resource=client.provided.resource)

        container = TestContainer()

        instance1, instance2 = self._run(
            asyncio.gather(
                container.service(),
                container.service(),
            ),
        )

        self.assertIs(instance1.resource, RESOURCE1)
        self.assertIs(instance2.resource, RESOURCE1)
        self.assertIs(instance1.resource, instance2.resource)

    def test_provided_item(self):
        class TestClient:
            def __init__(self, resource):
                self.resource = resource

            def __getitem__(self, item):
                return getattr(self, item)

        class TestService:
            def __init__(self, resource):
                self.resource = resource

        class TestContainer(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
            client = providers.Factory(TestClient, resource=resource)
            service = providers.Factory(TestService, resource=client.provided['resource'])

        container = TestContainer()

        instance1, instance2 = self._run(
            asyncio.gather(
                container.service(),
                container.service(),
            ),
        )

        self.assertIs(instance1.resource, RESOURCE1)
        self.assertIs(instance2.resource, RESOURCE1)
        self.assertIs(instance1.resource, instance2.resource)

    def test_provided_method_call(self):
        class TestClient:
            def __init__(self, resource):
                self.resource = resource

            def get_resource(self):
                return self.resource

        class TestService:
            def __init__(self, resource):
                self.resource = resource

        class TestContainer(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
            client = providers.Factory(TestClient, resource=resource)
            service = providers.Factory(TestService, resource=client.provided.get_resource.call())

        container = TestContainer()

        instance1, instance2 = self._run(
            asyncio.gather(
                container.service(),
                container.service(),
            ),
        )

        self.assertIs(instance1.resource, RESOURCE1)
        self.assertIs(instance2.resource, RESOURCE1)
        self.assertIs(instance1.resource, instance2.resource)


class DependencyTests(AsyncTestCase):

    def test_isinstance(self):
        dependency = 1.0

        async def get_async():
            return dependency

        provider = providers.Dependency(instance_of=float)
        provider.override(providers.Callable(get_async))

        self.assertTrue(provider.is_async_mode_undefined())

        dependency1 = self._run(provider())

        self.assertTrue(provider.is_async_mode_enabled())

        dependency2 = self._run(provider())

        self.assertEqual(dependency1, dependency)
        self.assertEqual(dependency2, dependency)

    def test_isinstance_invalid(self):
        async def get_async():
            return {}

        provider = providers.Dependency(instance_of=float)
        provider.override(providers.Callable(get_async))

        self.assertTrue(provider.is_async_mode_undefined())

        with self.assertRaises(errors.Error):
            self._run(provider())

        self.assertTrue(provider.is_async_mode_enabled())

    def test_async_mode(self):
        dependency = 123

        async def get_async():
            return dependency

        def get_sync():
            return dependency

        provider = providers.Dependency(instance_of=int)
        provider.override(providers.Factory(get_async))

        self.assertTrue(provider.is_async_mode_undefined())

        dependency1 = self._run(provider())

        self.assertTrue(provider.is_async_mode_enabled())

        dependency2 = self._run(provider())
        self.assertEqual(dependency1, dependency)
        self.assertEqual(dependency2, dependency)

        provider.override(providers.Factory(get_sync))

        dependency3 = self._run(provider())

        self.assertTrue(provider.is_async_mode_enabled())

        dependency4 = self._run(provider())
        self.assertEqual(dependency3, dependency)
        self.assertEqual(dependency4, dependency)


class OverrideTests(AsyncTestCase):

    def test_provider(self):
        dependency = object()

        async def _get_dependency_async():
            return dependency

        def _get_dependency_sync():
            return dependency

        provider = providers.Provider()

        provider.override(providers.Callable(_get_dependency_async))
        dependency1 = self._run(provider())

        provider.override(providers.Callable(_get_dependency_sync))
        dependency2 = self._run(provider())

        self.assertIs(dependency1, dependency)
        self.assertIs(dependency2, dependency)

    def test_callable(self):
        dependency = object()

        async def _get_dependency_async():
            return dependency

        def _get_dependency_sync():
            return dependency

        provider = providers.Callable(_get_dependency_async)
        dependency1 = self._run(provider())

        provider.override(providers.Callable(_get_dependency_sync))
        dependency2 = self._run(provider())

        self.assertIs(dependency1, dependency)
        self.assertIs(dependency2, dependency)

    def test_factory(self):
        dependency = object()

        async def _get_dependency_async():
            return dependency

        def _get_dependency_sync():
            return dependency

        provider = providers.Factory(_get_dependency_async)
        dependency1 = self._run(provider())

        provider.override(providers.Callable(_get_dependency_sync))
        dependency2 = self._run(provider())

        self.assertIs(dependency1, dependency)
        self.assertIs(dependency2, dependency)

    def test_async_mode_enabling(self):
        dependency = object()

        async def _get_dependency_async():
            return dependency

        provider = providers.Callable(_get_dependency_async)
        self.assertTrue(provider.is_async_mode_undefined())

        self._run(provider())

        self.assertTrue(provider.is_async_mode_enabled())

    def test_async_mode_disabling(self):
        dependency = object()

        def _get_dependency():
            return dependency

        provider = providers.Callable(_get_dependency)
        self.assertTrue(provider.is_async_mode_undefined())

        provider()

        self.assertTrue(provider.is_async_mode_disabled())

    def test_async_mode_enabling_on_overriding(self):
        dependency = object()

        async def _get_dependency_async():
            return dependency

        provider = providers.Provider()
        provider.override(providers.Callable(_get_dependency_async))
        self.assertTrue(provider.is_async_mode_undefined())

        self._run(provider())

        self.assertTrue(provider.is_async_mode_enabled())

    def test_async_mode_disabling_on_overriding(self):
        dependency = object()

        def _get_dependency():
            return dependency

        provider = providers.Provider()
        provider.override(providers.Callable(_get_dependency))
        self.assertTrue(provider.is_async_mode_undefined())

        provider()

        self.assertTrue(provider.is_async_mode_disabled())


class TestAsyncModeApi(unittest.TestCase):

    def setUp(self):
        self.provider = providers.Provider()

    def test_default_mode(self):
        self.assertFalse(self.provider.is_async_mode_enabled())
        self.assertFalse(self.provider.is_async_mode_disabled())
        self.assertTrue(self.provider.is_async_mode_undefined())

    def test_enable(self):
        self.provider.enable_async_mode()

        self.assertTrue(self.provider.is_async_mode_enabled())
        self.assertFalse(self.provider.is_async_mode_disabled())
        self.assertFalse(self.provider.is_async_mode_undefined())

    def test_disable(self):
        self.provider.disable_async_mode()

        self.assertFalse(self.provider.is_async_mode_enabled())
        self.assertTrue(self.provider.is_async_mode_disabled())
        self.assertFalse(self.provider.is_async_mode_undefined())

    def test_reset(self):
        self.provider.enable_async_mode()

        self.assertTrue(self.provider.is_async_mode_enabled())
        self.assertFalse(self.provider.is_async_mode_disabled())
        self.assertFalse(self.provider.is_async_mode_undefined())

        self.provider.reset_async_mode()

        self.assertFalse(self.provider.is_async_mode_enabled())
        self.assertFalse(self.provider.is_async_mode_disabled())
        self.assertTrue(self.provider.is_async_mode_undefined())


class AsyncTypingStubTests(AsyncTestCase):

    def test_async_(self):
        container = Container()

        client1 = self._run(container.client.async_())
        client2 = self._run(container.client.async_())

        self.assertIsInstance(client1, Client)
        self.assertIs(client1.resource1, RESOURCE1)
        self.assertIs(client1.resource2, RESOURCE2)

        self.assertIsInstance(client2, Client)
        self.assertIs(client2.resource1, RESOURCE1)
        self.assertIs(client2.resource2, RESOURCE2)

        service1 = self._run(container.service.async_())
        service2 = self._run(container.service.async_())

        self.assertIsInstance(service1, Service)
        self.assertIsInstance(service1.client, Client)
        self.assertIs(service1.client.resource1, RESOURCE1)
        self.assertIs(service1.client.resource2, RESOURCE2)

        self.assertIsInstance(service2, Service)
        self.assertIsInstance(service2.client, Client)
        self.assertIs(service2.client.resource1, RESOURCE1)
        self.assertIs(service2.client.resource2, RESOURCE2)

        self.assertIsNot(service1.client, service2.client)


class AsyncProvidersWithAsyncDependenciesTests(AsyncTestCase):

    def test_injections(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/368
        async def async_db_provider():
            return {'db': 'ok'}

        async def async_service(db=None):
            return {'service': 'ok', 'db': db}

        class Container(containers.DeclarativeContainer):

            db = providers.Factory(async_db_provider)
            service = providers.Singleton(async_service, db=db)

        container = Container()
        service = self._run(container.service())

        self.assertEquals(service, {'service': 'ok', 'db': {'db': 'ok'}})


class AsyncProviderWithAwaitableObjectTests(AsyncTestCase):

    def test(self):
        class SomeResource:
            def __await__(self):
                raise RuntimeError('Should never happen')

        async def init_resource():
            pool = SomeResource()
            yield pool

        class Service:
            def __init__(self, resource) -> None:
                self.resource = resource

        class Container(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource)
            service = providers.Singleton(Service, resource=resource)

        container = Container()

        self._run(container.init_resources())
        self.assertIsInstance(container.service(), asyncio.Future)
        self.assertIsInstance(container.resource(), asyncio.Future)

        resource = self._run(container.resource())
        service = self._run(container.service())

        self.assertIsInstance(resource, SomeResource)
        self.assertIsInstance(service.resource, SomeResource)
        self.assertIs(service.resource, resource)

    def test_without_init_resources(self):
        class SomeResource:
            def __await__(self):
                raise RuntimeError('Should never happen')

        async def init_resource():
            pool = SomeResource()
            yield pool

        class Service:
            def __init__(self, resource) -> None:
                self.resource = resource

        class Container(containers.DeclarativeContainer):
            resource = providers.Resource(init_resource)
            service = providers.Singleton(Service, resource=resource)

        container = Container()

        self.assertIsInstance(container.service(), asyncio.Future)
        self.assertIsInstance(container.resource(), asyncio.Future)

        resource = self._run(container.resource())
        service = self._run(container.service())

        self.assertIsInstance(resource, SomeResource)
        self.assertIsInstance(service.resource, SomeResource)
        self.assertIs(service.resource, resource)
