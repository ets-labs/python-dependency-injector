Coroutine providers
-------------------

.. currentmodule:: dependency_injector.providers

:py:class:`Coroutine` provider create wrapped coroutine on every call.

:py:class:`Coroutine` provider is designed for making better integration with
``asyncio`` coroutines. In particular, :py:class:`Coroutine` provider returns
``True`` for ``asyncio.iscoroutinefunction()`` checks.

.. note::

    :py:class:`Coroutine` provider works only for Python 3.4+.

Example of usage :py:class:`Coroutine` provider with ``async / await``-based
coroutine:

.. literalinclude:: ../../examples/providers/coroutine_async_await.py
   :language: python
   :linenos:

Coroutine providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Coroutine` provider takes a various number of positional and keyword
arguments that are used as wrapped coroutine injections. Every time, when
:py:class:`Coroutine` provider is called, positional and keyword argument
injections would be passed as coroutine arguments.

Injections are done according to the next rules:

+ All providers (instances of :py:class:`Provider`) are called every time 
  when injection needs to be done.
+ Providers could be injected "as is" (delegated), if it is defined obviously.
  Check out :ref:`coroutine_providers_delegation`.
+ All other injectable values are provided *"as is"*.
+ Positional context arguments will be appended after :py:class:`Coroutine`
  positional injections.
+ Keyword context arguments have priority on :py:class:`Coroutine` keyword
  injections and will be merged over them.

.. note::

    Examples of making injections could be found in API docs -
    :py:class:`Coroutine`.

.. _coroutine_providers_delegation:

Coroutine providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Coroutine` provider could be delegated to any other provider via
any kind of injection. 

Delegation of :py:class:`Coroutine` providers is the same as
:py:class:`Factory` providers delegation, please follow 
:ref:`factory_providers_delegation` section for examples (with exception 
of using :py:class:`DelegatedCoroutine` instead of
:py:class:`DelegatedFactory`).

Abstract coroutine providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`AbstractCoroutine` provider is a :py:class:`Coroutine` provider that
must be explicitly overridden before calling.

Behaviour of :py:class:`AbstractCoroutine` providers is the same as of
:py:class:`AbstractFactory`, please follow :ref:`abstract_factory_providers`
section for examples (with exception of using :py:class:`AbstractCoroutine`
provider instead of :py:class:`AbstractFactory`).

.. disqus::
