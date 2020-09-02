Coroutine provider
==================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Coroutine,Asynchronous,
              Asyncio,Example
   :description: Coroutine provider creates a coroutine. This page demonstrates how to use a
                 Coroutine provider.

.. currentmodule:: dependency_injector.providers

:py:class:`Coroutine` provider creates a coroutine.

.. literalinclude:: ../../examples/providers/coroutine.py
   :language: python
   :lines: 3-

.. note::
   The example works on Python 3.7+. For earlier versions use ``loop.run_until_complete()``.

``Coroutine`` provider handles an injection of the dependencies the same way like a
:ref:`factory-provider`.

.. note::
   ``Coroutine`` provider returns ``True`` for ``asyncio.iscoroutinefunction()`` check.

.. disqus::
