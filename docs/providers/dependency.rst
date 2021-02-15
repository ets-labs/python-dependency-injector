.. _dependency-provider:

Dependency provider
===================

.. currentmodule:: dependency_injector.providers

:py:class:`Dependency` provider is a placeholder for a dependency of a certain type.

To specify a type of the dependency use ``instance_of`` argument: ``Dependency(instance_of=SomeClass)``.
Dependency provider will control that returned object is an instance of ``instance_of`` type.

.. literalinclude:: ../../examples/providers/dependency.py
   :language: python
   :lines: 3-
   :emphasize-lines: 26,35-36

To provide a dependency you need to override the ``Dependency`` provider. You can call
provider ``.override()`` method or provide an overriding provider when creating a container.
See :ref:`provider-overriding`. If you don't provide a dependency, ``Dependency`` provider
will raise an error:

.. literalinclude:: ../../examples/providers/dependency_undefined_error.py
   :language: python
   :lines: 18-

You also can provide a default for the dependency. To provide a default use ``default`` argument:
``Dependency(..., default=...)``. Default can be a value or a provider. If default is not a provider,
dependency provider will wrap it into the ``Object`` provider.

.. literalinclude:: ../../examples/providers/dependency_default.py
   :language: python
   :lines: 16-23
   :emphasize-lines: 3

See also: :ref:`check-container-dependencies`.

.. disqus::
