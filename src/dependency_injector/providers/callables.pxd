"""Dependency injector callable providers.

Powered by Cython.
"""

from .base cimport Provider
from .injections cimport (
    PositionalInjection,
    NamedInjection,
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
