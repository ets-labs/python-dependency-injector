Advanced usage
==============

Current section of documentation describes advanced usage of 
*Dependency Injector*.

@inject decorator
-----------------

``@di.inject()`` decorator can be used for making *inline* dependency 
injections.  It *patches* decorated callable in such way that dependency 
injection will be done during every call of decorated callable.

``@di.inject()`` decorator takes keyword argument, that will be injected 
during every next call of decorated callback with the same name. Any Python 
object will be injected *as is*, except ``di.Provider``'s, which will be 
called to provide injectable values.

Example:

.. literalinclude:: ../../examples/advanced_usage/inject_simple.py
   :language: python

Example of usage ``@di.inject()`` decorator with Flask:

.. literalinclude:: ../../examples/advanced_usage/inject_flask.py
   :language: python


@inject decorator with classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``@di.inject()`` could be applied for classes. In such case, it will look for 
class's ``__init__()`` method and pass injection to it. If decorated class has 
no ``__init__()`` method, appropriate ``di.Error`` will be raised.

Example of usage ``@di.inject()`` with Flask class-based view:

.. literalinclude:: ../../examples/advanced_usage/inject_flask_class_based.py
   :language: python
