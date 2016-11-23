"""Dependency injector provider utils.

Powered by Cython.
"""

cdef object CLASS_TYPES


cpdef bint is_provider(object instance)


cpdef object ensure_is_provider(object instance)


cpdef bint is_delegated(object instance)


cpdef str represent_provider(object provider, object provides)


cpdef object deepcopy(object instance, dict memo=*)
