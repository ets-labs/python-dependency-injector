"""Dependency injector configuration providers.

Powered by Cython.
"""

from .base cimport (
    Provider,
)


cdef class Configuration(Provider):
    cdef str __name
    cdef object __value
    cdef dict __children

    cpdef str get_name(self)
    cpdef object update(self, object value)
    cpdef object _provide(self, tuple args, dict kwargs)
    cpdef str _get_child_name(self, str child_name)
