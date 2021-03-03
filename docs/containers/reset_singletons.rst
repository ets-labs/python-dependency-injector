.. _reset-container-singletons:

Reset container singletons
--------------------------

To reset all container singletons use method ``.reset_singletons()``.

.. literalinclude:: ../../examples/containers/reset_singletons.py
   :language: python
   :lines: 3-
   :emphasize-lines: 16

Method ``.reset_singletons()`` also resets singletons in sub-containers: ``providers.Container`` and
``providers.DependenciesContainer.``

.. literalinclude:: ../../examples/containers/reset_singletons_subcontainers.py
   :language: python
   :lines: 3-
   :emphasize-lines: 21

You can use ``.reset_singletons()`` method with a context manager. Singletons will be reset on
both entering and exiting a context.

.. literalinclude:: ../../examples/containers/reset_singletons_with.py
   :language: python
   :lines: 3-
   :emphasize-lines: 14-15

See also: :ref:`singleton-provider`.

.. disqus::
