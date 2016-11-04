"""Dependency injector callable providers.

Powered by Cython.
"""

from .base cimport Provider


cdef class Callable(Provider):
    pass


cdef class DelegatedCallable(Callable):
    __IS_DELEGATED__ = True
