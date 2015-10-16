Creating catalog provider bundles
---------------------------------

``di.AbstractCatalog.Bundle`` is a limited collection of catalog providers. 
While catalog could be used as a centralized place for particular providers 
group, such bundles of catalog providers can be used for creating several 
limited scopes that could be passed to different subsystems.

``di.AbstractCatalog.Bundle`` has exactly the same API as 
``di.AbstractCatalog`` except of the limitations on getting providers.

Each ``di.AbstractCatalog`` has a reference to its bundle class - 
``di.AbstractCatalog.Bundle``. For example, if some concrete catalog has name 
``SomeCatalog``, then its bundle class could be reached as 
``SomeCatalog.Bundle``. 

``di.AbstractCatalog.Bundle`` expects to get the list of its catalog providers
as positional arguments and will limit the scope of created bundle to this 
list. 

Example:

.. image:: /images/catalogs/bundles.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/catalogs/bundles.py
   :language: python
