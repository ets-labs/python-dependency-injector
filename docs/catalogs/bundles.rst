Catalog provider bundles
------------------------

.. currentmodule:: dependency_injector.catalogs

:py:class:`CatalogBundle` is a frozen, limited collection of catalog 
providers. While catalog could be used as a centralized place for 
particular providers group, such bundles of catalog providers can be used 
for creating several frozen, limited scopes that could be passed to different 
subsystems.

:py:class:`CatalogBundle` has API's parity with catalogs
(:py:class:`DeclarativeCatalog` or :py:class:`DynamicCatalog`) in terms of 
retrieving the providers, but it is "frozen" in terms of modification 
provider's list.

:py:class:`CatalogBundle` is considered to be dependable on catalogs 
(:py:class:`DeclarativeCatalog` or :py:class:`DynamicCatalog`) entity by 
its design.

Each catalog (:py:class:`DeclarativeCatalog` or :py:class:`DynamicCatalog`) 
has a reference to its bundle class - :py:attr:`DeclarativeCatalog.Bundle` 
(or :py:attr:`DynamicCatalog.Bundle` consequently). For example, subclass of 
:py:class:`CatalogBundle` for some concrete declarative catalog 
``SomeCatalog`` could be reached as ``SomeCatalog.Bundle``. 

:py:class:`CatalogBundle` expects to get the list of its catalog providers
as positional arguments and will limit the scope of created bundle to this 
list. 

.. note:: 
   
    Some notes about :py:class:`CatalogBundle` design.

    Design and syntax of :py:class:`CatalogBundle` was developed with the idea 
    of keeping full functionalities of type-hinting and introspection of 
    modern IDE's. This design came from some practical experience of using 
    :py:class:`CatalogBundle` and considered to be the most comfortable for 
    developer.

Example:

.. image:: /images/catalogs/bundles.png
    :width: 100%
    :align: center

Listing of `services.py`:

.. literalinclude:: ../../examples/catalogs/bundles/services.py
   :language: python

Listing of `views.py`:

.. literalinclude:: ../../examples/catalogs/bundles/views.py
   :language: python

Listing of `catalogs.py`:

.. literalinclude:: ../../examples/catalogs/bundles/catalogs.py
   :language: python
