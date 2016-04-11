Dynamic catalogs
----------------

.. currentmodule:: dependency_injector.catalogs

:py:class:`DynamicCatalog` is a catalog of providers that could be created in 
application's runtime. It should cover most of the cases when list of 
providers that would be included in catalog is non-deterministic in terms of 
apllication code (catalog's structure could be determined just after 
application will be started and will do some initial work, like parsing list 
of catalog's providers from the configuration).

:py:class:`DeclarativeCatalog` and :py:class:`DynamicCatalog` have 
100% API parity.

Main difference between :py:class:`DeclarativeCatalog` and 
:py:class:`DynamicCatalog` is that :py:class:`DeclarativeCatalog` acts on 
class-level, while :py:class:`DynamicCatalog` do the same on 
instance-level.

Here is an simple example of defining dynamic catalog with several factories:

.. literalinclude:: ../../examples/catalogs/dynamic.py
   :language: python
   :linenos:

Next one example demonstrates creation and runtime filling of dynamic catalog:

.. literalinclude:: ../../examples/catalogs/dynamic_runtime_creation.py
   :language: python
   :linenos:
