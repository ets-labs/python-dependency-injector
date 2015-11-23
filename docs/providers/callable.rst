Callable providers
------------------

.. module:: dependency_injector.providers

:py:class:`Callable` provider is a provider that wraps particular callable with
some injections. Every call of this provider returns result of call of initial
callable.

Callable providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Callable` takes a various number of positional and keyword 
arguments that are used as decorated callable injections. Every time, when 
:py:class:`Callable` is called, positional and keyword argument injections 
would be passed as an callable arguments.

Such behaviour is very similar to the standard Python ``functools.partial`` 
object, except of one thing: all injectable values are provided 
*"as is"*, except of providers (subclasses of :py:class:`Provider`). Providers 
will be called every time, when injection needs to be done. For example, 
if injectable value of injection is a :py:class:`Factory`, it will provide 
new one instance (as a result of its call) every time, when injection needs 
to be done.

:py:class:`Callable` behaviour with context positional and keyword arguments 
is very like a standard Python ``functools.partial``:

- Positional context arguments will be appended after :py:class:`Callable` 
  positional injections.
- Keyword context arguments have priority on :py:class:`Callable` keyword 
  injections and will be merged over them.

Example that shows usage of :py:class:`Callable` with positional argument 
injections:

.. literalinclude:: ../../examples/providers/callable_args.py
   :language: python

Next one example shows usage of :py:class:`Callable` with keyword argument 
injections:

.. image:: /images/providers/callable.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/callable_kwargs.py
   :language: python

Callable providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Callable` provider could be delegated to any other provider via any 
kind of injection. Delegation of :py:class:`Callable` providers is the same as 
:py:class:`Factory` and :py:class:`Singleton` providers delegation, please 
follow *Factory providers delegation* section for example.

:py:class:`Callable` delegate could be created obviously using 
``Delegate(Callable(...))`` or by calling ``Callable(...).delegate()`` method.

Example:

.. literalinclude:: ../../examples/providers/callable_delegation.py
   :language: python
