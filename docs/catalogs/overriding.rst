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

Also there are several useful methods and properties that help to work with 
catalog overridings:

- ``di.AbstractCatalog.is_overridden`` - read-only, evaluated in runtime, 
  property that is set to True if catalog is overridden.
- ``di.AbstractCatalog.last_overriding`` - reference to the last overriding 
  catalog, if any.
- ``di.AbstractCatalog.overridden_by`` - tuple of all overriding catalogs.
- ``di.AbstractCatalog.reset_last_overriding()`` - reset last overriding 
  catalog.
- ``di.AbstractCatalog.reset_override()`` - reset all overridings for all 
  catalog providers. 
