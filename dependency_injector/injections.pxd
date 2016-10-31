"""Dependency injector injections.

Cython optimized code.
"""

cpdef tuple parse_positional_injections(tuple args)
cpdef tuple parse_named_injections(dict kwargs)


cdef class Injection:
    pass


cdef class PositionalInjection(Injection):
    cdef object __value
    cdef int __is_provider
    cdef int __is_delegated
    cdef int __call

    cdef inline object get_value(self):
        if self.__call == 0:
            return self.__value
        return self.__value()


cdef class NamedInjection(Injection):
    cdef object __name
    cdef object __value
    cdef int __is_provider
    cdef int __is_delegated
    cdef int __call

    cdef inline object get_name(self):
        return self.__name

    cdef inline object get_value(self):
        if self.__call == 0:
            return self.__value
        return self.__value()


cdef inline tuple __provide_positional_args(tuple inj_args,
                                            int inj_args_len,
                                            tuple args):
    cdef PositionalInjection injection
    if inj_args_len > 0:
        positional_args = list()
        for index in range(inj_args_len):
            injection = <PositionalInjection>inj_args[index]
            positional_args.append(injection.get_value())
        positional_args.extend(args)
        args = positional_args
    return args

cdef inline dict __provide_keyword_args(tuple inj_kwargs,
                                        int inj_kwargs_len,
                                        dict kwargs):
    cdef NamedInjection kw_injection
    if inj_kwargs_len > 0:
        for index in range(inj_kwargs_len):
            kw_injection = <NamedInjection>inj_kwargs[index]
            kwargs[kw_injection.get_name()] = kw_injection.get_value()
    return kwargs
