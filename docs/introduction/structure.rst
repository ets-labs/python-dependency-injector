Structure of Dependency Injector
--------------------------------

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control
   :description: This article describes "Dependency Injector" framework 
                 components and their interaction between each other. 
                 Providers and containers are the former components of 
                 the framework.

Current section describes *Dependency Injector* main entities and their 
interaction between each other.

.. image:: /images/internals.png
    :width: 100%
    :align: center

There are 3 main entities: providers, containers.

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

Providers could be:

+ Injected into each other.
+ Overridden by each other.
+ Extended.

Containers 
~~~~~~~~~~

Containers are collections of providers. They are used for grouping 
of providers by some principles. Base class is - 
:py:class:`dependency_injector.containers.DeclarativeContainer`.

Containers could be:

+ Overridden by each other.
+ Copied from each other.
+ Extended.
