"""Dependency injector provider utils.

Powered by Cython.
"""

from .base cimport Provider


cdef tuple CLASS_TYPES


cdef class OverridingContext(object):
    cdef Provider __overridden
    cdef Provider __overriding


cpdef bint is_provider(object instance)
cpdef object ensure_is_provider(object instance)
cpdef bint is_delegated(object instance)
cpdef str represent_provider(object provider, object provides)
