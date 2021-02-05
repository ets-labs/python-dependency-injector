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

.. disqus::
