.. _aggregate-provider:

Aggregate provider
==================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Configuration,Injection,
              Aggregate,Polymorphism,Environment Variable,Flexibility
   :description: Aggregate provider aggregates other providers.
                 This page demonstrates how to implement the polymorphism and increase the
                 flexibility of your application using the Aggregate provider.

:py:class:`Aggregate` provider aggregates a group of other providers.

.. currentmodule:: dependency_injector.providers

.. literalinclude:: ../../examples/providers/aggregate.py
   :language: python
   :lines: 3-
   :emphasize-lines: 24-27

Each provider in the ``Aggregate`` is associated with a key. You can call aggregated providers by providing
their key as a first argument. All positional and keyword arguments following the key will be forwarded to
the called provider:

.. code-block:: python

   yaml_reader = container.config_readers("yaml", "./config.yml", foo=...)

You can also retrieve an aggregated provider by providing its key as an attribute name:

.. code-block:: python

   yaml_reader = container.config_readers.yaml("./config.yml", foo=...)

To retrieve a dictionary of aggregated providers, use ``.providers`` attribute:

.. code-block:: python

   container.config_readers.providers == {
       "yaml": <YAML provider>,
       "json": <JSON provider>,
   }

.. note::
   You can not override the ``Aggregate`` provider.

.. note::
   When you inject the ``Aggregate`` provider, it is passed "as is".

To use non-string keys or string keys with ``.`` and ``-``, provide a dictionary as a positional argument:

.. code-block:: python

   aggregate = providers.Aggregate({
       SomeClass: providers.Factory(...),
       "key.with.periods": providers.Factory(...),
       "key-with-dashes": providers.Factory(...),
   })

.. seealso::
   :ref:`selector-provider` to make injections based on a configuration value, environment variable, or a result of a callable.

   ``Aggregate`` provider is different from the :ref:`selector-provider`. ``Aggregate`` provider doesn't select which provider
   to inject and doesn't have a selector. It is a group of providers and is always injected "as is". The rest of the interface
   of both providers is similar.

.. note::
   ``Aggregate`` provider is a successor of :ref:`factory-aggregate-provider` provider. ``Aggregate`` provider doesn't have
   a restriction on the provider type, while ``FactoryAggregate`` aggregates only ``Factory`` providers.

.. disqus::
