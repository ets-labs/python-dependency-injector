"""Dependency injector containers.

Powered by Cython.
"""

# Declarative containers are declared as regular types because of metaclasses


# Dynamic container


# Utils
cpdef bint is_container(object instance)


cpdef object _check_provider_type(object container, object provider)
