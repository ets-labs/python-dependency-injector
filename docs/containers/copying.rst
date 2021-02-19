Container copying
-----------------

You can create declarative container copies using ``@containers.copy()`` decorator.

.. literalinclude:: ../../examples/containers/declarative_copy_decorator1.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18-22

Decorator ``@containers.copy()`` copies providers from source container to destination container.
Destination container provider will replace source provider, if names match.

Decorator ``@containers.copy()`` helps you when you create derived declarative containers
from the base one. Base container often keeps default dependencies while derived containers define
overriding providers. Without ``@containers.copy()`` decorator, overridden providers are available
in the derived container, but base class dependencies continue to be bound to the base class providers.

.. literalinclude:: ../../examples/containers/declarative_copy_decorator2.py
   :language: python
   :lines: 11-

.. disqus::
