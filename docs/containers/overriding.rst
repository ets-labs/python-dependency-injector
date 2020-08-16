Overriding of the container
---------------------------

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

.. disqus::
