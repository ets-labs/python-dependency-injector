"""Dependency injector providers.

Powered by Cython.
"""

cimport cython


# Base providers
cdef class Provider(object):
    cdef tuple __overridden
    cdef Provider __last_overriding

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
    cdef object __root_ref
    cdef dict __children
    cdef object __cache


cdef class Configuration(Object):
    cdef str __name
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


cdef class Singleton(BaseSingleton):
    cdef object __storage

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedSingleton(Singleton):
    pass


cdef class ThreadSafeSingleton(BaseSingleton):
    cdef object __storage
    cdef object __storage_lock

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedThreadSafeSingleton(ThreadSafeSingleton):
    pass


cdef class ThreadLocalSingleton(BaseSingleton):
    cdef object __storage

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


cdef class Container(Provider):
    cdef object container_cls
    cdef dict overriding_providers
    cdef object container

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
cdef inline tuple __provide_positional_args(
        tuple args,
        tuple inj_args,
        int inj_args_len,
):
    cdef int index
    cdef list positional_args
    cdef PositionalInjection injection

    if inj_args_len == 0:
        return args

    positional_args = list()
    for index in range(inj_args_len):
        injection = <PositionalInjection>inj_args[index]
        positional_args.append(__get_value(injection))
    positional_args.extend(args)

    return tuple(positional_args)


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline dict __provide_keyword_args(
        dict kwargs,
        tuple inj_kwargs,
        int inj_kwargs_len,
):
    cdef int index
    cdef object name
    cdef object value
    cdef dict prefixed
    cdef NamedInjection kw_injection

    if len(kwargs) == 0:
        for index in range(inj_kwargs_len):
            kw_injection = <NamedInjection>inj_kwargs[index]
            name = __get_name(kw_injection)
            kwargs[name] = __get_value(kw_injection)
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

    return kwargs


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline object __inject_attributes(
        object instance,
        tuple attributes,
        int attributes_len,
):
    cdef NamedInjection attr_injection
    for index in range(attributes_len):
        attr_injection = <NamedInjection>attributes[index]
        setattr(instance,
                __get_name(attr_injection),
                __get_value(attr_injection))


cdef inline object __call(
        object call,
        tuple context_args,
        tuple injection_args,
        int injection_args_len,
        dict kwargs,
        tuple injection_kwargs,
        int injection_kwargs_len,
):
    cdef tuple positional_args
    cdef dict keyword_args

    positional_args = __provide_positional_args(
        context_args,
        injection_args,
        injection_args_len,
    )
    keyword_args = __provide_keyword_args(
        kwargs,
        injection_kwargs,
        injection_kwargs_len,
    )

    return call(*positional_args, **keyword_args)


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
        __inject_attributes(instance,
                            self.__attributes,
                            self.__attributes_len)

    return instance
