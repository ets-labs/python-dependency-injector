Structure of Dependency Injector
--------------------------------

Current section describes *Dependency Injector* main entities and their 
interaction between each other.

.. image:: /images/internals.png
    :width: 100%
    :align: center

There are 3 main entities:

.. glossary::

    Providers
        Providers are strategies of accesing objects. For example, 
        :py:class:`dependency_injector.providers.Factory` creates new instance 
        of provided class every time it is called. 
        :py:class:`dependency_injector.providers.Singleton` creates provided 
        instance once and returns it on every next call. Providers could be 
        injected into each other. Providers could be overridden by another 
        providers. Base class is - 
        :py:class:`dependency_injector.providers.Provider`.

    Injections
        Injections are instructions for making dependency injections 
        (there are several ways how they could be done). Injections are used 
        mostly by :py:class:`dependency_injector.providers.Factory` and 
        :py:class:`dependency_injector.providers.Singleton` providers, but 
        these are not only cases. Base class is - 
        :py:class:`dependency_injector.injections.Injection`.

    Catalogs 
        Catalogs are collections of providers. They are used for grouping 
        of providers by some principles. Base class is - 
        :py:class:`dependency_injector.catalogs.DeclarativeCatalog`.

Some general principles about *Dependency Injector* entities:

+ All of the entities could be used in composition with each other or 
  separatelly.
+ Each of the entities could be extended via specialization.
