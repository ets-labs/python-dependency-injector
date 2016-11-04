"""Dependency injector errors.

Powered by Cython.
"""


cdef class Error(Exception):
    """Base error.

    All dependency injector errors extend this error class.
    """
