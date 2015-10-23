Advanced usage
==============

Current section of documentation describes advanced usage of 
*Dependency Injector*.

@inject decorator
-----------------

``@di.inject()`` decorator can be used for making *inline* dependency 
injections.  It *patches* decorated callable in such way that dependency 
injection will be done during every call of decorated callable.

``di.inject()`` takes a various number of positional and keyword arguments 
that are used as decorated callable injections. Every time, when 
``di.inject()`` is called, positional and keyword argument injections would be 
passed as an callable arguments.

Such behaviour is very similar to the standard Python ``functools.partial`` 
object, except of one thing: all injectable values are provided 
*"as is"*, except of providers (subclasses of ``di.Provider``). Providers 
will be called every time, when injection needs to be done. For example, 
if injectable value of injection is a ``di.Factory``, it will provide new one 
instance (as a result of its call) every time, when injection needs to be done.

``di.inject()`` behaviour with context positional and keyword arguments is 
very like a standard Python ``functools.partial``:

- Positional context arguments will be appended after ``di.inject()`` 
  positional injections.
- Keyword context arguments have priority on ``di.inject()`` keyword 
  injections and will be merged over them.

Example:

.. literalinclude:: ../../examples/advanced_usage/inject_simple.py
   :language: python

Example of usage ``@di.inject()`` decorator with Flask:

.. literalinclude:: ../../examples/advanced_usage/inject_flask.py
   :language: python


@inject decorator with classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``@di.inject()`` could be applied for classes. In such case, it will look for 
class ``__init__()`` method and pass injection to it. If decorated class has 
no ``__init__()`` method, appropriate ``di.Error`` will be raised.

Example of usage ``@di.inject()`` with Flask class-based view:

.. literalinclude:: ../../examples/advanced_usage/inject_flask_class_based.py
   :language: python
