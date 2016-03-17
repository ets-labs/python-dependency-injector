===========================================================
Dependency Injector - Python dependency injection framework
===========================================================

*Dependency Injector* is a Python dependency injection framework. It was 
designed to be unified, developer's friendly tool for managing any kind
of Python objects and their dependencies in formal, pretty way.

Below is a list of some key features and points of *Dependency Injector*:

- Easy, smart, pythonic style.
- Obvious, clear structure.
- Memory efficiency.
- Thread safety.
- Semantic versioning.

Main idea of *Dependency Injector* is to keep dependencies under control.

Status
------

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

API client example:

.. code-block:: python

    """Pythonic way for Dependency Injection - API Client."""

    from dependency_injector import providers

    from mock import Mock


    class ApiClient(object):
        """Some API client."""

        def __init__(self, host, api_key):
            """Initializer."""
            self.host = host
            self.api_key = api_key

        def call(self, operation, data):
            """Make some network operations."""
            print 'API call [{0}:{1}], method - {2}, data - {3}'.format(
                self.host, self.api_key, operation, repr(data))


    class User(object):
        """User model."""

        def __init__(self, id, api_client):
            """Initializer."""
            self.id = id
            self.api_client = api_client

        def register(self):
            """Register user."""
            self.api_client.call('register', {'id': self.id})


    # Creating ApiClient and User providers:
    api_client = providers.Singleton(ApiClient,
                                     host='production.com',
                                     api_key='PROD_API_KEY')
    user_factory = providers.Factory(User,
                                     api_client=api_client)

    # Creating several users and register them:
    user1 = user_factory(1)
    user1.register()
    # API call [production.com:PROD_API_KEY], method - register, data - {'id': 1}

    user2 = user_factory(2)
    user2.register()
    # API call [production.com:PROD_API_KEY], method - register, data - {'id': 2}

    # Mock ApiClient for testing:
    with api_client.override(Mock(ApiClient)) as api_client_mock:
        user = user_factory('test')
        user.register()
        api_client_mock().call.assert_called_with('register', {'id': 'test'})


    # Overriding of ApiClient on dev environment:
    api_client.override(providers.Singleton(ApiClient,
                                            host='localhost',
                                            api_key='DEV_API_KEY'))

    user3 = user_factory(3)
    user3.register()
    # API call [localhost:DEV_API_KEY], method - register, data - {'id': 3}

Auth system example:

.. code-block:: python

    """Pythonic way for Dependency Injection - Auth System."""

    from dependency_injector import providers
    from dependency_injector import injections


    @providers.DelegatedCallable
    def get_user_info(user_id):
        """Return user info."""
        raise NotImplementedError()


    @providers.Factory
    @injections.inject(get_user_info=get_user_info)
    class AuthComponent(object):
        """Some authentication component."""

        def __init__(self, get_user_info):
            """Initializer."""
            self.get_user_info = get_user_info

        def authenticate_user(self, token):
            """Authenticate user by token."""
            user_info = self.get_user_info(user_id=token + '1')
            return user_info


    print AuthComponent
    print get_user_info


    @providers.override(get_user_info)
    @providers.DelegatedCallable
    def get_user_info(user_id):
        """Return user info."""
        return {'user_id': user_id}


    print AuthComponent().authenticate_user(token='abc')
    # {'user_id': 'abc1'}

Service providers catalog example:

.. code-block:: python

    """Pythonic way for Dependency Injection - Service Providers Catalog."""

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

Providing callbacks catalog example:

.. code-block:: python

    """Pythonic way for Dependency Injection - Providing Callbacks Catalog."""

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

        @providers.Singleton
        def database():
            """Provide database connection.

            :rtype: providers.Provider -> sqlite3.Connection
            """
            return sqlite3.connect(':memory:')

        @providers.Factory
        @injections.inject(db=database)
        def users(**kwargs):
            """Provide users service.

            :rtype: providers.Provider -> UsersService
            """
            return UsersService(**kwargs)

        @providers.Factory
        @injections.inject(db=database)
        @injections.inject(users_service=users)
        def auth(**kwargs):
            """Provide users service.

            :rtype: providers.Provider -> AuthService
            """
            return AuthService(**kwargs)


    # Retrieving catalog providers:
    users_service = Services.users()
    auth_service = Services.auth()

    # Making some asserts:
    assert users_service.db is auth_service.db is Services.database()
    assert isinstance(auth_service.users_service, UsersService)
    assert users_service is not Services.users()
    assert auth_service is not Services.auth()

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
