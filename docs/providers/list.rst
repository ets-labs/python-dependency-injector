List provider
=============

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,List,Injection
   :description: List provider helps to inject a list of the dependencies. This page demonstrates
                 how to use a List provider.

.. currentmodule:: dependency_injector.providers

:py:class:`List` provider provides a list of values.

.. literalinclude:: ../../examples/providers/list.py
   :language: python
   :lines: 3-
   :emphasize-lines: 21-24

``List`` provider handles positional arguments the same way as a :ref:`factory-provider`.

.. note::
    Keyword argument are not supported.

.. disqus::
