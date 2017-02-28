Callable providers
------------------

.. currentmodule:: dependency_injector.providers

:py:class:`Callable` provider calls wrapped callable on every call.

Callable providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Callable` provider takes a various number of positional and keyword 
arguments that are used as wrapped callable injections. Every time, when 
:py:class:`Callable` provider is called, positional and keyword argument 
injections would be passed as an callable arguments.

Injections are done according to the next rules:

+ All providers (instances of :py:class:`Provider`) are called every time 
  when injection needs to be done.
+ Providers could be injected "as is" (delegated), if it is defined obviously.
  Check out :ref:`callable_providers_delegation`.
+ All other injectable values are provided *"as is"*.
+ Positional context arguments will be appended after :py:class:`Callable` 
  positional injections.
+ Keyword context arguments have priority on :py:class:`Callable` keyword 
  injections and will be merged over them.

Example that shows usage of :py:class:`Callable` with positional argument 
injections:

.. literalinclude:: ../../examples/providers/callable_args.py
   :language: python
   :linenos:

Next one example shows usage of :py:class:`Callable` with keyword argument 
injections:

.. image:: /images/providers/callable.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/callable_kwargs.py
   :language: python
   :linenos:

.. _callable_providers_delegation:

Callable providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Callable` provider could be delegated to any other provider via 
any kind of injection. 

Delegation of :py:class:`Callable` providers is the same as 
:py:class:`Factory` providers delegation, please follow 
:ref:`factory_providers_delegation` section for examples (with exception 
about using :py:class:`DelegatedCallable` instead of 
:py:class:`DelegatedFactory`).


.. disqus::
