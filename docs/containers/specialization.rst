Specialization of the container provider type
---------------------------------------------

.. currentmodule:: dependency_injector.containers

You can make a restriction of the :py:class:`DeclarativeContainer` provider type:

.. literalinclude:: ../../examples/containers/declarative_provider_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 29-31

The emphasized lines will cause an error because ``other_provider`` is not a subtype of the
``ServiceProvider``. This helps to control the content of the container.

The same works for the :py:class:`DynamicContainer`:

.. literalinclude:: ../../examples/containers/dynamic_provider_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 23

The emphasized line will also cause an error.

.. disqus::
