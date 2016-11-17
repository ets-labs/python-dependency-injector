"""Dependency injector singleton providers.

Powered by Cython.
"""

from .base cimport Provider
from .factories cimport Factory


cdef class BaseSingleton(Provider):
    cdef Factory __instantiator


cdef class Singleton(BaseSingleton):
    cdef object __storage

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedSingleton(Singleton):
    pass


cdef class ThreadSafeSingleton(BaseSingleton):
    cdef object __storage
    cdef object __lock

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedThreadSafeSingleton(ThreadSafeSingleton):
    pass


cdef class ThreadLocalSingleton(BaseSingleton):
    cdef object __storage

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedThreadLocalSingleton(ThreadLocalSingleton):
    pass
