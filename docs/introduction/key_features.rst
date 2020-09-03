Key features
------------

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control
   :description: This article describes key features of the Dependency Injector
                 framework.

``Dependency Injector`` is a dependency injection framework for Python. It takes the
responsibility of assembling your objects.

Key features of the ``Dependency Injector`` are:

- **Pythonic design**. Simple & explicit.
- **High performance**. Written in ``Cython``.
- **Maturity and production readiness**. Downloaded over 200.000 times a month.

It stands on two principles:

- **Explicit is better than implicit (PEP20)**.
- **Do not do any magic to your code**.

How is the ``Dependency Injector`` different from the other frameworks?

- **No autowiring.** The framework does NOT do any autowiring / autoresolving of the dependencies. You need to specify everything explicitly. Because *"Explicit is better than implicit" (PEP20)*.
- **Does not pollute your code.** Your application does NOT know and does NOT depend on the framework. No ``@inject`` decorators, annotations, patching or any other magic tricks.

In addition ``Dependency Injector`` is:

- Tested.
- Documented.
- Supported.
- Semantically versioned.
- Distributed as pre-compiled wheels.

The power of the ``Dependency Injector`` is in its straightforwardness. It is a simple tool for
the powerful concept.

.. disqus::
