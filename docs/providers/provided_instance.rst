Injecting provided object attributes, items, or call its methods
================================================================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Attribute,Method,Call
   :description: This page demonstrates how to inject attributes, items or call method of the
                 provided instance.

.. currentmodule:: dependency_injector.providers

You can inject provided object attribute, item or result of its method call.

.. literalinclude:: ../../examples/providers/provided_instance.py
   :language: python
   :emphasize-lines: 26-32
   :lines: 3-

To use the feature you should use the ``.provided`` attribute of the injected provider. This
attribute helps to specify what happens with the provided instance before the injection. You can
use any combination of the following:

- an attribute of the provided object
- an item of the provided object
- a call of the provided object method

When you use a call of the provided instance method you can specify the injections for this
method like you do with any other provider.

You can do nested constructions:

.. literalinclude:: ../../examples/providers/provided_instance_complex.py
   :language: python
   :emphasize-lines: 24-30
   :lines: 3-

The ``.provided`` attribute is available for the next providers:

- :py:class:`Factory` and its subclasses
- :py:class:`Singleton` and its subclasses
- :py:class:`Callable` and its subclasses
- :py:class:`Object`
- :py:class:`List`
- :py:class:`Selector`
- :py:class:`Dependency`

When you create a new provider subclass and want to implement the ``.provided`` attribute, you
should use the :py:class:`ProvidedInstance` provider. Add the ``.provided`` property
implementation to a new subclass:

.. code-block:: python

   @property
   def provided(self):
       return ProvidedInstance(self)

.. disqus::
