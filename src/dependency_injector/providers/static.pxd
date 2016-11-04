"""Dependency injector static providers.

Powered by Cython.
"""

from .base cimport Provider


cdef class Object(Provider):
    cdef object __provides

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class Delegate(Object):
    pass

cdef class ExternalDependency(Provider):
    cdef type __instance_of
