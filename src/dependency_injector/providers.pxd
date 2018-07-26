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


cdef class Delegate(Object):
    pass


cdef class Dependency(Provider):
    cdef type __instance_of


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


# Configuration providers
cdef class Configuration(Object):
    cdef str __name
    cdef dict __children


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


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline tuple __provide_positional_args(tuple args,
                                            tuple inj_args,
                                            int inj_args_len):
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
cdef inline dict __provide_keyword_args(dict kwargs,
                                        tuple inj_kwargs,
                                        int inj_kwargs_len):
    cdef int index
    cdef object name
    cdef NamedInjection kw_injection

    if len(kwargs) == 0:
        for index in range(inj_kwargs_len):
            kw_injection = <NamedInjection>inj_kwargs[index]
            name = __get_name(kw_injection)
            kwargs[name] = __get_value(kw_injection)
    else:
        for index in range(inj_kwargs_len):
            kw_injection = <NamedInjection>inj_kwargs[index]
            name = __get_name(kw_injection)
            if name not in kwargs:
                kwargs[name] = __get_value(kw_injection)

    return kwargs


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline object __inject_attributes(object instance,
                                       tuple attributes,
                                       int attributes_len):
    cdef NamedInjection attr_injection
    for index in range(attributes_len):
        attr_injection = <NamedInjection>attributes[index]
        setattr(instance,
                __get_name(attr_injection),
                __get_value(attr_injection))


cdef inline object __callable_call(Callable self, tuple args, dict kwargs):
    cdef tuple positional_args
    cdef dict keyword_args

    positional_args = __provide_positional_args(args,
                                                self.__args,
                                                self.__args_len)
    keyword_args = __provide_keyword_args(kwargs,
                                          self.__kwargs,
                                          self.__kwargs_len)

    return self.__provides(*positional_args, **keyword_args)


cdef inline object __factory_call(Factory self, tuple args, dict kwargs):
    cdef object instance

    instance = __callable_call(self.__instantiator, args, kwargs)

    if self.__attributes_len > 0:
        __inject_attributes(instance,
                            self.__attributes,
                            self.__attributes_len)

    return instance
