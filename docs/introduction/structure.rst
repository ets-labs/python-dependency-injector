Structure of Dependency Injector
--------------------------------

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control
   :description: This article describes "Dependency Injector" framework 
                 components and their interaction between each other. 
                 Catalogs, providers and injections are the former 
                 components of the framework.

Current section describes *Dependency Injector* main entities and their 
interaction between each other.

.. image:: /images/internals.png
    :width: 100%
    :align: center

There are 3 main entities: providers, injections and catalogs.

+ All of the entities could be used in composition with each other or 
  separatelly.
+ Each of the entities could be extended via specialization.

Providers
~~~~~~~~~

Providers are strategies of accessing objects. For example, 
:py:class:`dependency_injector.providers.Factory` creates new instance 
of provided class every time it is called. 
:py:class:`dependency_injector.providers.Singleton` creates provided 
instance once and returns it on every next call. Providers could be 
injected into each other. Providers could be overridden by another 
providers. Base class is - 
:py:class:`dependency_injector.providers.Provider`.

Injections
~~~~~~~~~~

Injections are instructions for making dependency injections 
(there are several ways how they could be done). Injections are used 
mostly by :py:class:`dependency_injector.providers.Factory` and 
:py:class:`dependency_injector.providers.Singleton` providers, but 
these are not only cases. Base class is - 
:py:class:`dependency_injector.injections.Injection`.

Catalogs 
~~~~~~~~~

Catalogs are collections of providers. They are used for grouping 
of providers by some principles. Base class is - 
:py:class:`dependency_injector.catalogs.DeclarativeCatalog`.
