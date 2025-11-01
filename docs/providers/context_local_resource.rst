.. _context-local-resource-provider:

Context Local Resource provider
================================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Resource,Context Local,
              Context Variables,Singleton,Per-context
   :description: Context Local Resource provider provides a component with initialization and shutdown
                 that is scoped to execution context using contextvars. This page demonstrates how to
                 use context local resource provider.

.. currentmodule:: dependency_injector.providers

``ContextLocalResource`` inherits from :ref:`resource-provider` and uses the same initialization and shutdown logic
as the standard ``Resource`` provider.
It extends it with context-local storage using Python's ``contextvars`` module.
This means that objects are context local singletons - the same context will
receive the same instance, but different execution contexts will have their own separate instances.

This is particularly useful in asynchronous applications where you need per-request resource instances
(such as database sessions) that are automatically cleaned up when the request context ends.
Example:

.. literalinclude:: ../../examples/providers/context_local_resource.py
   :language: python
   :lines: 3-



.. disqus::

