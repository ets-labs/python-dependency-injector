Callable providers
------------------

``di.Callable`` provider is a provider that wraps particular callable with
some injections. Every call of this provider returns result of call of initial
callable.

Callable providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``di.Callable`` provider uses keyword argument injections. Keyword argument 
injections are done by passing injectable values as keyword arguments during 
call time.

Context keyword arguments have higher priority than keyword argument 
injections.

Example:

.. image:: /images/providers/callable.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/callable_injections.py
   :language: python

Callable providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``di.Callable`` provider could be delegated to any other provider via any kind 
of injection. Delegation of ``di.Callable`` providers is the same as 
``di.Factory`` and ``di.Singleton`` providers delegation, please follow 
*Factory providers delegation* section for example.

``di.Callable`` delegate could be created obviously using 
``di.Delegate(di.Callable())`` or by calling ``di.Callable.delegate()`` method.

Example:

.. literalinclude:: ../../examples/providers/callable_delegation.py
   :language: python
