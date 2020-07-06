.. figure:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/logo.svg

| 

.. image:: https://img.shields.io/pypi/v/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Latest Version
.. image:: https://img.shields.io/pypi/l/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: License
.. image:: https://pepy.tech/badge/dependency-injector
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads
.. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Supported Python versions
.. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Supported Python implementations
.. image:: https://travis-ci.org/ets-labs/python-dependency-injector.svg?branch=master
   :target: https://travis-ci.org/ets-labs/python-dependency-injector
   :alt: Build Status
.. image:: http://readthedocs.org/projects/python-dependency-injector/badge/?version=latest
   :target: http://python-dependency-injector.ets-labs.org/
   :alt: Docs Status
.. image:: https://coveralls.io/repos/github/ets-labs/python-dependency-injector/badge.svg?branch=master
   :target: https://coveralls.io/github/ets-labs/python-dependency-injector?branch=master
   :alt: Coverage Status

What is ``Dependency Injector``?
================================

``Dependency Injector`` is a Python dependency injection framework for Python.

Example:

.. code-block:: python

    import logging
    import sqlite3

    import boto3

    from dependency_injector import containers, providers
    from example import services, main


    class Application(containers.DeclarativeContainer):
        """Application container."""

        config = providers.Configuration('config')

        # Gateways

        database_client = providers.Singleton(sqlite3.connect, config.database.dsn)

        s3_client = providers.Singleton(
            boto3.client, 's3',
            aws_access_key_id=config.aws.access_key_id,
            aws_secret_access_key=config.aws.secret_access_key,
        )

        # Services

        users_service = providers.Factory(
            services.UsersService,
            db=database_client,
        )

        auth_service = providers.Factory(
            services.AuthService,
            token_ttl=config.auth.token_ttl,
            db=database_client,
        )

        photos_service = providers.Factory(
            services.PhotosService,
            db=database_client,
            s3=s3_client,
        )


Run the application:

.. code-block:: python

    """Run example of dependency injection in Python."""

    import sys
    import logging

    from container import Application


    if __name__ == '__main__':
        # Configure container:
        container = Application(
            config={
                'database': {
                    'dsn': ':memory:',
                },
                'aws': {
                    'access_key_id': 'KEY',
                    'secret_access_key': 'SECRET',
                },
                'auth': {
                    'token_ttl': 3600,
                },
            }
        )
        container.logger().addHandler(logging.StreamHandler(sys.stdout))

        # Run application:
        container.main(*sys.argv[1:])

You can find more *Dependency Injector* examples in the ``/examples`` directory
on our GitHub:

    https://github.com/ets-labs/python-dependency-injector


Installation
------------

The *Dependency Injector* library is available on `PyPi`_::

    pip install dependency-injector

Documentation
-------------

Documentation is on `Read The Docs <http://python-dependency-injector.ets-labs.org/>`_


.. _Dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
.. _Inversion of control: https://en.wikipedia.org/wiki/Inversion_of_control
.. _PyPi: https://pypi.org/project/dependency-injector/
.. _User's guide: http://python-dependency-injector.ets-labs.org/
.. _API docs: http://python-dependency-injector.ets-labs.org/api/
