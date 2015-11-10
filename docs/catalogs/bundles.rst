Creating catalog provider bundles
---------------------------------

``di.DeclarativeCatalog.Bundle`` is a limited collection of catalog providers. 
While catalog could be used as a centralized place for particular providers 
group, such bundles of catalog providers can be used for creating several 
limited scopes that could be passed to different subsystems.

``di.DeclarativeCatalog.Bundle`` has exactly the same API as 
``di.DeclarativeCatalog`` except of the limitations on getting providers.

Each ``di.DeclarativeCatalog`` has a reference to its bundle class - 
``di.DeclarativeCatalog.Bundle``. For example, if some concrete catalog has name 
``SomeCatalog``, then its bundle class could be reached as 
``SomeCatalog.Bundle``. 

``di.DeclarativeCatalog.Bundle`` expects to get the list of its catalog providers
as positional arguments and will limit the scope of created bundle to this 
list. 

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
