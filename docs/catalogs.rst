Catalogs
========

Catalogs are collections of providers. Main purpose of catalogs is to group
providers. 

There are, actually, several popular use cases of catalogs:

- Grouping of providers from same architectural layer (for example, 
  ``Services``, ``Models`` and ``Forms`` catalogs).
- Grouping of providers from a same functional components (for example,
  catalog ``Users``, that contains all functional parts of ``Users``
  component).

Als, for both of these and some other cases, it might be useful to attach 
some init / shutdown functionality or something else, that deals with group 
of providers.

Writing catalogs
----------------

Catalogs have to be created by extending base catalog class 
``objects.catalog.AbstractCatalog``.

Providers have to be defined like catalog's attributes. Every provider in
catalog has name. This name should follow ``some_provider`` manner, that is 
standard naming convention for names of attributes in Python.

.. note::

    It might be useful to add such 
    ``""":type: (objects.Provider) -> Object1"""`` documentation blocks one 
    line after provider definition for every provider. It will help code 
    analysis tools and IDE's to understand that variable above contains some 
    callable object, that returns particular instance as a result of call.

Example:

.. image:: /images/catalogs/simple.png
    :width: 100%
    :align: center

.. literalinclude:: ../examples/catalogs/simple.py
   :language: python

Operating with catalog providers
--------------------------------

There are several things that could be useful for operating with catalog
providers:

- First of all, ``Catalog.providers`` attribute contains ``dict`` with all
  catalog providers and their catalog names. This dictionary could be used
  for any kind of operations that could be done with providers. The only note,
  is that ``Catalog.providers`` attribute is read-only.
- Second one, ``Catalog.filter(provider_type=Provider)`` method could be
  used for filtering catalog providers by provider types (for example, for 
  getting all ``Factory`` providers).

Example:

.. literalinclude:: ../examples/catalogs/operating_with_providers.py
   :language: python

Overriding of catalogs
----------------------

Catalogs can be overridden by other catalogs. This, actually, means that 
all of the providers from overriding catalog will override providers with the 
same names in overridden catalog.

There are two ways to override catalog by another catalog:

- Use ``Catalog.override(Catalog)`` method.
- Use ``@override(Catalog)`` class decorator.

Example of overriding catalog using ``Catalog.override()`` method:

.. literalinclude:: ../examples/catalogs/override.py
   :language: python

Example of overriding catalog using ``@override()`` decorator:

.. literalinclude:: ../examples/catalogs/override_decorator.py
   :language: python
