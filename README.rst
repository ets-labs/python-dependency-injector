====================================================================
Dependency Injector - Dependency injection microframework for Python
====================================================================

*Dependency Injector* is a dependency injection microframework for Python. 
It was designed to be unified, developer-friendly tool that helps to implement 
dependency injection design pattern in formal, pretty, Pythonic way.

*Dependency Injector* framework key features are:

+ Easy, smart, pythonic style.
+ Obvious, clear structure.
+ Extensibility and flexibility.
+ High performance.
+ Memory efficiency.
+ Thread safety.
+ Documentation.
+ Semantic versioning.

*Dependency Injector* containers and providers are implemented as C extension 
types using Cython.

Status
------

+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://img.shields.io/pypi/v/dependency_injector.svg                                                   |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                                                      |
|                                       |    :alt: Latest Version                                                                                            |
|                                       | .. image:: https://img.shields.io/pypi/l/dependency_injector.svg                                                   |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                                                      |
|                                       |    :alt: License                                                                                                   |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg                                          |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                                                      |
|                                       |    :alt: Supported Python versions                                                                                 |
|                                       | .. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg                                      |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                                                      |
|                                       |    :alt: Supported Python implementations                                                                          |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| *Builds and tests coverage*           | .. image:: https://travis-ci.org/ets-labs/python-dependency-injector.svg?branch=master                             |
|                                       |    :target: https://travis-ci.org/ets-labs/python-dependency-injector                                              |
|                                       |    :alt: Build Status                                                                                              |
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

Dependency injection
--------------------

`Dependency injection`_ is a software design pattern that implements 
`Inversion of control`_ for resolving dependencies. Formally, if object **A** 
depends on object **B**, object **A** must not create or import object **B** 
directly. Instead of this object **A** must provide a way for *injecting* 
object **B**. The responsibilities of objects creation and dependencies 
injection are delegated to external code - the *dependency injector*. 

Popular terminology of dependency injection pattern:

+ Object **A**, that is dependant on object **B**, is often called - 
  the *client*.
+ Object **B**, that is a dependency, is often called - the *service*.
+ External code that is responsible for creation of objects and injection 
  of dependencies is often called - the *dependency injector*.

There are several ways of how *service* can be injected into the *client*: 

+ by passing it as ``__init__`` argument (constructor / initializer injection)
+ by setting it as attribute's value (attribute injection)
+ by passing it as method's argument (method injection)

Dependency injection pattern has few strict rules that should be followed:

+ The *client* delegates to the *dependency injector* the responsibility 
  of injecting its dependencies - the *service(s)*.
+ The *client* doesn't know how to create the *service*, it knows only 
  interface of the *service*. The *service* doesn't know that it is used by 
  the *client*.
+ The *dependency injector* knows how to create the *client* and 
  the *service*, it also knows that the *client* depends on the *service*, 
  and knows how to inject the *service* into the *client*.
+ The *client* and the *service* know nothing about the *dependency injector*.

Dependency injection pattern provides the following advantages: 

+ Control on application structure.
+ Decreased coupling between application components.
+ Increased code reusability.
+ Increased testability.
+ Increased maintainability.
+ Reconfiguration of system without rebuilding.

Example of dependency injection
-------------------------------

Let's go through next example:

.. image:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/engines_cars/diagram.png
    :width: 100%
    :align: center

Listing of ``example.engines`` module:

.. code-block:: python

    """Dependency injection example, engines module."""


    class Engine(object):
        """Example engine base class.

        Engine is a heart of every car. Engine is a very common term and could be
        implemented in very different ways.
        """


    class GasolineEngine(Engine):
        """Gasoline engine."""


    class DieselEngine(Engine):
        """Diesel engine."""


    class ElectroEngine(Engine):
        """Electro engine."""

Listing of ``example.cars`` module:

.. code-block:: python

    """Dependency injection example, cars module."""


    class Car(object):
        """Example car."""

        def __init__(self, engine):
            """Initializer."""
            self._engine = engine  # Engine is injected

Next example demonstrates creation of several cars with different engines:

.. code-block:: python

    """Dependency injection example, Cars & Engines."""

    import example.cars
    import example.engines


    if __name__ == '__main__':
        gasoline_car = example.cars.Car(example.engines.GasolineEngine())
        diesel_car = example.cars.Car(example.engines.DieselEngine())
        electro_car = example.cars.Car(example.engines.ElectroEngine())

While previous example demonstrates advantages of dependency injection, there 
is a disadvantage demonstration as well - creation of car requires additional 
code for specification of dependencies. Nevertheless, this disadvantage could 
be easily avoided by using a dependency injection framework for creation of 
inversion of control container (IoC container).

Example of creation of several inversion of control containers (IoC containers)
using *Dependency Injector*:

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

        electro = providers.Factory(example.engines.ElectroEngine)


    class Cars(containers.DeclarativeContainer):
        """IoC container of car providers."""

        gasoline = providers.Factory(example.cars.Car,
                                     engine=Engines.gasoline)

        diesel = providers.Factory(example.cars.Car,
                                   engine=Engines.diesel)

        electro = providers.Factory(example.cars.Car,
                                    engine=Engines.electro)


    if __name__ == '__main__':
        gasoline_car = Cars.gasoline()
        diesel_car = Cars.diesel()
        electro_car = Cars.electro()

Dependency Injector structure
-----------------------------

Dependency Injector is a microframework and has a very simple structure.

There are 2 main entities: providers & containers.

.. image:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/internals.png
    :width: 100%
    :align: center

Providers
~~~~~~~~~

Providers are strategies of accessing objects. They define how particular 
objects are provided.

- **Provider** - base provider class.
- **Callable** - provider that calls wrapped callable on every call. Supports 
  positional & keyword argument injections.
- **Factory** - provider that creates new instance of specified class on every 
  call. Supports positional & keyword argument injections, as well as 
  attribute injections.
- **Singleton** - provider that creates new instance of specified class on first 
  call and returns same instance on every next call. Supports positional & 
  keyword argument injections, as well as attribute injections.
- **Object** - provider that returns provided instance "as is".
- **ExternalDependency** - provider that can be useful for development of 
  self-sufficient libraries / modules / applications that has required 
  external dependencies.
- **Configuration** - provider that helps with implementing late static binding 
  of configuration options - use first, define later.

Containers
~~~~~~~~~~

Containers are collections of providers. Main purpose of containers is to 
group providers.

- **DeclarativeContainer** - is inversion of control container that could be 
  defined in declarative manner. It should cover most of the cases when list 
  of providers that would be included in container is deterministic 
  (container will not change its structure in runtime).
- **DynamicContainer** - is an inversion of control container with dynamic 
  structure. It should cover most of the cases when list of providers that 
  would be included in container is non-deterministic and depends on 
  application's flow or its configuration (container's structure could be 
  determined just after application will be started and will do some initial 
  work, like parsing list of container providers from the configuration).

Dependency Injector in action
-----------------------------

Brief example below is a simplified version of inversion of control 
containters from one of the real-life applications. This example demonstrates 
usage of *Dependency Injector* inversion of control containers & providers 
for specifying all application components and their dependencies beetween 
each other in one module. Besides other listed above advantages, it gives a 
great opportunity to control & manage application's structure in one place.

.. code-block:: python

    """Example of dependency injection in Python."""

    import logging
    import sqlite3

    import boto3

    import example.main
    import example.services

    import dependency_injector.containers as containers
    import dependency_injector.providers as providers


    class Core(containers.DeclarativeContainer):
        """IoC container of core component providers."""

        config = providers.Configuration('config')

        logger = providers.Singleton(logging.Logger, name='example')


    class Gateways(containers.DeclarativeContainer):
        """IoC container of gateway (API clients to remote services) providers."""

        database = providers.Singleton(sqlite3.connect, Core.config.database.dsn)

        s3 = providers.Singleton(
            boto3.client, 's3',
            aws_access_key_id=Core.config.aws.access_key_id,
            aws_secret_access_key=Core.config.aws.secret_access_key)


    class Services(containers.DeclarativeContainer):
        """IoC container of business service providers."""

        users = providers.Factory(example.services.UsersService,
                                  db=Gateways.database,
                                  logger=Core.logger)

        auth = providers.Factory(example.services.AuthService,
                                 db=Gateways.database,
                                 logger=Core.logger,
                                 token_ttl=Core.config.auth.token_ttl)

        photos = providers.Factory(example.services.PhotosService,
                                   db=Gateways.database,
                                   s3=Gateways.s3,
                                   logger=Core.logger)


    class Application(containers.DeclarativeContainer):
        """IoC container of application component providers."""

        main = providers.Callable(example.main.main,
                                  users_service=Services.users,
                                  auth_service=Services.auth,
                                  photos_service=Services.photos)

Next example demonstrates run of example application defined above:

.. code-block:: python

    """Run example application."""

    import sys
    import logging

    from containers import Core, Application


    if __name__ == '__main__':
        # Configure platform:
        Core.config.update({'database': {'dsn': ':memory:'},
                            'aws': {'access_key_id': 'KEY',
                                    'secret_access_key': 'SECRET'},
                            'auth': {'token_ttl': 3600}})
        Core.logger().addHandler(logging.StreamHandler(sys.stdout))

        # Run application:
        Application.main(uid=sys.argv[1],
                         password=sys.argv[2],
                         photo=sys.argv[3])

You can get more *Dependency Injector* examples in ``/examples`` directory on
GitHub:

    https://github.com/ets-labs/python-dependency-injector

Installation
------------

*Dependency Injector* library is available on `PyPi`_::

    pip install dependency_injector

Documentation
-------------

*Dependency Injector* documentation is hosted on ReadTheDocs:

- `User's guide`_ 
- `API docs`_

Feedback & Support
------------------

Feel free to post questions, bugs, feature requests, proposals etc. on
*Dependency Injector*  GitHub Issues:

    https://github.com/ets-labs/python-dependency-injector/issues

Your feedback is quite important!


.. _Dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
.. _Inversion of control: https://en.wikipedia.org/wiki/Inversion_of_control
.. _PyPi: https://pypi.python.org/pypi/dependency_injector
.. _User's guide: http://python-dependency-injector.ets-labs.org/
.. _API docs: http://python-dependency-injector.ets-labs.org/api/
