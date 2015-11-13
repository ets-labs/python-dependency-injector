Declarative catalogs
--------------------

``di.DeclarativeCatalog`` is a catalog of providers that could be defined in 
declarative manner. It should cover most of the cases when list of providers 
that would be included in catalog is deterministic (catalog will not change 
its structure in runtime).

Definition of declarative catalogs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Declarative catalogs have to extend base declarative catalog class - 
``di.DeclarativeCatalog``.

Providers have to be defined like catalog's class attributes. Every provider in
catalog has name. This name should follow ``some_provider`` convention, 
that is standard naming convention for attribute names in Python.

.. note::

    It might be useful to add such ``""":type: di.Provider -> Object1"""`` 
    docstrings just on the next line after provider's definition.  It will 
    help code analyzing tools and IDE's to understand that variable above 
    contains some callable object, that returns particular instance as a 
    result of its call.

Here is an simple example of declarative catalog with several factories:

.. image:: /images/catalogs/declarative.png
    :width: 85%
    :align: center

.. literalinclude:: ../../examples/catalogs/declarative.py
   :language: python

Declarative catalogs API
~~~~~~~~~~~~~~~~~~~~~~~~

``di.DeclarativeCatalog`` has several features that could be useful for some 
kind of operations on catalog's providers:

- ``di.DeclarativeCatalog.providers`` is read-only attribute that contains 
  ``dict`` of all catalog providers, including providers that are inherited 
  from parent catalogs, where key is the name of provider and value is 
  provider itself.
- ``di.DeclarativeCatalog.cls_providers`` is read-only attribute contains 
  ``dict`` of current catalog providers, where key is the name of provider 
  and value is provider itself.
- ``di.DeclarativeCatalog.inherited_providers`` is read-only attribute 
  contains ``dict`` of all providers that are inherited from parent catalogs, 
  where key is the name of provider and value is provider itself. 
- ``di.DeclarativeCatalog.filter(provider_type=di.Provider)`` is a class 
  method that could be used for filtering catalog providers by provider types 
  (for example, for getting all ``di.Factory`` providers). 
  ``di.DeclarativeCatalog.filter()`` method use 
  ``di.DeclarativeCatalog.providers``.

Example:

.. image:: /images/catalogs/declarative_api.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/catalogs/declarative_api.py
   :language: python
