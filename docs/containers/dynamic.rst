Dynamic container
-----------------

.. currentmodule:: dependency_injector.containers

:py:class:`DynamicContainer` is a collection of the providers defined in the runtime.

You create the dynamic container instance and put the providers as attributes.

.. literalinclude:: ../../examples/containers/dynamic.py
   :language: python
   :lines: 3-

The dynamic container is good for the case when your application structure depends on the
configuration file or some other source that you can reach only after application is already
running (database, api, etc).

In this example we use the configuration to fill in the dynamic container with the providers:

.. literalinclude:: ../../examples/containers/dynamic_runtime_creation.py
   :language: python
   :lines: 3-

.. disqus::

