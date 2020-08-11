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

It stands on two principles:

- Explicit is better than implicit (PEP20).
- Do no magic to your code.

How does it different from the other frameworks?

- **No autowiring.** The framework does NOT do any autowiring / autoresolving of the dependencies. You need to specify everything explicitly. Because *"Explicit is better than implicit" (PEP20)*.
- **Does not pollute your code.** Your application does NOT know and does NOT depend on the framework. No ``@inject`` decorators, annotations, patching or any other magic tricks.

``Dependency Injector`` makes a simple contract with you:

- You tell the framework how to build you code
- The framework does it for you

The power of the ``Dependency Injector`` is in its simplicity and straightforwardness. It is a simple tool for the powerful concept.

With the ``Dependency Injector`` you keep **application structure in one place**.
This place is called **the container**. You use the container to manage all the components of the
application. All the component dependencies are defined explicitly. This provides the control on
the application structure. It is **easy to understand and change** it.

.. figure:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/di-map.svg
   :target: https://github.com/ets-labs/python-dependency-injector

*The container is like a map of your application. You always know what depends on what.*

Explore the documentation to know more about the ``Dependency Injector``.

.. _contents:

Contents
--------

..  toctree::
    :maxdepth: 2

    introduction/index
    main/installation
    tutorials/index
    providers/index
    containers/index
    examples/index
    api/index
    main/feedback
    main/changelog
