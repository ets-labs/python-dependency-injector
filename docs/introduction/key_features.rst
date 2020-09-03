Key features
------------

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control
   :description: This article describes key features of the Dependency Injector
                 framework.

Key features of the ``Dependency Injector``:

- **Providers**. Provides ``Factory``, ``Singleton``, ``Callable``, ``Coroutine``, ``Object``,
  ``List``, ``Configuration``, ``Dependency`` and ``Selector`` providers that help assembling your
  objects. See :ref:`providers`.
- **Overriding**. Can override any provider by another provider on the fly. This helps in testing
  and configuring dev / stage environment to replace API clients with stubs etc. See
  :ref:`provider-overriding`.
- **Configuration**. Read configuration from ``yaml`` & ``ini`` files, environment variables
  and dictionaries. See :ref:`configuration-provider`.
- **Containers**. Provides declarative and dynamic containers. See :ref:`containers`.
- **Performance**. Written in ``Cython``.
- **Maturity**. Mature and ready for production.

The framework stands on two principles:

- **Explicit is better than implicit (PEP20)**.
- **Do not do any magic to your code**.

How is that different from the other frameworks?

- **No autowiring.** The framework does NOT do any autowiring / autoresolving of the dependencies. You need to specify everything explicitly. Because *"Explicit is better than implicit" (PEP20)*.
- **Does not pollute your code.** Your application does NOT know and does NOT depend on the framework. No ``@inject`` decorators, annotations, patching or any other magic tricks.

The power of the framework is in a simplicity. ``Dependency Injector`` is a simple tool for the powerful concept.

In addition ``Dependency Injector`` is:

- Tested.
- Documented.
- Supported.
- Semantically versioned.
- Distributed as pre-compiled wheels.

.. disqus::
