Key features
------------

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control
   :description: This article describes key features of "Dependency Injector" 
                 framework. It also provides some cases and recommendations 
                 about usage of "Dependency Injector" framework.


``Dependency Injector`` is a dependency injection framework for Python.
It was designed to be a unified and developer-friendly tool that helps
implement a dependency injection design pattern in a formal, pretty, and
Pythonic way.

It stands on two principles:

- Explicit is better than implicit (PEP20).
- Do no magic to your code.

How does it different from the other frameworks?

- **No autowiring.** The framework does NOT do any autowiring / autoresolving of the dependencies. You need to specify everything explicitly. Because *"Explicit is better than implicit" (PEP20)*.
- **Does not pollute your code.** Your application does NOT know and does NOT depend on the framework. No ``@inject`` decorators, annotations, patching or any other magic tricks.

``Dependency Injector`` makes a simple contract with you:

- You tell the framework how to build you code
- The framework does it for you

The power of the ``Dependency Injector`` is in its simplicity and straightforwardness. It is a simple tool for the powerful concept.

The key features of the ``Dependency Injector`` framework are:

+ Easy, smart, and Pythonic style.
+ Does NOT pollute client code.
+ Obvious and clear structure.
+ Extensibility and flexibility.
+ High performance.
+ Memory efficiency.
+ Thread safety.
+ Documented.
+ Semantically versioned.
+ Distributed as pre-compiled wheels.

``Dependency Injector`` containers and providers are implemented as C extension
types using ``Cython``.

``Dependency Injector`` framework can be used in the different application types:

+ Web applications based on the ``Flask``, ``Django`` or any other web framework.
+ Asynchronous applications ``asyncio``, ``aiohttp``, ``Tornado``, or ``Twisted``.
+ Standalone frameworks and libraries.
+ GUI applications.

``Dependency Injector`` framework can be integrated on the different project
stages:

+ It can be used in the beginning of the development of a new application.
+ It can be integrated into application that is on its active development stage.
+ It can be used for refactoring of legacy application.

Components of ``Dependency Injector`` framework could be used:

+ In composition with each other.
+ Independently from each other.

.. disqus::
