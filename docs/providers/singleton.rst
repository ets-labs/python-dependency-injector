Singleton providers
-------------------

.. currentmodule:: dependency_injector.providers

:py:class:`Singleton` provider creates new instance of specified class on 
first call and returns same instance on every next call.

Example:

.. image:: /images/providers/singleton.png
    :width: 80%
    :align: center

.. literalinclude:: ../../examples/providers/singleton.py
   :language: python

Singleton providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Singleton` provider extends :py:class:`Factory` provider, so, all 
of the rules about injections are the same, as for :py:class:`Factory` 
provider.

.. note::

    Due that :py:class:`Singleton` provider creates specified class instance 
    only on the first call, all injections are done once, during the first 
    call, also.  Every next call, while instance has been already created 
    and memorized, no injections are done, :py:class:`Singleton` provider just 
    returns memorized earlier instance.

    This may cause some problems, for example, in case of trying to bind
    :py:class:`Factory` provider with :py:class:`Singleton` provider (provided 
    by dependent :py:class:`Factory` instance will be injected only once, 
    during the first call). Be aware that such behaviour was made with opened 
    eyes and is not a bug.

    By the way, in such case, :py:class:`Delegate` provider can be useful. It 
    makes possible to inject providers *as is*. Please check out full example 
    in *Providers delegation* section.

Singleton providers resetting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Created and memorized by :py:class:`Singleton` instance can be reset. Reset of
:py:class:`Singleton`'s memorized instance is done by clearing reference to 
it.  Further lifecycle of memorized instance is out of :py:class:`Singleton` 
provider's control.

Example:

.. literalinclude:: ../../examples/providers/singleton_reseting.py
   :language: python

Singleton providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Singleton` provider could be delegated to any other provider via 
any kind of injection. Delegation of :py:class:`Singleton` providers is the 
same as :py:class:`Factory` providers delegation, please follow *Factory 
providers delegation* section for example.

:py:class:`Singleton` delegate could be created obviously using 
``Delegate(Singleton(...))`` or by calling ``Singleton(...).delegate()`` 
method.

Example:

.. literalinclude:: ../../examples/providers/singleton_delegation.py
   :language: python

Singleton providers specialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Singleton` provider could be specialized for any kind of needs via 
declaring its subclasses. 

One of such features is a limitation to :py:class:`Singleton` provided type:

.. literalinclude:: ../../examples/providers/singleton_provided_type.py
   :language: python
