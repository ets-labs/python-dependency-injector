Selector providers
------------------

.. currentmodule:: dependency_injector.providers

:py:class:`Selector` provider selects provider based on the configuration value or other callable.

.. literalinclude:: ../../examples/providers/selector.py
   :language: python
   :emphasize-lines: 6-10
   :lines: 3-5,14-20
   :linenos:

:py:class:`Selector` provider has a callable called ``selector`` and a dictionary of providers.

The ``selector`` callable is provided as a first positional argument. It can be
:py:class:`Configuration` provider or any other callable. It has to return a string value.
That value is used as a key for selecting the provider from the dictionary of providers.

The providers are provided as keyword arguments. Argument name is used as a key for
selecting the provider.

Full example:

.. literalinclude:: ../../examples/providers/selector.py
   :language: python
   :emphasize-lines: 14-18
   :lines: 3-
   :linenos:

.. disqus::
