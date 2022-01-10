.. _selector-provider:

Selector provider
=================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Configuration,Injection,
              Selector,Polymorphism,Environment Variable,Flexibility
   :description: Selector selects provider based on a configuration value or another callable.
                 This page demonstrates how to implement the polymorphism and increase the
                 flexibility of your application using the Selector provider.

.. currentmodule:: dependency_injector.providers

:py:class:`Selector` provider selects provider based on a configuration value or another callable.

.. literalinclude:: ../../examples/providers/selector.py
   :language: python
   :lines: 3-
   :emphasize-lines: 16-20

The first argument of the ``Selector`` provider is called ``selector``. It can be an option of
a ``Configuration`` provider or any other callable. The ``selector`` callable has to return a
string value. This value is used as a key for selecting the provider.

The providers are provided as keyword arguments. Argument name is used as a key for selecting the
provider.

When a ``Selector`` provider is called, it gets a ``selector`` value and delegates the work to
the provider with a matching name. The ``selector`` callable works as a switch: when the returned
value is changed the ``Selector`` provider will delegate the work to another provider.

.. seealso::
   :ref:`aggregate-provider` to inject a group of providers.

.. disqus::
