Advanced usage
==============

Current section of documentation describes advanced usage of 
*Dependency Injector*.

@inject decorator
-----------------

.. currentmodule:: dependency_injector.injections

:py:func:`inject` decorator is a part of 
:py:mod:`dependency_injector.injections` module.

:py:func:`inject` decorator can be used for making *inline* dependency 
injections.  It *patches* decorated callable in such way that dependency 
injection will be done during every call of decorated callable.

:py:func:`inject` takes a various number of positional and keyword arguments 
that are used as decorated callable injections. Every time, when 
:py:func:`inject` is called, positional and keyword argument injections would 
be passed as an callable arguments.

Such behaviour is very similar to the standard Python ``functools.partial`` 
object, except of one thing: all injectable values are provided 
*"as is"*, except of providers (subclasses of 
:py:class:`dependency_injector.providers.Provider`). Providers 
will be called every time, when injection needs to be done. For example, 
if injectable value of injection is a 
:py:class:`dependency_injector.providers.Factory`, it will provide new one 
instance (as a result of its call) every time, when injection needs to be done.

:py:func:`inject` behaviour with context positional and keyword arguments is 
very like a standard Python ``functools.partial``:

- Positional context arguments will be appended after :py:func:`inject` 
  positional injections.
- Keyword context arguments have priority on :py:func:`inject` keyword 
  injections and will be merged over them.

Example:

.. literalinclude:: ../../examples/advanced_usage/inject_simple.py
   :language: python
   :linenos:

Example of usage :py:func:`inject` decorator with Flask:

.. literalinclude:: ../../examples/advanced_usage/inject_flask.py
   :language: python
   :linenos:


@inject decorator with classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:func:`inject` could be applied for classes. In such case, it will look for 
class ``__init__()`` method and pass injection to it. If decorated class has 
no ``__init__()`` method, appropriate 
:py:exc:`dependency_injector.errors.Error` will be raised.

Example of usage :py:func:`inject` with Flask class-based view:

.. literalinclude:: ../../examples/advanced_usage/inject_flask_class_based.py
   :language: python
   :linenos:
