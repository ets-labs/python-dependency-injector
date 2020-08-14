Declarative containers
----------------------

.. currentmodule:: dependency_injector.containers

:py:class:`DeclarativeContainer` is a collection of the providers defined in the declarative
manner. It covers the use cases when your application structure does not change in the runtime.

Container has the ``.providers`` attribute. It is a dictionary of the container providers.

.. literalinclude:: ../../examples/containers/declarative.py
   :language: python
   :lines: 3-

Your declarative container has to extend base declarative container class -
:py:class:`dependency_injector.containers.DeclarativeContainer`.

Declarative container classes can not have any methods or any other attributes then providers.

The declarative container providers should only be used after the container is initialized.

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
