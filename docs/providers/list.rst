List providers
--------------

.. currentmodule:: dependency_injector.providers

:py:class:`List` provider provides a list of values.

.. literalinclude:: ../../examples/providers/list.py
   :language: python
   :lines: 23-29
   :linenos:

:py:class:`List` provider is needed for injecting a list of dependencies. It handles
positional argument injections the same way as :py:class:`Factory` provider:

+ All providers (instances of :py:class:`Provider`) are called every time
  when injection needs to be done.
+ Providers could be injected "as is" (delegated), if it is defined explicitly. Check out
  :ref:`factory_providers_delegation`.
+ All other values are injected *"as is"*.

Full example:

.. literalinclude:: ../../examples/providers/list.py
   :language: python
   :emphasize-lines: 23-29
   :linenos:

.. note::

    Positional context argument injections and keyword argument injections are not
    supported.

.. disqus::
