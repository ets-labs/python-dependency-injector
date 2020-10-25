Container overriding
--------------------

.. currentmodule:: dependency_injector.containers

The container can be overridden by the other container. All of the providers from the overriding
container will override the providers with the same names in the overridden container.

.. literalinclude:: ../../examples/containers/override.py
   :language: python
   :lines: 3-

It helps in a testing. Also you can use it for configuring project for the different
environments: replace an API client with a stub on the dev or stage.

The container also has:

- ``container.overridden`` - tuple of all overriding containers.
- ``container.reset_last_overriding()`` - reset last overriding for each provider in the container.
- ``container.reset_override()`` - reset all overriding in the container.

:py:class:`DynamicContainer` has the same functionality.

Another possible way to override container providers on declarative level is
``@containers.override()`` decorator:

.. literalinclude:: ../../examples/containers/declarative_override_decorator.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12-16

Decorator ``@containers.override()`` takes a container for overriding as an argument.
This container providers will be overridden by the providers with the same names from
the decorated container.

It helps to change the behaviour of application by importing extension modules but not a code change.
Imported module can override providers in main container. While the code uses main container as
before, the overridden providers provide components defined in the extension module.

.. disqus::
