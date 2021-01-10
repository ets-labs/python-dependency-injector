.. _async-injections:

Asynchronous injections
=======================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Providers,Async,Injections,Asynchronous,Await,
              Asyncio
   :description: Dependency Injector providers support asynchronous injections. This page
                 demonstrates how make asynchronous dependency injections in Python.

Providers support asynchronous injections.

.. literalinclude:: ../../examples/providers/async.py
   :language: python
   :emphasize-lines: 26-29
   :lines: 3-

If provider has any awaitable injections it switches into async mode. In async mode provider always returns awaitable.
This causes a cascade effect:

.. code-block:: bash

   provider1()              <── Async mode enabled <──┐
   │                                                  │
   ├──> provider2()                                   │
   │                                                  │
   ├──> provider3()         <── Async mode enabled <──┤
   │    │                                             │
   │    └──> provider4()    <── Async provider ───────┘
   │
   └──> provider5()
        │
        └──> provider6()
