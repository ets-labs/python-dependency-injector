Overriding of providers
-----------------------

Every provider could be overridden by another provider.

This gives opportunity to make system behaviour more flexible in some points.
The main feature is that while your code is using providers, it depends on 
providers, but not on the objects that providers provide. As a result of this, 
you can change providing by provider object to a different one, but still
compatible one, without chaning your previously written code.

Provider overriding functionality has such interface:

.. image:: /images/providers/provider_override.png
    :width: 45%
    :align: center

+ ``di.Provider.override()`` - takes another provider that will be used 
  instead of current provider. This method could be called several times. 
  In such case, last passed provider would be used as overriding one.
+ ``di.Provider.reset_override()`` - resets all overriding providers. Provider 
  starts to behave itself like usual.
+ ``di.Provider.is_overridden`` - bool, ``True`` if provider is overridden.

.. note::

   Actually, initial provider forms stack from overriding providers. There is 
   some, not so common, but still usefull, functionality that could be used:

   + ``di.Provider.last_overriding`` - always keeps reference to last 
     overriding provider.
   + ``di.Provider.reset_last_overriding()`` - remove last overriding provider 
     from stack of overriding providers.

Example:

.. image:: /images/providers/overriding_simple.png
    :width: 80%
    :align: center

.. literalinclude:: ../../examples/providers/overriding_simple.py
   :language: python

Example:

.. image:: /images/providers/overriding_users_model.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/overriding_users_model.py
   :language: python
