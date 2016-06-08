Providers
=========

Providers are strategies of accessing objects. They define how particular 
objects are provided.

Every provider is callable (implements ``__call__()``). Every call to provider 
instance returns provided result, according to the providing strategy of 
particular provider. 

Current documentation section consists from description of standard providers
library and some useful information like overriding of providers and writing 
of custom providers.

All providers are validated in multithreading environment and considered to 
be thread safe.

+ Base providers class is: :py:class:`dependency_injector.providers.Provider`
+ Providers module API docs: :py:mod:`dependency_injector.providers`
+ Providers class diagram:

.. image:: /images/providers/providers_class_diagram.png
    :width: 100%
    :align: center

..  toctree::
    :maxdepth: 2

    factory
    singleton
    callable
    external_dependency
    static
    overriding
    custom
