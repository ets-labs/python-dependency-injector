Catalogs
========

Catalogs are collections of providers. Main purpose of catalogs is to group
providers. 

There are, actually, several popular cases of catalogs usage:

- Grouping of providers from the same architectural layer (for example, 
  ``Services``, ``Models`` and ``Forms`` catalogs).
- Grouping of providers from the same functional groups (for example,
  catalog ``Users``, that contains all functional parts of ``Users``
  component).

Also, for both of these and some other cases, it might be useful to attach 
some init / shutdown functionality or something else, that deals with group 
of providers.

Writing catalogs
----------------

Catalogs have to extend base catalog class ``di.AbstractCatalog``.

Providers have to be defined like catalog's attributes. Every provider in
catalog has name. This name should follow ``some_provider`` convention, 
that is standard naming convention for attribute names in Python.

.. note::

    It might be useful to add such ``""":type: (di.Provider) -> Object1"""`` 
    documentation blocks one line after provider definition for every provider.
    It will help code analyzing tools and IDE's to understand that variable 
    above contains some callable object, that returns particular instance 
    in a result of call.

Example:

.. image:: /images/catalogs/simple.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/catalogs/simple.py
   :language: python

Operating with catalog providers
--------------------------------

There are several things that could be useful for operating with catalog
providers:

- First of all, ``di.AbstractCatalog.providers`` attribute contains ``dict`` 
  with all catalog providers. This dictionary could be used for any kind of 
  operations that could be done with providers. The only note, is that 
  ``di.AbstractCatalog.providers`` attribute is read-only.
- Second one, ``di.AbstractCatalog.filter(provider_type=di.Provider)`` method 
  could be used for filtering catalog providers by provider types (for example,
  for getting all ``di.Factory`` providers).

Example:

.. literalinclude:: ../../examples/catalogs/operating_with_providers.py
   :language: python

Overriding of catalogs
----------------------

Catalogs can be overridden by other catalogs. This, actually, means that 
all of the providers from overriding catalog will override providers with the 
same names in overridden catalog.

There are two ways to override catalog by another catalog:

- Use ``di.AbstractCatalog.override(AnotherCatalog)`` method.
- Use ``@di.override(AnotherCatalog)`` class decorator.

Example of overriding catalog using ``di.AbstractCatalog.override()`` method:

.. literalinclude:: ../../examples/catalogs/override.py
   :language: python

Example of overriding catalog using ``@di.override()`` decorator:

.. literalinclude:: ../../examples/catalogs/override_decorator.py
   :language: python
