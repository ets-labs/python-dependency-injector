.. _create-provider:

Creating a custom provider
==========================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Custom provider, Create
   :description: This page demonstrates how to create a custom provider.

.. currentmodule:: dependency_injector.providers

You can create a custom provider.

To create a custom provider you need to follow these rules:

1. New provider class should inherit :py:class:`Provider`.
2. You need to implement the ``Provider._provide()`` method.
3. You need to implement the ``Provider.__deepcopy__()`` method. It should return an
   equivalent copy of a provider. All providers must be copied with the ``deepcopy()`` function
   from the ``providers`` module. It's essential to pass ``memo`` into ``deepcopy`` in order to keep
   the preconfigured ``args`` and ``kwargs`` of stored providers. After the a new provider object
   is created, use ``Provider._copy_overriding()`` method to copy all overriding providers. See the
   example below.
4. If new provider has a ``__init__()`` method, it should call the parent
   ``Provider.__init__()``.
5. If new provider stores any other providers, these providers should be listed in
   ``.related`` property. Property ``.related`` also should yield providers from parent
   ``.related`` property.

.. literalinclude:: ../../examples/providers/custom_factory.py
   :language: python
   :lines: 3-

.. note::
   1. Prefer delegation over inheritance. If you choose between inheriting a ``Factory`` or
      inheriting a ``Provider`` and use ``Factory`` internally - the last is better.
   2. When creating a new provider follow the ``Factory``-like injections style. Consistency matters.
   3. Use the ``__slots__`` attribute to make sure nothing could be attached to your provider. You
      will also save some memory.

.. note::
   If you don't find needed provider in the ``providers`` module and experience troubles creating
   one by your own - open a
   `Github Issue <https://github.com/ets-labs/python-dependency-injector/issues>`_.

   I'll help you to resolve the issue if that's possible. If the new provider can be useful for
   others I'll include it into the ``providers`` module.

.. disqus::
