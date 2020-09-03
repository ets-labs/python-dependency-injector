Callable provider
=================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Function,Method,Example
   :description: Callable provider helps to make dependencies injection into functions. This page
                 demonstrates how to use a Callable provider.

.. currentmodule:: dependency_injector.providers

:py:class:`Callable` provider calls a function, a method or another callable.

.. literalinclude:: ../../examples/providers/callable.py
   :language: python
   :lines: 3-

``Callable`` provider handles an injection of the dependencies the same way like a
:ref:`factory-provider`.

.. disqus::
