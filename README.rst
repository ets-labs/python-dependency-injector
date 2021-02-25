.. figure:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/logo.svg
   :target: https://github.com/ets-labs/python-dependency-injector

| 

.. image:: https://img.shields.io/pypi/v/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Latest Version
   
.. image:: https://img.shields.io/pypi/l/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: License

.. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Supported Python versions
   
.. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Supported Python implementations

.. image:: https://pepy.tech/badge/dependency-injector
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://pepy.tech/badge/dependency-injector/month
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://pepy.tech/badge/dependency-injector/week
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://img.shields.io/pypi/wheel/dependency-injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Wheel

.. image:: https://img.shields.io/github/workflow/status/ets-labs/python-dependency-injector/Tests%20and%20linters/master
   :target: https://github.com/ets-labs/python-dependency-injector/actions
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/ets-labs/python-dependency-injector/badge.svg?branch=master
   :target: https://coveralls.io/github/ets-labs/python-dependency-injector?branch=master
   :alt: Coverage Status

What is ``Dependency Injector``?
================================

``Dependency Injector`` is a dependency injection framework for Python.

It helps implementing the dependency injection principle.

Key features of the ``Dependency Injector``:

- **Providers**. Provides ``Factory``, ``Singleton``, ``Callable``, ``Coroutine``, ``Object``,
  ``List``, ``Dict``, ``Configuration``, ``Resource``, ``Dependency`` and ``Selector`` providers
  that help assembling your objects.
  See `Providers <https://python-dependency-injector.ets-labs.org/providers/index.html>`_.
- **Overriding**. Can override any provider by another provider on the fly. This helps in testing
  and configuring dev / stage environment to replace API clients with stubs etc. See
  `Provider overriding <https://python-dependency-injector.ets-labs.org/providers/overriding.html>`_.
- **Configuration**. Reads configuration from ``yaml`` & ``ini`` files, ``pydantic`` settings,
  environment variables, and dictionaries.
  See `Configuration provider <https://python-dependency-injector.ets-labs.org/providers/configuration.html>`_.
- **Containers**. Provides declarative and dynamic containers.
  See `Containers <https://python-dependency-injector.ets-labs.org/containers/index.html>`_.
- **Resources**. Helps with initialization and configuring of logging, event loop, thread
  or process pool, etc. Can be used for per-function execution scope in tandem with wiring.
  See `Resource provider <https://python-dependency-injector.ets-labs.org/providers/resource.html>`_.
- **Wiring**. Injects dependencies into functions and methods. Helps integrating with
  other frameworks: Django, Flask, Aiohttp, Sanic, FastAPI, etc.
  See `Wiring <https://python-dependency-injector.ets-labs.org/wiring.html>`_.
- **Asynchronous**. Supports asynchronous injections.
  See `Asynchronous injections <https://python-dependency-injector.ets-labs.org/providers/async.html>`_.
- **Typing**. Provides typing stubs, ``mypy``-friendly.
  See `Typing and mypy <https://python-dependency-injector.ets-labs.org/providers/typing_mypy.html>`_.
- **Performance**. Fast. Written in ``Cython``.
- **Maturity**. Mature and production-ready. Well-tested, documented and supported.

.. code-block:: python

   from dependency_injector import containers, providers
   from dependency_injector.wiring import inject, Provide


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration()

       api_client = providers.Singleton(
           ApiClient,
           api_key=config.api_key,
           timeout=config.timeout.as_int(),
       )

       service = providers.Factory(
           Service,
           api_client=api_client,
       )


   @inject
   def main(service: Service = Provide[Container.service]):
       ...


   if __name__ == '__main__':
       container = Container()
       container.config.api_key.from_env('API_KEY')
       container.config.timeout.from_env('TIMEOUT')
       container.wire(modules=[sys.modules[__name__]])

       main()  # <-- dependency is injected automatically

       with container.api_client.override(mock.Mock()):
           main()  # <-- overridden dependency is injected automatically

When you call ``main()`` function the ``Service`` dependency is assembled and injected automatically.

When doing a testing you call the ``container.api_client.override()`` to replace the real API
client with a mock. When you call ``main()`` the mock is injected.

You can override any provider with another provider.

It also helps you in configuring project for the different environments: replace an API client
with a stub on the dev or stage.

With the ``Dependency Injector`` objects assembling is consolidated in the container.
Dependency injections are defined explicitly.
This makes easier to understand and change how application works.

.. figure:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/di-readme.svg
   :target: https://github.com/ets-labs/python-dependency-injector

Visit the docs to know more about the
`Dependency injection and inversion of control in Python <https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html>`_.

Installation
------------

The package is available on the `PyPi`_::

    pip install dependency-injector

Documentation
-------------

The documentation is available `here <https://python-dependency-injector.ets-labs.org/>`_.

Examples
--------

Choose one of the following:

- `Application example (single container) <https://python-dependency-injector.ets-labs.org/examples/application-single-container.html>`_
- `Application example (multiple containers) <https://python-dependency-injector.ets-labs.org/examples/application-multiple-containers.html>`_
- `Decoupled packages example (multiple containers) <https://python-dependency-injector.ets-labs.org/examples/decoupled-packages.html>`_
- `Boto3 example <https://python-dependency-injector.ets-labs.org/examples/boto3.html>`_
- `Django example <https://python-dependency-injector.ets-labs.org/examples/django.html>`_
- `Flask example <https://python-dependency-injector.ets-labs.org/examples/flask.html>`_
- `Aiohttp example <https://python-dependency-injector.ets-labs.org/examples/aiohttp.html>`_
- `Sanic example <https://python-dependency-injector.ets-labs.org/examples/sanic.html>`_
- `FastAPI example <https://python-dependency-injector.ets-labs.org/examples/fastapi.html>`_
- `FastAPI + Redis example <https://python-dependency-injector.ets-labs.org/examples/fastapi-redis.html>`_
- `FastAPI + SQLAlchemy example <https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html>`_

Tutorials
---------

Choose one of the following:

- `Flask web application tutorial <https://python-dependency-injector.ets-labs.org/tutorials/flask.html>`_
- `Aiohttp REST API tutorial <https://python-dependency-injector.ets-labs.org/tutorials/aiohttp.html>`_
- `Asyncio monitoring daemon tutorial <https://python-dependency-injector.ets-labs.org/tutorials/asyncio-daemon.html>`_
- `CLI application tutorial <https://python-dependency-injector.ets-labs.org/tutorials/cli.html>`_

Concept
-------

The framework stands on the `PEP20 (The Zen of Python) <https://www.python.org/dev/peps/pep-0020/>`_ principle:

.. code-block:: bash

   Explicit is better than implicit

You need to specify how to assemble and where to inject the dependencies explicitly.

The power of the framework is in a simplicity.
``Dependency Injector`` is a simple tool for the powerful concept.

Frequently asked questions
--------------------------

What is the dependency injection?
 - dependency injection is a principle that decreases coupling and increases cohesion

Why should I do the dependency injection?
 - your code becomes more flexible, testable and clear 😎

How do I start doing the dependency injection?
 - you start writing the code following the dependency injection principle
 - you register all of your application components and their dependencies in the container
 - when you need a component, you specify where to inject it or get it from the container

What price do I pay and what do I get?
 - you need to explicitly specify the dependencies
 - it will be extra work in the beginning
 - it will payoff as the project grows

Have a question?
 - Open a `Github Issue <https://github.com/ets-labs/python-dependency-injector/issues>`_

Found a bug?
 - Open a `Github Issue <https://github.com/ets-labs/python-dependency-injector/issues>`_

Want to help?
 - |star| Star the ``Dependency Injector`` on the `Github <https://github.com/ets-labs/python-dependency-injector/>`_
 - |new| Start a new project with the ``Dependency Injector``
 - |tell| Tell your friend about the ``Dependency Injector``

Want to contribute?
 - |fork| Fork the project
 - |pull| Open a pull request to the ``develop`` branch

.. _PyPi: https://pypi.org/project/dependency-injector/

.. |star| unicode:: U+2B50 U+FE0F .. star sign1
.. |new| unicode:: U+1F195 .. new sign
.. |tell| unicode:: U+1F4AC .. tell sign
.. |fork| unicode:: U+1F500 .. fork sign
.. |pull| unicode:: U+2B05 U+FE0F .. pull sign
