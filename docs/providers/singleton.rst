Singleton providers
-------------------

``Singleton`` provider creates new instance of specified class on first call
and returns same instance on every next call.

Example:

.. image:: /images/providers/singleton.png
    :width: 80%
    :align: center

.. literalinclude:: ../../examples/providers/singleton.py
   :language: python

Singleton providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Singleton`` providers use ``Factory`` providers for first creation of
specified class instance, so, all of the rules about injections are the same,
as for ``Factory`` providers.

.. image:: /images/providers/singleton_internals.png
    :width: 80%
    :align: center

.. note::

    Due that ``Singleton`` provider creates specified class instance only on
    the first call, all injections are done once, during the first call, also.
    Every next call, while instance has been already created and memorized, no
    injections are done, ``Singleton`` provider just returns memorized earlier
    instance.

    This may cause some problems, for example, in case of trying to bind
    ``Factory`` provider with ``Singleton`` provider (provided by dependent
    ``Factory`` instance will be injected only once, during the first call).
    Be aware that such behaviour was made with opened eyes and is not a bug.

    By the way, in such case, ``Delegate`` provider can be useful. It makes
    possible to inject providers *as is*. Please check out full example in
    *Providers delegation* section.

Singleton providers resetting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Created and memorized by ``Singleton`` instance can be reset. Reset of
``Singleton``'s memorized instance is done by clearing reference to it. Further
lifecycle of memorized instance is out of ``Singleton`` provider's control.

Example:

.. literalinclude:: ../../examples/providers/singleton_reseting.py
   :language: python

Singleton providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Singleton`` provider could be delegated to any other provider via any kind of
injection. Delegation of ``Singleton`` providers is the same as ``Factory``
providers delegation, please follow *Factory providers delegation* section for
example.

``Singleton`` delegate could be created obviously using 
``Delegate(Singleton())`` or by calling ``Singleton.delegate()`` method.

Example:

.. literalinclude:: ../../examples/providers/singleton_delegation.py
   :language: python
