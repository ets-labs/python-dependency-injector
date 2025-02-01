=================================================================
Dependency Injector --- Dependency injection framework for Python
=================================================================

.. meta::
   :google-site-verification: V1hlKfpgL3AARAElwFcqP4qW1Smsx5bKSRU8O86i20Y
   :keywords: Python,Dependency injection,DI,Inversion of Control,IoC,
              IoC Container,Factory, Singleton, Design Patterns
   :description: Dependency Injector is a dependency injection framework
                 for Python. It helps to maintain you application structure.
                 It was designed to be unified, developer-friendly
                 tool that helps to implement dependency injection design
                 pattern in formal, pretty, Pythonic way. Dependency Injector
                 provides implementations of such popular design patterns
                 like IoC container, Factory and Singleton. Dependency
                 Injector providers are implemented as C extension types
                 using Cython.

.. _index:

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

.. image:: https://static.pepy.tech/badge/dependency-injector
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://static.pepy.tech/badge/dependency-injector/month
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://static.pepy.tech/badge/dependency-injector/week
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://img.shields.io/pypi/wheel/dependency-injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Wheel

.. image:: https://img.shields.io/github/actions/workflow/status/ets-labs/python-dependency-injector/tests-and-linters.yml?branch=master
   :target: https://github.com/ets-labs/python-dependency-injector/actions
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/ets-labs/python-dependency-injector/badge.svg?branch=master
   :target: https://coveralls.io/github/ets-labs/python-dependency-injector?branch=master
   :alt: Coverage Status

``Dependency Injector`` is a dependency injection framework for Python.

It helps implementing the dependency injection principle.

Key features of the ``Dependency Injector``:

- **Providers**. Provides ``Factory``, ``Singleton``, ``Callable``, ``Coroutine``, ``Object``,
  ``List``, ``Dict``, ``Configuration``, ``Resource``, ``Dependency``, and ``Selector`` providers
  that help assemble your objects. See :ref:`providers`.
- **Overriding**. Can override any provider by another provider on the fly. This helps in testing
  and configuring dev/stage environment to replace API clients with stubs etc. See
  :ref:`provider-overriding`.
- **Configuration**. Reads configuration from ``yaml``, ``ini``, and ``json`` files, ``pydantic`` settings,
  environment variables, and dictionaries. See :ref:`configuration-provider`.
- **Resources**. Helps with initialization and configuring of logging, event loop, thread
  or process pool, etc. Can be used for per-function execution scope in tandem with wiring.
  See :ref:`resource-provider`.
- **Containers**. Provides declarative and dynamic containers. See :ref:`containers`.
- **Wiring**. Injects dependencies into functions and methods. Helps integrate with
  other frameworks: Django, Flask, Aiohttp, Sanic, FastAPI, etc. See :ref:`wiring`.
- **Asynchronous**. Supports asynchronous injections. See :ref:`async-injections`.
- **Typing**. Provides typing stubs, ``mypy``-friendly. See :ref:`provider-typing`.
- **Performance**. Fast. Written in ``Cython``.
- **Maturity**. Mature and production-ready. Well-tested, documented, and supported.

.. code-block:: python

   from dependency_injector import containers, providers
   from dependency_injector.wiring import Provide, inject


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration()

       api_client = providers.Singleton(
           ApiClient,
           api_key=config.api_key,
           timeout=config.timeout,
       )

       service = providers.Factory(
           Service,
           api_client=api_client,
       )


   @inject
   def main(service: Service = Provide[Container.service]) -> None:
       ...


   if __name__ == "__main__":
       container = Container()
       container.config.api_key.from_env("API_KEY", required=True)
       container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
       container.wire(modules=[__name__])

       main()  # <-- dependency is injected automatically

       with container.api_client.override(mock.Mock()):
           main()  # <-- overridden dependency is injected automatically

With the ``Dependency Injector``, object assembling is consolidated in the container.
Dependency injections are defined explicitly.
This makes it easier to understand and change how the application works.

.. figure:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/di-readme.svg
   :target: https://github.com/ets-labs/python-dependency-injector

Explore the documentation to know more about the ``Dependency Injector``.

.. _contents:

Contents
--------

.. toctree::
   :maxdepth: 2

   introduction/index
   examples/index
   tutorials/index
   providers/index
   containers/index
   wiring
   examples-other/index
   api/index
   main/feedback
   main/changelog
