Callable providers
------------------

``Callable`` provider is a provider that wraps particular callable with
some injections. Every call of this provider returns result of call of initial
callable.

Callable providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Callable`` provider uses ``KwArg`` injections. ``KwArg`` injections are
done by passing injectable values as keyword arguments during call time.

Context keyword arguments have higher priority than ``KwArg`` injections.

Example:

.. image:: /images/providers/callable.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/callable_injections.py
   :language: python

Callable providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Callable`` provider could be delegated to any other provider via any kind of
injection. Delegation of ``Callable`` providers is the same as ``Factory`` and
``Singleton`` providers delegation, please follow *Factory providers 
delegation* section for example.

``Callable`` delegate could be created obviously using 
``Delegate(Callable())`` or by calling ``Callable.delegate()`` method.

Example:

.. literalinclude:: ../../examples/providers/callable_delegation.py
   :language: python
