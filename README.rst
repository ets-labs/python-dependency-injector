===========================================================
Dependency Injector - Python dependency injection framework
===========================================================

*Dependency Injector* is a Python dependency injection framework. It was 
designed to be unified, developer-friendly tool that helps to implement 
dependency injection pattern in formal, pretty, Pythonic way.

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

*Dependency Injector* library is available on `PyPi`_::

    pip install dependency_injector

Dependency Injection
--------------------

`Dependency injection`_ is a software design pattern that implements 
`Inversion of control`_ for resolving dependencies. Formally, if object **A** 
depends on object **B**, object **A** must not create or import object **B**, 
but provide a way for injecting object **B** (object **B** could be injected 
into object **A**  in several ways: by passing it as ``__init__`` argument, by 
setting it as attribute's value or by passing it as method's argument). 

Dependency injection pattern has few strict rules that should be followed:

+ Object **A** (the client) delegates to external code (the dependency 
  injector) the responsibility of providing its dependencies - object **B** 
  (the service).
+ The client doesn't know how to create the service, it knows only interface 
  of service.
+ The service doesn't know that it is used by the client.
+ The dependency injector knows how to create the client.
+ The dependency injector knows how to create the service.
+ The dependency injector knows that the client depends on the service.
+ The dependency injector knows how to inject the service into the client.
+ The client knows nothing about the dependency injector.
+ The service knows nothing about the dependency injector.

Next two examples demonstrate refactoring of a small piece of code to 
dependency injection pattern:

.. code-block:: python

    """Car & Engine example."""


    class Engine(object):
        """Example engine."""


    class Car(object):
        """Example car."""

        def __init__(self):
            """Initializer."""
            self.engine = Engine()  # Engine is a "hardcoded" dependency


    if __name__ == '__main__':
        car = Car()  # Application creates Car's instance

``Car`` **creates** an ``Engine`` during its creation. Really? Does it make 
more sense than creating an ``Engine`` separately and then 
**inject it into** ``Car`` when ``Car`` is being created? Looks more 
realistic, right?

.. code-block:: python

    """Refactored Car & Engine example that demonstrates dependency injection."""


    class Engine(object):
        """Example engine."""


    class Car(object):
        """Example car."""

        def __init__(self, engine):
            """Initializer."""
            self.engine = engine  # Engine is an "injected" dependency


    if __name__ == '__main__':
        engine = Engine()  # Application creates Engine's instance
        car = Car(engine)  # and inject it into the Car's instance

Advantages of dependency injection
----------------------------------

Dependency injection pattern provides next advantages: 

+ Control on application structure.
+ Decreased coupling between application components.
+ Increased code reusability.
+ Increased testability.
+ Increased maintainability.
+ Reconfiguration of system without rebuilding.

Example of dependency injection
-------------------------------

Brief example below demonstrates usage of *Dependency Injector* for creating 
several IoC containers for some microservice system:

.. code-block:: python

    """Example of dependency injection in Python."""

    import logging
    import sqlite3

    import boto.s3.connection

    import example.main
    import example.services

    import dependency_injector.containers as containers
    import dependency_injector.providers as providers


    class Platform(containers.DeclarativeContainer):
        """IoC container of platform service providers."""

        logger = providers.Singleton(logging.Logger, name='example')

        database = providers.Singleton(sqlite3.connect, ':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection,
                                 aws_access_key_id='KEY',
                                 aws_secret_access_key='SECRET')


    class Services(containers.DeclarativeContainer):
        """IoC container of business service providers."""

        users = providers.Factory(example.services.Users,
                                  logger=Platform.logger,
                                  db=Platform.database)

        auth = providers.Factory(example.services.Auth,
                                 logger=Platform.logger,
                                 db=Platform.database,
                                 token_ttl=3600)

        photos = providers.Factory(example.services.Photos,
                                   logger=Platform.logger,
                                   db=Platform.database,
                                   s3=Platform.s3)


    class Application(containers.DeclarativeContainer):
        """IoC container of application component providers."""

        main = providers.Callable(example.main.main,
                                  users_service=Services.users,
                                  auth_service=Services.auth,
                                  photos_service=Services.photos)

Next example demonstrates run of dependency injection example application 
defined above:

.. code-block:: python

    """Run dependency injection example application.

    Instructions for running:

        python run.py 1 secret photo.jpg
    """

    import sys
    import logging

    from containers import Platform, Application


    if __name__ == '__main__':
        # Configure platform logger:
        Platform.logger().addHandler(logging.StreamHandler(sys.stdout))

        # Run application:
        Application.main(uid=sys.argv[1],
                         password=sys.argv[2],
                         photo=sys.argv[3])

        # Previous call is an equivalent of next operations:
        #
        # logger = logging.Logger(name='example')
        # database = sqlite3.connect(':memory:')
        # s3 = boto.s3.connection.S3Connection(aws_access_key_id='KEY',
        #                                      aws_secret_access_key='SECRET')
        #
        # example.main.main(uid=sys.argv[1],
        #                   password=sys.argv[2],
        #                   photo=sys.argv[3],
        #                   users_service=example.services.Users(logger=logger,
        #                                                        db=database),
        #                   auth_service=example.services.Auth(logger=logger,
        #                                                      db=database,
        #                                                      token_ttl=3600),
        #                   photos_service=example.services.Photos(logger=logger,
        #                                                          db=database,
        #                                                          s3=s3))
        #
        # Output:
        #
        # User 1 has been found in database
        # User 1 has been successfully authenticated
        # Photo photo.jpg has been successfully uploaded by user 1
   
Alternative definition styles of providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Dependecy Injector* supports few other styles of dependency injections 
definition.

IoC containers from previous example could look like these:

.. code-block:: python

    class Platform(containers.DeclarativeContainer):
        """IoC container of platform service providers."""

        logger = providers.Singleton(logging.Logger) \
            .add_kwargs(name='example')

        database = providers.Singleton(sqlite3.connect) \
            .add_args(':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection) \
            .add_kwargs(aws_access_key_id='KEY',
                        aws_secret_access_key='SECRET')

or like this these:

.. code-block:: python

    class Platform(containers.DeclarativeContainer):
        """IoC container of platform service providers."""

        logger = providers.Singleton(logging.Logger)
        logger.add_kwargs(name='example')

        database = providers.Singleton(sqlite3.connect)
        database.add_args(':memory:')

        s3 = providers.Singleton(boto.s3.connection.S3Connection)
        s3.add_kwargs(aws_access_key_id='KEY',
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


.. _Dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
.. _Inversion of control: https://en.wikipedia.org/wiki/Inversion_of_control
.. _PyPi: https://pypi.python.org/pypi/dependency_injector
.. _User's guide: http://python-dependency-injector.ets-labs.org/en/stable/
.. _API docs: http://python-dependency-injector.ets-labs.org/en/stable/api/
