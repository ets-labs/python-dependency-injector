Declarative container
---------------------

.. currentmodule:: dependency_injector.containers

:py:class:`DeclarativeContainer` is a class-based style of the providers definition.

You create the declarative container subclass, put the providers as attributes and create the
container instance.

.. literalinclude:: ../../examples/containers/declarative.py
   :language: python
   :lines: 3-

The declarative container providers should only be used when you have the container instance.
Working with the providers of the container on the class level will influence all further
instances.

The declarative container can not have any methods or any other attributes then providers.

The container class provides next attributes:

- ``providers`` - the dictionary of all the container providers
- ``cls_providers`` - the dictionary of the container providers of the current container
- ``inherited_providers`` - the dictionary of all the inherited container providers

.. literalinclude:: ../../examples/containers/declarative_inheritance.py
   :language: python
   :lines: 3-

Injections in the declarative container are done the usual way:

.. literalinclude:: ../../examples/containers/declarative_injections.py
   :language: python
   :lines: 3-

You can override the container providers when you create the container instance:

.. literalinclude:: ../../examples/containers/declarative_override_providers.py
   :language: python
   :lines: 3-

.. disqus::
