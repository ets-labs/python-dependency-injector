"""Dependency injector singleton providers.

Powered by Cython.
"""

from .base cimport Provider


cdef class BaseSingleton(Provider):
    pass


cdef class Singleton(BaseSingleton):
    pass


cdef class DelegatedSingleton(Singleton):
    pass


cdef class ThreadSafeSingleton(Singleton):
    pass


cdef class DelegatedThreadSafeSingleton(ThreadSafeSingleton):
    pass


cdef class ThreadLocalSingleton(BaseSingleton):
    pass


cdef class DelegatedThreadLocalSingleton(ThreadLocalSingleton):
    pass
