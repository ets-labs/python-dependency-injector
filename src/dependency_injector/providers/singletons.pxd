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

    cdef inline object __provide(self, tuple args, dict kwargs):
        if self.__storage is None:
            self.__storage = self.__instantiator.__provide(args, kwargs)
        return self.__storage


cdef class DelegatedSingleton(Singleton):
    pass


cdef class ThreadSafeSingleton(BaseSingleton):
    cdef object __storage
    cdef object __lock

    cpdef object _provide(self, tuple args, dict kwargs)

    cdef inline object __provide(self, tuple args, dict kwargs):
        with self.__lock:
            if self.__storage is None:
                self.__storage = self.__instantiator.__provide(args, kwargs)
        return self.__storage


cdef class DelegatedThreadSafeSingleton(ThreadSafeSingleton):
    pass


cdef class ThreadLocalSingleton(BaseSingleton):
    cdef object __storage

    cpdef object _provide(self, tuple args, dict kwargs)

    cdef inline object __provide(self, tuple args, dict kwargs):
        cdef object instance

        try:
            instance = self.__storage.instance
        except AttributeError:
            instance = self.__instantiator.__provide(args, kwargs)
            self.__storage.instance = instance
        finally:
            return instance


cdef class DelegatedThreadLocalSingleton(ThreadLocalSingleton):
    pass
