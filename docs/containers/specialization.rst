Specialization of containers
----------------------------

.. currentmodule:: dependency_injector.containers

:py:class:`DeclarativeContainer` could be specialized for any kind of needs 
via declaring its subclasses. 

One of such `builtin` features is a limitation for providers type.

Next example shows usage of this feature with :py:class:`DeclarativeContainer` 
in couple with feature of :py:class:`dependency_injector.providers.Factory` 
for limitation of its provided type:

.. literalinclude:: ../../examples/containers/declarative_provider_type.py
   :language: python
   :linenos:

Limitation for providers type could be used with :py:class:`DynamicContainer` 
as well:

.. literalinclude:: ../../examples/containers/dynamic_provider_type.py
   :language: python
   :linenos:
