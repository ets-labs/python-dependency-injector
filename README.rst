====================================================================
Dependency Injector - Dependency injection microframework for Python
====================================================================

*Dependency Injector* is a dependency injection microframework for Python. 
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

Status
------

+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://img.shields.io/pypi/v/dependency_injector.svg                                                   |
|                                       |    :target: https://pypi.org/project/dependency-injector/                                                          |
|                                       |    :alt: Latest Version                                                                                            |
|                                       | .. image:: https://img.shields.io/pypi/l/dependency_injector.svg                                                   |
|                                       |    :target: https://pypi.org/project/dependency-injector/                                                          |
|                                       |    :alt: License                                                                                                   |
|                                       | .. image:: https://pepy.tech/badge/dependency-injector                                                             |
|                                       |    :target: https://pepy.tech/project/dependency-injector                                                          |
|                                       |    :alt: Downloads                                                                                                 |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg                                          |
|                                       |    :target: https://pypi.org/project/dependency-injector/                                                          |
|                                       |    :alt: Supported Python versions                                                                                 |
|                                       | .. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg                                      |
|                                       |    :target: https://pypi.org/project/dependency-injector/                                                          |
|                                       |    :alt: Supported Python implementations                                                                          |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| *Builds and tests coverage*           | .. image:: https://travis-ci.org/ets-labs/python-dependency-injector.svg?branch=master                             |
|                                       |    :target: https://travis-ci.org/ets-labs/python-dependency-injector                                              |
|                                       |    :alt: Build Status                                                                                              |
|                                       | .. image:: http://readthedocs.org/projects/python-dependency-injector/badge/?version=latest                        |
|                                       |    :target: http://python-dependency-injector.ets-labs.org/                                                        |
|                                       |    :alt: Docs Status                                                                                               |
|                                       | .. image:: https://coveralls.io/repos/github/ets-labs/python-dependency-injector/badge.svg?branch=master           |
|                                       |    :target: https://coveralls.io/github/ets-labs/python-dependency-injector?branch=master                          |
|                                       |    :alt: Coverage Status                                                                                           |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| *Github*                              | .. image:: https://img.shields.io/github/watchers/ets-labs/python-dependency-injector.svg?style=social&label=Watch |
|                                       |    :target: https://github.com/ets-labs/python-dependency-injector                                                 |
|                                       |    :alt: Github watchers                                                                                           |
|                                       | .. image:: https://img.shields.io/github/stars/ets-labs/python-dependency-injector.svg?style=social&label=Star     |
|                                       |    :target: https://github.com/ets-labs/python-dependency-injector                                                 |
|                                       |    :alt: Github stargazers                                                                                         |
|                                       | .. image:: https://img.shields.io/github/forks/ets-labs/python-dependency-injector.svg?style=social&label=Fork     |
|                                       |    :target: https://github.com/ets-labs/python-dependency-injector                                                 |
|                                       |    :alt: Github forks                                                                                              |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+

Installation
------------

The *Dependency Injector* library is available on `PyPi`_::

    pip install dependency-injector

Documentation
-------------

The *Dependency Injector* documentation is hosted on ReadTheDocs:

- `User's guide`_
- `API docs`_

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

Example of dependency injection
-------------------------------

Let's go through next example:

.. image:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/engines_cars/diagram.png
    :width: 100%
    :align: center

Listing of ``example.engines`` module:

.. code-block:: python

    """Dependency injection example, engines module."""


    class Engine:
        """Example engine base class.

        Engine is a heart of every car. Engine is a very common term and could be
        implemented in very different ways.
        """


    class GasolineEngine(Engine):
        """Gasoline engine."""


    class DieselEngine(Engine):
        """Diesel engine."""


    class ElectricEngine(Engine):
        """Electric engine."""

Listing of ``example.cars`` module:

.. code-block:: python

    """Dependency injection example, cars module."""


    class Car:
        """Example car."""

        def __init__(self, engine):
            """Initializer."""
            self._engine = engine  # Engine is injected

The next example demonstrates the creation of several cars with different engines:

.. code-block:: python

    """Dependency injection example, Cars & Engines."""

    import example.cars
    import example.engines


    if __name__ == '__main__':
        gasoline_car = example.cars.Car(example.engines.GasolineEngine())
        diesel_car = example.cars.Car(example.engines.DieselEngine())
        electric_car = example.cars.Car(example.engines.ElectricEngine())

While the previous example demonstrates the advantages of dependency injection,
there is a disadvantage demonstrated as well - the creation of a car requires 
additional code to specify its dependencies. However, this disadvantage
could be avoided by using a dependency injection framework for the creation of 
an inversion of control container (IoC container).

Here's an example of the creation of several inversion of control containers
(IoC containers) using *Dependency Injector*:

.. code-block:: python

    """Dependency injection example, Cars & Engines IoC containers."""

    import example.cars
    import example.engines

    import dependency_injector.containers as containers
    import dependency_injector.providers as providers


    class Engines(containers.DeclarativeContainer):
        """IoC container of engine providers."""

        gasoline = providers.Factory(example.engines.GasolineEngine)

        diesel = providers.Factory(example.engines.DieselEngine)

        electric = providers.Factory(example.engines.ElectricEngine)


    class Cars(containers.DeclarativeContainer):
        """IoC container of car providers."""

        gasoline = providers.Factory(example.cars.Car,
                                     engine=Engines.gasoline)

        diesel = providers.Factory(example.cars.Car,
                                   engine=Engines.diesel)

        electric = providers.Factory(example.cars.Car,
                                     engine=Engines.electric)


    if __name__ == '__main__':
        gasoline_car = Cars.gasoline()
        diesel_car = Cars.diesel()
        electric_car = Cars.electric()

Dependency Injector structure
-----------------------------

*Dependency Injector* is a microframework and has a simple structure.

There are two main entities: providers and containers.

.. image:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/internals.png
    :width: 100%
    :align: center

Providers
~~~~~~~~~

Providers describe strategies of accessing objects. They define how particular 
objects are provided.

- **Provider** - base provider class.
- **Callable** - provider that calls a wrapped callable on every call. Supports 
  positional and keyword argument injections.
- **Factory** - provider that creates new instance of specified class on every 
  call. Supports positional and keyword argument injections, as well as 
  attribute injections.
- **Singleton** - provider that creates new instance of specified class on its
  first call and returns the same instance on every next call. Supports
  position and keyword argument injections, as well as attribute injections.
- **Object** - provider that returns provided instance "as is".
- **ExternalDependency** - provider that can be useful for development of 
  self-sufficient libraries, modules, and applications that require external
  dependencies.
- **Configuration** - provider that helps with implementing late static binding 
  of configuration options - use first, define later.

Containers
~~~~~~~~~~

Containers are collections of providers. The main purpose of containers is to 
group providers.

- **DeclarativeContainer** - is an inversion of control container that can be 
  defined in a declarative manner. It covers most of the cases where a list of
  providers that is be included in a container is deterministic 
  (that means the container will not change its structure in runtime).
- **DynamicContainer** - is an inversion of control container with a dynamic 
  structure. It covers most of the cases where a  list of providers that 
  would be included in container is non-deterministic and depends on  the
  application's flow or its configuration (container's structure could be 
  determined just after the application starts and might perform some initial 
  work, like parsing a list of container providers from a configuration).

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

Feedback & Support
------------------

Feel free to post questions, bugs, feature requests, proposals, etc. on
the *Dependency Injector*  GitHub issues page:

    https://github.com/ets-labs/python-dependency-injector/issues

Your feedback is quite important!


.. _Dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
.. _Inversion of control: https://en.wikipedia.org/wiki/Inversion_of_control
.. _PyPi: https://pypi.org/project/dependency-injector/
.. _User's guide: http://python-dependency-injector.ets-labs.org/
.. _API docs: http://python-dependency-injector.ets-labs.org/api/
