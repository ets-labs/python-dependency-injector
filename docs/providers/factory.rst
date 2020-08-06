Factory providers
-----------------

.. currentmodule:: dependency_injector.providers

:py:class:`Factory` provider creates new instance of specified class on every 
call.

Nothing could be better than brief example:

.. image:: /images/providers/factory.png
    :width: 80%
    :align: center

.. literalinclude:: ../../examples/providers/factory.py
   :language: python

Factory providers and __init__ injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Factory` takes a various number of positional and keyword arguments 
that are used as ``__init__()`` injections. Every time, when 
:py:class:`Factory` creates new one instance, positional and keyword 
argument injections would be passed as instance arguments.

Injections are done according to the next rules:

+ All providers (instances of :py:class:`Provider`) are called every time 
  when injection needs to be done.
+ Providers could be injected "as is" (delegated), if it is defined obviously.
  Check out :ref:`factory_providers_delegation`.
+ All other injectable values are provided *"as is"*.
+ Positional context arguments will be appended after :py:class:`Factory` 
  positional injections.
+ Keyword context arguments have priority on :py:class:`Factory` keyword 
  injections and will be merged over them.

For example, if injectable value of injection is a :py:class:`Factory`, it 
will provide new one instance (as a result of its call) every time, when 
injection needs to be done.

Example below is a little bit more complicated. It shows how to create 
:py:class:`Factory` of particular class with ``__init__()`` injections which 
injectable values are also provided by another factories:

.. image:: /images/providers/factory_init_injections.png

.. literalinclude:: ../../examples/providers/factory_init_injections.py
   :language: python

Factory providers and building complex object graphs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use :py:class:`Factory` provider to build complex object graphs.

Consider next example:

.. literalinclude:: ../../examples/providers/factory_deep_init_injections.py
   :language: python

.. note::

   You can use ``__`` separator in the name of the keyword argument to pass the value to the child
   factory, e.g. ``algorithm_factory(task__loss__regularizer__alpha=0.5)``.

.. _factory_providers_delegation:

Factory providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Factory` provider could be delegated to any other provider via any 
kind of injection. 

As it was mentioned earlier, if :py:class:`Factory` is 
injectable value, it will be called every time when injection needs to be 
done. But sometimes there is a need to inject :py:class:`Factory` provider 
itself (not a result of its call) as a dependency. Such injections are called 
- *delegated provider injections*.
  
Saying in other words, delegation of factories - is a way to inject factories 
themselves, instead of results of their calls. 

:py:class:`Factory` delegation is performed by wrapping delegated 
:py:class:`Factory` into special provider type - :py:class:`Delegate`, that 
just returns wrapped :py:class:`Factory`. 

Actually, there are three ways for creating factory delegates:

+ ``DelegatedFactory(...)`` - use special type of factory - 
  :py:class:`DelegatedFactory`. Such factories are always injected as 
  delegates ("as is"). 
+ ``Delegate(Factory(...))`` - obviously wrapping factory into 
  :py:class:`Delegate` provider.
+ ``Factory(...).delegate()`` - calling factory :py:meth:`Factory.delegate` 
  method, that returns delegate wrapper for current factory.
+ ``Factory(...).provider`` - getting factory :py:attr:`Factory.provider` 
  attribute, that returns delegate wrapper for current factory (alias of 
  ``Factory(...).delegate()`` method).

Example:

.. image:: /images/providers/factory_delegation.png
    :width: 85%
    :align: center

.. literalinclude:: ../../examples/providers/factory_delegation.py
   :language: python

.. _factory_providers_specialization:

Factory providers specialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Factory` provider could be specialized for any kind of needs via 
creating its subclasses. 

One of such specialization features is a limitation to :py:class:`Factory` 
provided type:

.. literalinclude:: ../../examples/providers/factory_provided_type.py
   :language: python

.. _abstract_factory_providers:

Abstract factory providers
~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`AbstractFactory` provider is a :py:class:`Factory` provider that
must be explicitly overridden before calling.

.. note::

    Overriding of :py:class:`AbstractFactory` provider is possible only by
    another :py:class:`Factory` provider.

:py:class:`AbstractFactory` provider is useful when it is needed to specify
explicitly that it only provides abstraction, but not an implementation.
Client code must override such factories with factories that provide particular
implementations. Otherwise, :py:class:`AbstractFactory` will raise an error
on attempt of calling it. At the same time, :py:class:`AbstractFactory` is
regular provider that could be injected into other providers (or used for
any other kind of bindings) without being overridden. After
:py:class:`AbstractFactory` provider has been overridden, its behaviour is
identical to regular :py:class:`Factory` provider.

Example:

.. image:: /images/providers/abstract_factory.png
    :width: 100%
    :align: center

Listing of ``cache.py``:

.. literalinclude:: ../../examples/providers/abstract_factory/cache.py
   :language: python

Listing of ``example.py``:

.. literalinclude:: ../../examples/providers/abstract_factory/example.py
   :language: python

Factory aggregate providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`FactoryAggregate` provider is a special type of provider that 
aggregates other :py:class:`Factory` providers.

.. note::

    :py:class:`FactoryAggregate` is not overridable. Calling of 
    :py:meth:`FactoryAggregate.override` will result in raising of an 
    exception.

Next prototype might be the best demonstration of 
:py:class:`FactoryAggregate` features:

.. literalinclude:: ../../examples/providers/factory_aggregate/prototype.py
   :language: python

Example below shows one of the :py:class:`FactoryAggregate` use cases, when 
concrete implementation (game) must be selected based on dynamic input (CLI). 

Listing of ``games.py``:

.. literalinclude:: ../../examples/providers/factory_aggregate/games.py
   :language: python

Listing of ``example.py``:

.. literalinclude:: ../../examples/providers/factory_aggregate/example.py
   :language: python

.. disqus::
