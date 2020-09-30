.. _key-features:

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
- **Wiring**. Injects container providers into functions and methods. Helps integrating with
  other frameworks: Django, Flask, Aiohttp, etc. See :ref:`wiring`.
- **Typing**. Provides typing stubs, ``mypy``-friendly. See :ref:`provider-typing`.
- **Performance**. Fast. Written in ``Cython``.
- **Maturity**. Mature and production-ready. Well-tested, documented and supported.

The framework stands on the `PEP20 (The Zen of Python) <https://www.python.org/dev/peps/pep-0020/>`_ principle:

.. code-block:: plain

   Explicit is better than implicit

You need to specify how to assemble and where to inject the dependencies explicitly.

The power of the framework is in a simplicity.
``Dependency Injector`` is a simple tool for the powerful concept.

.. disqus::
