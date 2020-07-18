List providers
--------------

.. currentmodule:: dependency_injector.providers

:py:class:`List` provider provides a list of values.

.. literalinclude:: ../../examples/providers/list.py
   :language: python
   :emphasize-lines: 6-9
   :lines: 6-8, 23-29

:py:class:`List` provider is needed for injecting a list of dependencies. It handles
positional argument injections the same way as :py:class:`Factory` provider:

+ All providers (instances of :py:class:`Provider`) are called every time
  when injection needs to be done.
+ Providers could be injected "as is" (delegated), if it is defined explicitly. Check out
  :ref:`factory_providers_delegation`.
+ All other values are injected *"as is"*.
+ Positional context arguments will be appended after :py:class:`List` positional injections.

Full example:

.. literalinclude:: ../../examples/providers/list.py
   :language: python
   :emphasize-lines: 23-26
   :lines: 3-

.. note::

    Keyword argument injections are not supported.

.. disqus::
