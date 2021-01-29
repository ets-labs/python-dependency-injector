Dependency provider
===================

.. currentmodule:: dependency_injector.providers

:py:class:`Dependency` provider is a placeholder for a dependency of a certain type.

To specify a type of the dependency use ``instance_of`` argument: ``Dependency(instance_of=SomeClass)``.
Dependency provider will control that returned object is an instance of ``instance_of`` type.

The ``Dependency`` provider must be overridden before usage. It can be overridden by any type of
the provider. The only rule is that overriding provider must return an instance of ``instance_of``
dependency type.

.. literalinclude:: ../../examples/providers/dependency.py
   :language: python
   :lines: 3-
   :emphasize-lines: 26

.. disqus::
