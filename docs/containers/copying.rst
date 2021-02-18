Container copying
-----------------

You can create declarative container copies using ``@containers.copy()`` decorator.

.. literalinclude:: ../../examples/containers/declarative_copy_decorator.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18-22

Decorator ``@containers.copy()`` copies providers from source container to destination container.
Destination container provider will replace source provider, if names match.

.. disqus::
