Overriding of catalogs
----------------------

.. currentmodule:: dependency_injector.catalogs

Catalogs can be overridden by other catalogs. This, actually, means that 
all of the providers from overriding catalog will override providers with the 
same names in overridden catalog.

There are two ways to override :py:class:`DeclarativeCatalog` with another 
catalog:

- Use :py:meth:`DeclarativeCatalog.override` method.
- Use :py:func:`override` class decorator.

Example of overriding catalog using :py:meth:`DeclarativeCatalog.override` 
method:

.. literalinclude:: ../../examples/catalogs/override_declarative.py
   :language: python

Example of overriding catalog using :py:func:`override` decorator:

.. literalinclude:: ../../examples/catalogs/override_declarative_decorator.py
   :language: python

Also there are several useful :py:class:`DeclarativeCatalog`  methods and 
properties that help to work with catalog overridings:

- :py:attr:`DeclarativeCatalog.is_overridden` - read-only property that is set 
  to ``True`` if catalog is overridden.
- :py:attr:`DeclarativeCatalog.last_overriding` - read-only reference to 
  the last overriding catalog, if any.
- :py:attr:`DeclarativeCatalog.overridden_by` - tuple of all overriding 
  catalogs.
- :py:meth:`DeclarativeCatalog.reset_last_overriding()` - reset last 
  overriding catalog.
- :py:meth:`DeclarativeCatalog.reset_override()` - reset all overridings for 
  all catalog providers. 

:py:class:`DynamicCatalog` has exactly the same functionality, except of 
:py:func:`override` decorator. Also :py:class:`DynamicCatalog` can override 
:py:class:`DeclarativeCatalog` and vise versa.

Example of overriding :py:class:`DeclarativeCatalog` by 
:py:class:`DynamicCatalog`:

.. literalinclude:: ../../examples/catalogs/override_declarative_by_dynamic.py
   :language: python
