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
  :py:class:`dependency_injector.providers.Factory` creates new instance of 
  provided class every time it is called. 
  :py:class:`dependency_injector.providers.Singleton` creates provided 
  instance once and returns it on every next call. Providers could be 
  overridden by another providers. Base class is - 
  :py:class:`dependency_injector.providers.Provider`.
- Injections. Injections are instructions for making dependency injections 
  (there are several ways how they could be done). Injections are used mostly
  by :py:class:`dependency_injector.providers.Factory` and 
  :py:class:`dependency_injector.providers.Singleton` providers, but 
  these are not only cases. Base class is - 
  :py:class:`dependency_injector.injections.Injection`.
- Catalogs. Catalogs are collections of providers. They are used for grouping 
  of providers by some principles. Base class is - 
  :py:class:`dependency_injector.catalogs.DeclarativeCatalog`.
