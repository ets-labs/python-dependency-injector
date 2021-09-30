Dict provider
=============

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Dict,Injection
   :description: Dict provider helps to inject a dictionary of the dependencies. This page demonstrates
                 how to use Dict provider.

.. currentmodule:: dependency_injector.providers

:py:class:`Dict` provider provides a dictionary of values.

.. literalinclude:: ../../examples/providers/dict.py
   :language: python
   :lines: 3-
   :emphasize-lines: 21-24

``Dict`` provider handles keyword arguments the same way as a :ref:`factory-provider`.

To use non-string keys or keys with ``.`` and ``-`` provide a dictionary as a positional argument:

.. code-block:: python

   providers.Dict({
       SomeClass: providers.Factory(...),
       "key.with.periods": providers.Factory(...),
       "key-with-dashes": providers.Factory(...),
   })

Example:

.. literalinclude:: ../../examples/providers/dict_non_string_keys.py
   :language: python
   :lines: 3-
   :emphasize-lines: 40-43

.. disqus::
