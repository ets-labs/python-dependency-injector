"""Dependency injector factory providers.

Powered by Cython.
"""

from .base cimport Provider


cdef class Factory(Provider):
    cdef object __instantiator

    cdef tuple __attributes
    cdef int __attributes_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedFactory(Factory):
    pass
