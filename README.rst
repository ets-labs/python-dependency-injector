===========================================================
Dependency Injector - Python dependency injection framework
===========================================================

*Dependency Injector* is a Python dependency injection framework. It was 
designed to be unified, developer-friendly tool for managing any kind
of Python objects and their dependencies in formal, pretty way.

*Dependency Injector* framework key features are:

+ Easy, smart, pythonic style.
+ Obvious, clear structure.
+ Extensibility and flexibility.
+ Memory efficiency.
+ Thread safety.
+ Documentation.
+ Semantic versioning.

Status
------

+---------------------------------------+----------------------------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://img.shields.io/pypi/v/dependency_injector.svg                       |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                          |
|                                       |    :alt: Latest Version                                                                |
|                                       | .. image:: https://img.shields.io/pypi/l/dependency_injector.svg                       |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                          |
|                                       |    :alt: License                                                                       |
+---------------------------------------+----------------------------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg              |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                          |
|                                       |    :alt: Supported Python versions                                                     |
|                                       | .. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg          |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                          |
|                                       |    :alt: Supported Python implementations                                              |
+---------------------------------------+----------------------------------------------------------------------------------------+
| *Builds and tests coverage*           | .. image:: https://travis-ci.org/ets-labs/python-dependency-injector.svg?branch=master |
|                                       |    :target: https://travis-ci.org/ets-labs/python-dependency-injector                  |
|                                       |    :alt: Build Status                                                                  |
|                                       | .. image:: https://coveralls.io/repos/ets-labs/python-dependency-injector/badge.svg    |
|                                       |    :target: https://coveralls.io/r/ets-labs/python-dependency-injector                 |
|                                       |    :alt: Coverage Status                                                               |
+---------------------------------------+----------------------------------------------------------------------------------------+

Installation
------------

*Dependency Injector* library is available on PyPi_::

    pip install dependency_injector

Example
-------

Brief example below demonstrates usage of *Dependency Injector* containers and 
providers for definition of several IoC containers for some microservice 
system that consists from several business and platform services:

.. code-block:: python

    """Example of several Dependency Injector IoC containers."""

    import sqlite3
    import boto.s3.connection
    import example.services

    import dependency_injector.containers as containers
    import dependency_injector.providers as providers


    class Platform(containers.DeclarativeContainer):
        """IoC container of platform service providers."""

        database = providers.Singleton(sqlite3.connect, ':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection,
                                 aws_access_key_id='KEY',
                                 aws_secret_access_key='SECRET')


    class Services(containers.DeclarativeContainer):
        """IoC container of business service providers."""

        users = providers.Factory(example.services.Users,
                                  db=Platform.database)

        auth = providers.Factory(example.services.Auth,
                                 db=Platform.database,
                                 token_ttl=3600)

        photos = providers.Factory(example.services.Photos,
                                   db=Platform.database,
                                   s3=Platform.s3)

Next example demonstrates usage of ``@inject`` decorator with IoC containers 
defined above: 

.. code-block:: python

    """Dependency Injector @inject decorator example."""

    import application
    import dependency_injector.injections as injections


    @injections.inject(users_service=application.Services.users)
    @injections.inject(auth_service=application.Services.auth)
    @injections.inject(photos_service=application.Services.photos)
    def main(users_service, auth_service, photos_service):
        """Main function."""
        user = users_service.get_user('user')
        auth_service.authenticate(user, 'secret')
        photos_service.upload_photo(user['id'], 'photo.jpg')


    if __name__ == '__main__':
        main()
   
Alternative definition styles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Dependecy Injector* supports few other styles of dependency injections 
definition.

IoC containers from previous example could look like these:

.. code-block:: python

    class Platform(containers.DeclarativeContainer):
        """IoC container of platform service providers."""

        database = providers.Singleton(sqlite3.connect) \
            .add_args(':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection) \
            .add_kwargs(aws_access_key_id='KEY',
                        aws_secret_access_key='SECRET')


    class Services(containers.DeclarativeContainer):
        """IoC container of business service providers."""

        users = providers.Factory(example.services.Users) \
            .add_kwargs(db=Platform.database)

        auth = providers.Factory(example.services.Auth) \
            .add_kwargs(db=Platform.database,
                        token_ttl=3600)

        photos = providers.Factory(example.services.Photos) \
            .add_kwargs(db=Platform.database,
                        s3=Platform.s3)

or like this these:

.. code-block:: python

    class Platform(containers.DeclarativeContainer):
        """IoC container of platform service providers."""

        database = providers.Singleton(sqlite3.connect)
        database.add_args(':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection)
        s3.add_kwargs(aws_access_key_id='KEY',
                      aws_secret_access_key='SECRET')


    class Services(containers.DeclarativeContainer):
        """IoC container of business service providers."""

        users = providers.Factory(example.services.Users)
        users.add_kwargs(db=Platform.database)

        auth = providers.Factory(example.services.Auth)
        auth.add_kwargs(db=Platform.database,
                        token_ttl=3600)

        photos = providers.Factory(example.services.Photos)
        photos.add_kwargs(db=Platform.database,
                          s3=Platform.s3)

You can get more *Dependency Injector* examples in ``/examples`` directory on
GitHub:

    https://github.com/ets-labs/python-dependency-injector

Documentation
-------------

*Dependency Injector* documentation is hosted on ReadTheDocs:

- `User's guide`_ 
- `API docs`_

Feedback
--------

Feel free to post questions, bugs, feature requests, proposals etc. on
*Dependency Injector*  GitHub Issues:

    https://github.com/ets-labs/python-dependency-injector/issues

Your feedback is quite important!


.. _PyPi: https://pypi.python.org/pypi/dependency_injector
.. _User's guide: http://python-dependency-injector.ets-labs.org/en/stable/
.. _API docs: http://python-dependency-injector.ets-labs.org/en/stable/api/
.. _SLOC: http://en.wikipedia.org/wiki/Source_lines_of_code
.. _SOLID: http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29
.. _IoC: http://en.wikipedia.org/wiki/Inversion_of_control
.. _dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
