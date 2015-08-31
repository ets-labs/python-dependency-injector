Introduction
============

Before you have started with *Dependency Injector* framework and dependecy 
injection, there are a couple of introduction notes that might be useful.

What is DI and why is it needed?
--------------------------------

Python ecosystem consists of a big amount of various libraries that contain
different classes and functions that could be used for applications
development. Each of them has its own role.

Modern Python applications are mostly the composition of well-known open
source systems / frameworks / libraries and some turnkey functionality.

When application goes bigger, its complexity and SLOC_ are also increased.
Being driven by SOLID_ (for example), developers often start to split
application's sources into not so big classes, functions and modules, that are
less complex, could be reused several times and so on... It always helps, but 
there is another problem on the horizon.

The name of this problem is - "Dependency hell!". It sounds like "I have so
many classes and functions! They are great, now I can understand each of them,
but it is so hard to see the whole picture! How are they linked with each 
other? What dependencies does this class have?". And this is a key question:
"What dependencies does certain class / function have?". To resolve this issues 
developers have to go inside with IoC_ principles and implementation patterns.

One of such IoC_ implementation patterns is called `dependency injection`_.

Dependency injection in Python
------------------------------

Interesting but, dependency injection is not very popular topic in Python. 
The things are so because Python is an awesome language. Your eyes are opened
and your hands are free while you are using Python. In practice this means that
you can do dependency injection in Python in quite an easy way because language
itself helps you to do this. At the same time, even the thins are so, you still
have to do some work. Another one 'minor' problem is that there are several 
ways to do dependency injection container.

Key features
------------

*Dependency Injector* is a dependency injection framework for Python projects. 
It was designed to be unified, developer's friendly tool for managing any kind
of Python objects and their dependencies in formal, pretty way.

Below is a list of some key features and points of *Dependency Injector*
framework:

- Easy, smart, pythonic style.
- Obvious, clear structure.
- Memory efficiency.
- Semantic versioning.

Main idea of *Dependency Injector* is to keep dependencies under control.

Main entities
-------------

Current section describes *Dependency Injector* main entities and their 
interaction with each other.

.. image:: /images/internals.png
    :width: 100%
    :align: center

There are 3 main entities:

- Providers. Providers are strategies of accesing objects. For example, 
  ``dependency_injector.providers.Factory`` creates new instance of provided 
  class every time it is called. ``dependency_injector.providers.Singleton`` 
  creates provided instance once and returns it on every next call. Providers 
  could be overridden by another providers. Base class is - 
  ``dependency_injector.providers.Provider``.
- Injections. Injections are instructions for making dependency injections 
  (there are several ways how they could be done). Injections are used mostly
  by ``dependency_injector.providers.Factory`` and 
  ``dependency_injector.providers.Singleton`` providers, but these are not only 
  cases. Base class is - 
  ``dependency_injector.injections.Injection``.
- Catalogs. Catalogs are collections of providers. They are used for grouping 
  of providers by some principles. Base class is - 
  ``dependency_injector.catalog.AbstractCatalog``.


.. _SLOC: http://en.wikipedia.org/wiki/Source_lines_of_code
.. _SOLID: http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29
.. _IoC: http://en.wikipedia.org/wiki/Inversion_of_control
.. _dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
