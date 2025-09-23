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

A declarative container cannot have any methods or attributes other than providers.

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

You can override container providers while creating a container instance:

.. literalinclude:: ../../examples/containers/declarative_override_providers.py
   :language: python
   :lines: 3-
   :emphasize-lines: 13

Alternatively, you can call ``container.override_providers()`` method when the container instance
already exists:

.. code-block:: python
   :emphasize-lines: 3

   container = Container()

   container.override_providers(foo=mock.Mock(Foo), bar=mock.Mock(Bar))

   assert isinstance(container.foo(), mock.Mock)
   assert isinstance(container.bar(), mock.Mock)

You can also use ``container.override_providers()`` with a context manager to reset
provided overriding after the context is closed:

.. code-block:: python
   :emphasize-lines: 3

   container = Container()

   with container.override_providers(foo=mock.Mock(Foo), bar=mock.Mock(Bar)):
       assert isinstance(container.foo(), mock.Mock)
       assert isinstance(container.bar(), mock.Mock)

   assert isinstance(container.foo(), Foo)
   assert isinstance(container.bar(), Bar)

.. disqus::
