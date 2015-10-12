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

