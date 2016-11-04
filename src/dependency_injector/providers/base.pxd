"""Dependency injector base providers.

Powered by Cython.
"""


cdef class Provider(object):
    cdef tuple __overridden
    cdef int __overridden_len

    cpdef object _provide(self, tuple args, dict kwargs)
    cpdef object _call_last_overriding(self, tuple args, dict kwargs)
