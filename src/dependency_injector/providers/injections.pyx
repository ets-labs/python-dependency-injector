"""Dependency injector injections.

Powered by Cython.
"""

cimport cython

from .utils cimport (
    is_provider,
    is_delegated,
)


cdef class Injection:
    """Abstract injection class."""


cdef class PositionalInjection(Injection):
    """Positional injection class."""

    def __init__(self, value):
        """Initializer."""
        self.__value = value
        self.__is_provider = <int>is_provider(value)
        self.__is_delegated = <int>is_delegated(value)
        self.__call = <int>(self.__is_provider == 1 and
                            self.__is_delegated == 0)

    def get_value(self):
        """Return injection value."""
        return self.__get_value()

    def get_original_value(self):
        """Return original value."""
        return self.__value


cdef class NamedInjection(Injection):
    """Keyword injection class."""

    def __init__(self, name, value):
        """Initializer."""
        self.__name = name
        self.__value = value
        self.__is_provider = <int>is_provider(value)
        self.__is_delegated = <int>is_delegated(value)
        self.__call = <int>(self.__is_provider == 1 and
                            self.__is_delegated == 0)

    def get_name(self):
        """Return injection value."""
        return self.__get_name()

    def get_value(self):
        """Return injection value."""
        return self.__get_value()

    def get_original_value(self):
        """Return original value."""
        return self.__value


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple parse_positional_injections(tuple args):
    """Parse positional injections."""
    cdef list injections = list()
    cdef int args_len = len(args)

    cdef int index
    cdef object arg
    cdef PositionalInjection injection

    for index in range(args_len):
        arg = args[index]
        injection = PositionalInjection(arg)
        injections.append(injection)

    return tuple(injections)


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple parse_named_injections(dict kwargs):
    """Parse named injections."""
    cdef list injections = list()

    cdef object name
    cdef object arg
    cdef NamedInjection injection

    for name, arg in kwargs.items():
        injection = NamedInjection(name, arg)
        injections.append(injection)

    return tuple(injections)
