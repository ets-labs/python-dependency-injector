Specialization of catalogs
--------------------------

.. currentmodule:: dependency_injector.catalogs

:py:class:`DeclarativeCatalog` and :py:class:`DynamicCatalog` could be 
specialized for any kind of needs via declaring its subclasses. 

One of such `builtin` features is a limitation to 
:py:class:`DeclarativeCatalog` (and :py:class:`DynamicCatalog`) provider type. 

Next example shows usage of this feature with :py:class:`DeclarativeCatalog` 
in couple with feature of :py:class:`dependency_injector.providers.Factory` 
for limitation of its provided type:


Listing of `services.py`:

.. literalinclude:: ../../examples/catalogs/declarative_provider_type/services.py
   :language: python
   :linenos:

Listing of `catalog.py`:

.. literalinclude:: ../../examples/catalogs/declarative_provider_type/catalog.py
   :language: python
   :linenos:

Limitation to provider type could be used with :py:class:`DynamicCatalog` 
as well.

Next example does the same that previous one, but use 
:py:class:`DynamicCatalog` instead of :py:class:`DeclarativeCatalog`:

Listing of `services.py`:

.. literalinclude:: ../../examples/catalogs/dynamic_provider_type/services.py
   :language: python
   :linenos:

Listing of `catalog.py`:

.. literalinclude:: ../../examples/catalogs/dynamic_provider_type/catalog.py
   :language: python
   :linenos:
