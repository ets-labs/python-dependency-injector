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

Providers package API docs - :py:mod:`dependency_injector.providers`

..  toctree::
    :maxdepth: 2

    factory
    singleton
    callable
    coroutine
    object
    list
    dependency
    overriding
    custom
