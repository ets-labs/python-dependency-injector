Operating with catalogs
-----------------------

``di.AbstractCatalog`` has several features that could be useful for some kind 
of operations on catalog's providers:

- ``di.AbstractCatalog.providers`` is read-only attribute that contains 
  ``dict`` of all catalog providers, including providers that are inherited 
  from parent catalogs, where key is the name of provider and value is 
  provider itself.
- ``di.AbstractCatalog.cls_providers`` is read-only attribute contains ``dict``
  of current catalog providers, where key is the name of provider and value is 
  provider itself.
- ``di.AbstractCatalog.inherited_providers`` is read-only attribute contains 
  ``dict`` of all providers that are inherited from parent catalogs, where key 
  is the name of provider and value is provider itself. 
- ``di.AbstractCatalog.filter(provider_type=di.Provider)`` is a class method 
  that could be used for filtering catalog providers by provider types 
  (for example, for getting all ``di.Factory`` providers). 
  ``di.AbstractCatalog.filter()`` method use ``di.AbstractCatalog.providers``.

Example:

.. image:: /images/catalogs/operating_with_providers.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/catalogs/operating_with_providers.py
   :language: python
