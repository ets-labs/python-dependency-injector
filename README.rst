Dependency Injector
===================

Dependency injection framework for Python projects.

+---------------------------------------+---------------------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://img.shields.io/pypi/v/dependency_injector.svg                |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                   |
|                                       |    :alt: Latest Version                                                         |
|                                       | .. image:: https://img.shields.io/pypi/dm/dependency_injector.svg               |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                   |
|                                       |    :alt: Downloads                                                              |
|                                       | .. image:: https://img.shields.io/pypi/l/dependency_injector.svg                |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                   |
|                                       |    :alt: License                                                                |
+---------------------------------------+---------------------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg       |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                   |
|                                       |    :alt: Supported Python versions                                              |
|                                       | .. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg   |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                   |
|                                       |    :alt: Supported Python implementations                                       |
+---------------------------------------+---------------------------------------------------------------------------------+
| *Builds and tests coverage*           | .. image:: https://travis-ci.org/ets-labs/dependency_injector.svg?branch=master |
|                                       |    :target: https://travis-ci.org/ets-labs/dependency_injector                  |
|                                       |    :alt: Build Status                                                           |
|                                       | .. image:: https://coveralls.io/repos/ets-labs/dependency_injector/badge.svg    |
|                                       |    :target: https://coveralls.io/r/ets-labs/dependency_injector                 |
|                                       |    :alt: Coverage Status                                                        |
+---------------------------------------+---------------------------------------------------------------------------------+

*Dependency Injector* is a dependency injection framework for Python projects. 
It was designed to be unified, developer's friendly tool for managing any kind
of Python objects and their dependencies in formal, pretty way.

Below is a list of some key features and points of *Dependency Injector*
framework:

- Easy, smart, pythonic style.
- Obvious, clear structure.
- Memory efficiency.
- Thread safety.
- Semantic versioning.

Main idea of *Dependency Injector* is to keep dependencies under control.

Installation
------------

*Dependency Injector* library is available on PyPi_::

    pip install dependency_injector

Documentation
-------------

*Dependency Injector* documentation is hosted on ReadTheDocs:

- `User's guide`_ 
- `API docs`_

Examples
--------

.. code-block:: python

    """Concept example of `Dependency Injector`."""

    import sqlite3

    from dependency_injector import catalogs
    from dependency_injector import providers
    from dependency_injector import injections


    class UsersService(object):
        """Users service, that has dependency on database."""

        def __init__(self, db):
            """Initializer."""
            self.db = db


    class AuthService(object):
        """Auth service, that has dependencies on users service and database."""

        def __init__(self, db, users_service):
            """Initializer."""
            self.db = db
            self.users_service = users_service


    class Services(catalogs.DeclarativeCatalog):
        """Catalog of service providers."""

        database = providers.Singleton(sqlite3.connect, ':memory:')
        """:type: providers.Provider -> sqlite3.Connection"""

        users = providers.Factory(UsersService,
                                  db=database)
        """:type: providers.Provider -> UsersService"""

        auth = providers.Factory(AuthService,
                                 db=database,
                                 users_service=users)
        """:type: providers.Provider -> AuthService"""


    # Retrieving catalog providers:
    users_service = Services.users()
    auth_service = Services.auth()

    # Making some asserts:
    assert users_service.db is auth_service.db is Services.database()
    assert isinstance(auth_service.users_service, UsersService)
    assert users_service is not Services.users()
    assert auth_service is not Services.auth()


    # Making some "inline" injections:
    @injections.inject(users_service=Services.users)
    @injections.inject(auth_service=Services.auth)
    @injections.inject(database=Services.database)
    def example(users_service, auth_service, database):
        """Example callback."""
        assert users_service.db is auth_service.db
        assert auth_service.db is database
        assert database is Services.database()


    # Making a call of decorated callback:
    example()


    # Overriding auth service provider and making some asserts:
    class ExtendedAuthService(AuthService):
        """Extended version of auth service."""

        def __init__(self, db, users_service, ttl):
            """Initializer."""
            self.ttl = ttl
            super(ExtendedAuthService, self).__init__(db=db,
                                                      users_service=users_service)


    Services.auth.override(providers.Factory(ExtendedAuthService,
                                             db=Services.database,
                                             users_service=Services.users,
                                             ttl=3600))


    auth_service = Services.auth()

    assert isinstance(auth_service, ExtendedAuthService)

You can get more *Dependency Injector* examples in ``/examples`` directory on
GitHub:

    https://github.com/ets-labs/dependency_injector


Feedback
--------

Feel free to post questions, bugs, feature requests, proposals etc. on
*Dependency Injector*  GitHub Issues:

    https://github.com/ets-labs/dependency_injector/issues

Your feedback is quite important!


.. _PyPi: https://pypi.python.org/pypi/dependency_injector
.. _User's guide: http://dependency_injector.readthedocs.org/en/stable/
.. _API docs: http://dependency-injector.readthedocs.org/en/stable/api/
.. _SLOC: http://en.wikipedia.org/wiki/Source_lines_of_code
.. _SOLID: http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29
.. _IoC: http://en.wikipedia.org/wiki/Inversion_of_control
.. _dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
