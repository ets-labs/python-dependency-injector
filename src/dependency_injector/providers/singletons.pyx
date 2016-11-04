"""Dependency injector singleton providers.

Powered by Cython.
"""

from .base cimport Provider


cdef class BaseSingleton(Provider):
    pass


cdef class Singleton(BaseSingleton):
    pass


cdef class DelegatedSingleton(Singleton):
    __IS_DELEGATED__ = True


cdef class ThreadSafeSingleton(Singleton):
    pass


cdef class DelegatedThreadSafeSingleton(ThreadSafeSingleton):
    __IS_DELEGATED__ = True


cdef class ThreadLocalSingleton(BaseSingleton):
    pass


cdef class DelegatedThreadLocalSingleton(ThreadLocalSingleton):
    __IS_DELEGATED__ = True
