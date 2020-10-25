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

.. note::
    Positional argument are not supported.

.. disqus::
