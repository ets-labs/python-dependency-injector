
Advanced usage
==============

Current section of documentation describes advanced usage of *Objects*.

@inject decorator
-----------------

``@inject`` decorator can be used for making *inline* dependency injections.
It *patches* decorated callable in such way that dependency injection will be
done during every call of decorated callable.

``@inject`` decorator takes only argument that is supposed to be an
``objects.injections.KwArg`` injection.

Any Python object will be injected *as is*, except *Objects* providers,
that will be called to provide injectable value.

Example:

.. literalinclude:: ../../examples/advanced_usage/inject_decorator_simple.py
   :language: python

Example of dependecy injection in Flask view:

.. literalinclude:: ../../examples/advanced_usage/inject_decorator_flask.py
   :language: python
