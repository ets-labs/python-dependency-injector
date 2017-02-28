Dynamic containers
------------------

.. currentmodule:: dependency_injector.containers

:py:class:`DynamicContainer` is an inversion of control container with dynamic 
structure. It should cover most of the cases when list of providers that 
would be included in container is non-deterministic and depends on 
application's flow or its configuration (container's structure could be 
determined just after application will be started and will do some initial 
work, like parsing list of container's providers from the configuration).

While :py:class:`DeclarativeContainer` acts on class-level, 
:py:class:`DynamicContainer` does the same on instance-level.

Here is an simple example of defining dynamic container with several factories:

.. literalinclude:: ../../examples/containers/dynamic.py
   :language: python
   :linenos:

Next example demonstrates creation of dynamic container based on some 
configuration:

.. literalinclude:: ../../examples/containers/dynamic_runtime_creation.py
   :language: python
   :linenos:


.. disqus::
