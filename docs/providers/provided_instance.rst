Injecting attributes, items, or call methods of the provided instance
---------------------------------------------------------------------

.. currentmodule:: dependency_injector.providers

In this section you will know how to inject provided instance attribute or item into the other
provider.

It also describes how to call a method of the provided instance and use the result of
this call as an injection value.

.. literalinclude:: ../../examples/providers/provided_instance.py
   :language: python
   :emphasize-lines: 26-32
   :lines: 3-

To use the feature you should use the ``.provided`` attribute of the injected provider. This
attribute helps to specify what happens with the provided instance. You can retrieve an injection
value from:

- an attribute of the provided instance
- an item of the provided instance
- a call of the provided instance method

When you use the call of the provided instance method you can specify the injections into this
method like you do with any other provider.

You can do nested constructions:

.. literalinclude:: ../../examples/providers/provided_instance_complex.py
   :language: python
   :emphasize-lines: 24-30
   :lines: 3-

Attribute ``.provided`` is available for the providers that return instances. Providers that
have ``.provided`` attribute:

- :py:class:`Callable` and its subclasses
- :py:class:`Factory` and its subclasses
- :py:class:`Singleton` and its subclasses
- :py:class:`Object`
- :py:class:`List`
- :py:class:`Selector`
- :py:class:`Dependency`

Special providers like :py:class:`Configuration` or :py:class:`Delegate` do not have the
``.provided`` attribute.

Provider subclasses
-------------------

When you create a new provider subclass and want to implement the ``.provided`` attribute, you
should use the :py:class:`ProvidedInstance` provider.

.. code-block:: python

   @property
   def provided(self):
       """Return :py:class:`ProvidedInstance` provider."""
       return ProvidedInstance(self)

In all other cases you should not use :py:class:`ProvidedInstance`, :py:class:`AttributeGetter`,
:py:class:`ItemGetter`, or :py:class:`MethodCaller` providers directly. Use the ``.provided``
attribute of the injected provider instead.

.. disqus::
