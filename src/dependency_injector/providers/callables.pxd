"""Dependency injector callable providers.

Powered by Cython.
"""

from .base cimport Provider
from .injections cimport (
    PositionalInjection,
    NamedInjection,
    __provide_positional_args,
    __provide_keyword_args,
)



cdef class Callable(Provider):
    cdef object __provides

    cdef tuple __args
    cdef int __args_len

    cdef tuple __kwargs
    cdef int __kwargs_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedCallable(Callable):
    pass


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
