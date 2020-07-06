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

It was designed to be a unified and developer-friendly tool that helps
implement a dependency injection design pattern in a formal, pretty, and
Pythonic way.

The key features of the *Dependency Injector* framework are:

+ Easy, smart, and pythonic style.
+ Obvious and clear structure.
+ Extensibility and flexibility.
+ High performance.
+ Memory efficiency.
+ Thread safety.
+ Documented.
+ Semantically versioned.

*Dependency Injector* containers and providers are implemented as C extension 
types using Cython.


Installation
------------

The *Dependency Injector* library is available on `PyPi`_::

    pip install dependency-injector

Documentation
-------------

Documentation is on `Read The Docs <http://python-dependency-injector.ets-labs.org/>`_

Dependency injection
--------------------

`Dependency injection`_ is a software design pattern that implements 
`Inversion of control`_ to resolve dependencies. Formally, if object **A** 
depends on object **B**, object **A** must not create or import object **B** 
directly. Instead of this object **A** must provide a way to *inject* 
object **B**. The responsibilities of objects creation and dependency
injection are delegated to external code - the *dependency injector*. 

Popular terminology of the dependency injection pattern:

+ Object **A**, which depends on object **B**, is often called - 
  the *client*.
+ Object **B**, which is depended on, is often called - the *service*.
+ External code that is responsible for creation of objects and injection 
  of dependencies is often called - the *dependency injector*.

There are several ways to inject a *service* into a *client*: 

+ by passing it as an ``__init__`` argument (constructor / initializer
  injection)
+ by setting it as an attribute's value (attribute injection)
+ by passing it as a method's argument (method injection)

The dependency injection pattern has few strict rules that should be followed:

+ The *client* delegates to the *dependency injector* the responsibility 
  of injecting its dependencies - the *service(s)*.
+ The *client* doesn't know how to create the *service*, it knows only 
  the interface of the *service*. The *service* doesn't know that it is used by 
  the *client*.
+ The *dependency injector* knows how to create the *client* and 
  the *service*. It also knows that the *client* depends on the *service*, 
  and knows how to inject the *service* into the *client*.
+ The *client* and the *service* know nothing about the *dependency injector*.

The dependency injection pattern provides the following advantages: 

+ Control of application structure.
+ Decreased coupling of application components.
+ Increased code reusability.
+ Increased testability.
+ Increased maintainability.
+ Reconfiguration of a system without rebuilding.

Dependency Injector in action
-----------------------------

The brief example below is a simplified version of inversion of control 
containers from a real-life application. The example demonstrates the usage
of *Dependency Injector* inversion of control container and  providers for
specifying application components and their dependencies on each other in one
module. Besides other previously mentioned advantages, it shows a great
opportunity to control and manage application's structure in one place.

.. code-block:: python

    """Example of dependency injection in Python."""

    import logging
    import sqlite3

    import boto3

    from dependency_injector import containers, providers
    from example import services, main


    class IocContainer(containers.DeclarativeContainer):
        """Application IoC container."""

        config = providers.Configuration('config')
        logger = providers.Singleton(logging.Logger, name='example')

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
            logger=logger,
        )

        auth_service = providers.Factory(
            services.AuthService,
            token_ttl=config.auth.token_ttl,
            db=database_client,
            logger=logger,
        )

        photos_service = providers.Factory(
            services.PhotosService,
            db=database_client,
            s3=s3_client,
            logger=logger,
        )

        # Misc

        main = providers.Callable(
            main.main,
            users_service=users_service,
            auth_service=auth_service,
            photos_service=photos_service,
        )

The next example demonstrates a run of the example application defined above:

.. code-block:: python

    """Run example of dependency injection in Python."""

    import sys
    import logging

    from container import IocContainer


    if __name__ == '__main__':
        # Configure container:
        container = IocContainer(
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


.. _Dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
.. _Inversion of control: https://en.wikipedia.org/wiki/Inversion_of_control
.. _PyPi: https://pypi.org/project/dependency-injector/
.. _User's guide: http://python-dependency-injector.ets-labs.org/
.. _API docs: http://python-dependency-injector.ets-labs.org/api/
