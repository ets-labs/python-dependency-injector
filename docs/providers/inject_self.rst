Injecting container "self"
==========================

You can inject container "self" into container providers.

.. literalinclude:: ../../examples/containers/inject_self.py
   :language: python
   :lines: 3-
   :emphasize-lines: 20, 26

To inject container "self" you need to define ``Self`` provider. Container can have only one ``Self`` provider.

Usually you will use name ``__self__``.
You can also use different name. When you use different name container will also reference
defined ``Self`` provider in ``.__self__`` attribute.

Provider ``Self`` is not listed in container ``.providers`` attributes.

.. disqus::

