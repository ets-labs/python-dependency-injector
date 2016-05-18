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
|                                       | .. image:: https://img.shields.io/pypi/dm/dependency_injector.svg                      |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                          |
|                                       |    :alt: Downloads                                                                     |
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

Brief example below demonstrates usage of *Dependency Injector* catalogs and 
providers for definition of several IoC containers for some microservice 
system that consists from several business and platform services:

.. code-block:: python

    """Example of several Dependency Injector catalogs."""

    import sqlite3
    import boto.s3.connection
    import example.services

    from dependency_injector import catalogs
    from dependency_injector import providers


    class Platform(catalogs.DeclarativeCatalog):
        """Catalog of platform service providers."""

        database = providers.Singleton(sqlite3.connect, ':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection,
                                 aws_access_key_id='KEY',
                                 aws_secret_access_key='SECRET')


    class Services(catalogs.DeclarativeCatalog):
        """Catalog of business service providers."""

        users = providers.Factory(example.services.Users,
                                  db=Platform.database)

        photos = providers.Factory(example.services.Photos,
                                   db=Platform.database,
                                   s3=Platform.s3)

        auth = providers.Factory(example.services.Auth,
                                 db=Platform.database,
                                 token_ttl=3600)

Next example demonstrates usage of these IoC containers with the help of 
``@inject`` decorator:

.. code-block:: python

    """Dependency Injector example."""

    from dependency_injector.injections import inject

    from catalogs import Services


    @inject(users_service=Services.users)
    @inject(auth_service=Services.auth)
    @inject(photos_service=Services.photos)
    def main(login, password, photo, users_service, auth_service, photos_service):
        """Main function."""
        user = users_service.get_user(login)
        auth_service.authenticate(user, password)
        photos_service.upload_photo(user['id'], photo)


    if __name__ == '__main__':
        main(login='user', password='secret', photo='photo.jpg')

Also some alternative definition styles could be used. Like this one:

.. code-block:: python

    class Platform(catalogs.DeclarativeCatalog):
        """Catalog of platform service providers."""

        database = providers.Singleton(sqlite3.connect) \
            .args(':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection) \
            .kwargs(aws_access_key_id='KEY',
                    aws_secret_access_key='SECRET')

or like this one:

.. code-block:: python

    class Platform(catalogs.DeclarativeCatalog):
        """Catalog of platform service providers."""

        database = providers.Singleton(sqlite3.connect)
        database.args(':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection)
        s3.kwargs(aws_access_key_id='KEY',
                  aws_secret_access_key='SECRET')

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
