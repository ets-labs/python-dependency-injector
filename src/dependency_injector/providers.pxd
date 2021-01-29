"""Providers module."""

try:
    import asyncio
except ImportError:
    asyncio = None

import functools
import inspect

cimport cython


# Base providers
cdef class Provider(object):
    cdef tuple __overridden
    cdef Provider __last_overriding
    cdef int __async_mode

    cpdef object _provide(self, tuple args, dict kwargs)
    cpdef void _copy_overridings(self, Provider copied, dict memo)


cdef class Object(Provider):
    cdef object __provides

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class Delegate(Provider):
    cdef object __provides

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class Dependency(Provider):
    cdef object __instance_of
    cdef object __default


cdef class ExternalDependency(Dependency):
    pass


cdef class DependenciesContainer(Object):
    cdef dict __providers

    cpdef object _override_providers(self, object container)


cdef class OverridingContext(object):
    cdef Provider __overridden
    cdef Provider __overriding


# Callable providers
cdef class Callable(Provider):
    cdef object __provides

    cdef tuple __args
    cdef int __args_len

    cdef tuple __kwargs
    cdef int __kwargs_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedCallable(Callable):
    pass


cdef class AbstractCallable(Callable):
    cpdef object _provide(self, tuple args, dict kwargs)


cdef class CallableDelegate(Delegate):
    pass


# Coroutine providers
cdef class Coroutine(Callable):
    pass


cdef class DelegatedCoroutine(Coroutine):
    pass


cdef class AbstractCoroutine(Coroutine):
    cpdef object _provide(self, tuple args, dict kwargs)


cdef class CoroutineDelegate(Delegate):
    pass


# Configuration providers
cdef class ConfigurationOption(Provider):
    cdef tuple __name
    cdef Configuration __root
    cdef dict __children
    cdef bint __required
    cdef object __cache


cdef class TypedConfigurationOption(Callable):
    pass


cdef class Configuration(Object):
    cdef str __name
    cdef bint __strict
    cdef dict __children
    cdef object __weakref__


# Factory providers
cdef class Factory(Provider):
    cdef Callable __instantiator

    cdef tuple __attributes
    cdef int __attributes_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedFactory(Factory):
    pass


cdef class AbstractFactory(Factory):
    cpdef object _provide(self, tuple args, dict kwargs)


cdef class FactoryDelegate(Delegate):
    pass


cdef class FactoryAggregate(Provider):
    cdef dict __factories

    cdef Factory __get_factory(self, str factory_name)


# Singleton providers
cdef class BaseSingleton(Provider):
    cdef Factory __instantiator
    cdef object __storage


cdef class Singleton(BaseSingleton):

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedSingleton(Singleton):
    pass


cdef class ThreadSafeSingleton(BaseSingleton):
    cdef object __storage_lock

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedThreadSafeSingleton(ThreadSafeSingleton):
    pass


cdef class ThreadLocalSingleton(BaseSingleton):

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedThreadLocalSingleton(ThreadLocalSingleton):
    pass


cdef class AbstractSingleton(BaseSingleton):
    pass


cdef class SingletonDelegate(Delegate):
    pass


# Miscellaneous providers

cdef class List(Provider):
    cdef tuple __args
    cdef int __args_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class Dict(Provider):
    cdef tuple __kwargs
    cdef int __kwargs_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class Resource(Provider):
    cdef object __initializer
    cdef bint __initialized
    cdef object __shutdowner
    cdef object __resource

    cdef tuple __args
    cdef int __args_len

    cdef tuple __kwargs
    cdef int __kwargs_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class Container(Provider):
    cdef object __container_cls
    cdef dict __overriding_providers
    cdef object __container

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class Selector(Provider):
    cdef object __selector
    cdef dict __providers

    cpdef object _provide(self, tuple args, dict kwargs)

# Provided instance

cdef class ProvidedInstance(Provider):
    cdef Provider __provider

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class AttributeGetter(Provider):
    cdef Provider __provider
    cdef object __attribute

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class ItemGetter(Provider):
    cdef Provider __provider
    cdef object __item

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class MethodCaller(Provider):
    cdef Provider __provider
    cdef tuple __args
    cdef int __args_len
    cdef tuple __kwargs
    cdef int __kwargs_len

    cpdef object _provide(self, tuple args, dict kwargs)


# Injections
cdef class Injection(object):
    cdef object __value
    cdef int __is_provider
    cdef int __is_delegated
    cdef int __call


cdef class PositionalInjection(Injection):
    pass


cdef class NamedInjection(Injection):
    cdef object __name


cpdef tuple parse_positional_injections(tuple args)


cpdef tuple parse_named_injections(dict kwargs)


# Utils
cdef object CLASS_TYPES


cpdef bint is_provider(object instance)


cpdef object ensure_is_provider(object instance)


cpdef bint is_delegated(object instance)


cpdef str represent_provider(object provider, object provides)


cpdef object deepcopy(object instance, dict memo=*)


# Inline helper functions
cdef inline object __get_name(NamedInjection self):
    return self.__name


cdef inline object __get_value(Injection self):
    if self.__call == 0:
        return self.__value
    return self.__value()


cdef inline object __get_value_kwargs(Injection self, dict kwargs):
    if self.__call == 0:
        return self.__value
    return self.__value(**kwargs)


cdef inline tuple __separate_prefixed_kwargs(dict kwargs):
    cdef dict plain_kwargs = {}
    cdef dict prefixed_kwargs = {}

    for key, value in kwargs.items():
        if '__' not in key:
            plain_kwargs[key] = value
            continue

        index = key.index('__')
        prefix, name = key[:index], key[index+2:]

        if prefix not in prefixed_kwargs:
            prefixed_kwargs[prefix] = {}
        prefixed_kwargs[prefix][name] = value

    return plain_kwargs, prefixed_kwargs


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline object __provide_positional_args(
        tuple args,
        tuple inj_args,
        int inj_args_len,
):
    cdef int index
    cdef list positional_args = []
    cdef list awaitables = []
    cdef PositionalInjection injection

    if inj_args_len == 0:
        return args

    for index in range(inj_args_len):
        injection = <PositionalInjection>inj_args[index]
        value = __get_value(injection)
        positional_args.append(value)

        if __isawaitable(value):
            awaitables.append((index, value))

    positional_args.extend(args)

    if awaitables:
        return __awaitable_args_kwargs_future(positional_args, awaitables)

    return positional_args


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline object __provide_keyword_args(
        dict kwargs,
        tuple inj_kwargs,
        int inj_kwargs_len,
):
    cdef int index
    cdef object name
    cdef object value
    cdef dict prefixed = {}
    cdef list awaitables = []
    cdef NamedInjection kw_injection

    if len(kwargs) == 0:
        for index in range(inj_kwargs_len):
            kw_injection = <NamedInjection>inj_kwargs[index]
            name = __get_name(kw_injection)
            value = __get_value(kw_injection)
            kwargs[name] = value
            if __isawaitable(value):
                awaitables.append((name, value))
    else:
        kwargs, prefixed = __separate_prefixed_kwargs(kwargs)


        for index in range(inj_kwargs_len):
            kw_injection = <NamedInjection>inj_kwargs[index]
            name = __get_name(kw_injection)

            if name in kwargs:
                continue

            if name in prefixed:
                value = __get_value_kwargs(kw_injection, prefixed[name])
            else:
                value = __get_value(kw_injection)

            kwargs[name] = value
            if __isawaitable(value):
                awaitables.append((name, value))

    if awaitables:
        return __awaitable_args_kwargs_future(kwargs, awaitables)

    return kwargs


cdef inline object __awaitable_args_kwargs_future(object args, list awaitables):
    future_result = asyncio.Future()

    args_ready = asyncio.gather(*[value for _, value in awaitables])
    args_ready.add_done_callback(
        functools.partial(
            __async_prepare_args_kwargs_callback,
            future_result,
            args,
            awaitables,
        ),
    )
    asyncio.ensure_future(args_ready)

    return future_result


cdef inline void __async_prepare_args_kwargs_callback(
        object future_result,
        object args,
        object awaitables,
        object future,
):
    awaited = future.result()
    for value, (key, _) in zip(awaited, awaitables):
        args[key] = value
    future_result.set_result(args)


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline object __provide_attributes(tuple attributes, int attributes_len):
    cdef NamedInjection attr_injection
    cdef dict attribute_injections = {}
    cdef list awaitables = []

    for index in range(attributes_len):
        attr_injection = <NamedInjection>attributes[index]
        name = __get_name(attr_injection)
        value = __get_value(attr_injection)
        attribute_injections[name] = value
        if __isawaitable(value):
            awaitables.append((name, value))

    if awaitables:
        return __awaitable_args_kwargs_future(attribute_injections, awaitables)

    return attribute_injections


cdef inline object __async_inject_attributes(future_instance, future_attributes):
    future_result = asyncio.Future()

    attributes_ready = asyncio.gather(future_instance, future_attributes)
    attributes_ready.add_done_callback(
        functools.partial(
            __async_inject_attributes_callback,
            future_result,
        ),
    )
    asyncio.ensure_future(attributes_ready)

    return future_result


cdef inline void __async_inject_attributes_callback(object future_result, object future):
    instance, attributes = future.result()
    __inject_attributes(instance, attributes)
    future_result.set_result(instance)


cdef inline void __inject_attributes(object instance, dict attributes):
    for name, value in attributes.items():
        setattr(instance, name, value)


cdef inline object __call(
        object call,
        tuple context_args,
        tuple injection_args,
        int injection_args_len,
        dict context_kwargs,
        tuple injection_kwargs,
        int injection_kwargs_len,
):
    args = __provide_positional_args(
        context_args,
        injection_args,
        injection_args_len,
    )
    kwargs = __provide_keyword_args(
        context_kwargs,
        injection_kwargs,
        injection_kwargs_len,
    )

    args_awaitable = __isawaitable(args)
    kwargs_awaitable = __isawaitable(kwargs)

    if args_awaitable or kwargs_awaitable:
        if not args_awaitable:
            future = asyncio.Future()
            future.set_result(args)
            args = future

        if not kwargs_awaitable:
            future = asyncio.Future()
            future.set_result(kwargs)
            kwargs = future

        future_result = asyncio.Future()

        args_kwargs_ready = asyncio.gather(args, kwargs)
        args_kwargs_ready.add_done_callback(
            functools.partial(
                __async_call_callback,
                future_result,
                call,
            ),
        )
        asyncio.ensure_future(args_kwargs_ready)

        return future_result

    return call(*args, **kwargs)


cdef inline void __async_call_callback(object future_result, object call, object future):
    args, kwargs = future.result()
    result = call(*args, **kwargs)

    if __isawaitable(result):
        result = asyncio.ensure_future(result)
        result.add_done_callback(functools.partial(__async_result_callback, future_result))
        return

    future_result.set_result(result)


cdef inline object __async_result_callback(object future_result, object future):
    future_result.set_result(future.result())


cdef inline object __callable_call(Callable self, tuple args, dict kwargs):
    return __call(
        self.__provides,
        args,
        self.__args,
        self.__args_len,
        kwargs,
        self.__kwargs,
        self.__kwargs_len,
    )


cdef inline object __factory_call(Factory self, tuple args, dict kwargs):
    cdef object instance

    instance = __callable_call(self.__instantiator, args, kwargs)

    if self.__attributes_len > 0:
        attributes = __provide_attributes(self.__attributes, self.__attributes_len)

        instance_awaitable = __isawaitable(instance)
        attributes_awaitable = __isawaitable(attributes)

        if instance_awaitable or attributes_awaitable:
            if not instance_awaitable:
                future = asyncio.Future()
                future.set_result(instance)
                instance = future

            if not attributes_awaitable:
                future = asyncio.Future()
                future.set_result(attributes)
                attributes = future

            return __async_inject_attributes(instance, attributes)

        __inject_attributes(instance, attributes)

    return instance


cdef bint __has_isawaitable = False


cdef inline bint __isawaitable(object instance):
    global __has_isawaitable

    if __has_isawaitable is True:
        return inspect.isawaitable(instance)

    if hasattr(inspect, 'isawaitable'):
        __has_isawaitable = True
        return inspect.isawaitable(instance)

    return False
