Dependency provider
-------------------

.. currentmodule:: dependency_injector.providers

:py:class:`Dependency` provider is a placeholder for the dependency of the specified type.

The first argument of the ``Dependency`` provider specifies a type of the dependency. It is
called ``instance_of``. ``Dependency`` provider controls the type of the returned object to be an
instance of the ``instance_of`` type.

The ``Dependency`` provider must be overridden before usage. It can be overridden by any type of
the provider. The only rule is that overriding provider must return an instance of ``instance_of``
dependency type.

.. literalinclude:: ../../examples/providers/dependency.py
   :language: python
   :lines: 3-
   :emphasize-lines: 26

.. disqus::
