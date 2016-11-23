"""Dependency injector injections.

Powered by Cython.
"""

cimport cython


cdef class Injection(object):
    cdef object __value
    cdef int __is_provider
    cdef int __is_delegated
    cdef int __call


cdef class PositionalInjection(Injection):
    pass


cdef class NamedInjection(Injection):
    cdef object __name


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


cpdef tuple parse_positional_injections(tuple args)


cpdef tuple parse_named_injections(dict kwargs)
