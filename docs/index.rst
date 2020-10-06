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

.. image:: https://travis-ci.org/ets-labs/python-dependency-injector.svg?branch=master
   :target: https://travis-ci.org/ets-labs/python-dependency-injector
   :alt: Build Status

.. image:: http://readthedocs.org/projects/python-dependency-injector/badge/?version=latest
   :target: http://python-dependency-injector.ets-labs.org/
   :alt: Docs Status

.. image:: https://coveralls.io/repos/github/ets-labs/python-dependency-injector/badge.svg?branch=master
   :target: https://coveralls.io/github/ets-labs/python-dependency-injector?branch=master
   :alt: Coverage Status

``Dependency Injector`` is a dependency injection framework for Python.

It helps implementing the dependency injection principle.

Key features of the ``Dependency Injector``:

- **Providers**. Provides ``Factory``, ``Singleton``, ``Callable``, ``Coroutine``, ``Object``,
  ``List``, ``Configuration``, ``Dependency`` and ``Selector`` providers that help assembling your
  objects. See :ref:`providers`.
- **Overriding**. Can override any provider by another provider on the fly. This helps in testing
  and configuring dev / stage environment to replace API clients with stubs etc. See
  :ref:`provider-overriding`.
- **Configuration**. Read configuration from ``yaml`` & ``ini`` files, environment variables
  and dictionaries. See :ref:`configuration-provider`.
- **Containers**. Provides declarative and dynamic containers. See :ref:`containers`.
- **Wiring**. Injects container providers into functions and methods. Helps integrating with
  other frameworks: Django, Flask, Aiohttp, etc. See :ref:`wiring`.
- **Typing**. Provides typing stubs, ``mypy``-friendly. See :ref:`provider-typing`.
- **Performance**. Fast. Written in ``Cython``.
- **Maturity**. Mature and production-ready. Well-tested, documented and supported.

.. code-block:: python

    from dependency_injector import containers, providers
    from dependency_injector.wiring import Provide


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


    def main(service: Service = Provide[Container.service]):
        ...


    if __name__ == '__main__':
        container = Container()
        container.config.api_key.from_env('API_KEY')
        container.config.timeout.from_env('TIMEOUT')
        container.wire(modules=[sys.modules[__name__]])

        main()

With the ``Dependency Injector`` you explicitly define and inject the dependencies.
This makes easier to understand and change how application works.

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
