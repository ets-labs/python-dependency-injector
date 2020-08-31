Factory provider
----------------

.. currentmodule:: dependency_injector.providers

:py:class:`Factory` provider creates new objects.

.. literalinclude:: ../../examples/providers/factory.py
   :language: python
   :lines: 3-

The first argument of the ``Factory`` provider is a class, a factory function or a method
that creates an object.

The rest of the ``Factory`` positional and keyword arguments are the dependencies.
``Factory`` injects the dependencies every time when creates a new object. The dependencies are
injected following these rules:

+ If the dependency is a provider, this provider is called and the result of the call is injected.
+ If you need to inject the provider itself, you should use the ``.provider`` attribute. More at
  :ref:`factory_providers_delegation`.
+ All other dependencies are injected *"as is"*.
+ Positional context arguments are appended after ``Factory`` positional dependencies.
+ Keyword context arguments have the priority over the ``Factory`` keyword dependencies with the
  same name.

.. image:: images/factory_init_injections.png

.. literalinclude:: ../../examples/providers/factory_init_injections.py
   :language: python
   :lines: 3-

Passing arguments to the underlying providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Factory`` provider can pass the arguments to the underlying providers. This helps when you need
to assemble a nested objects graph and pass the arguments deep inside.

Consider the example:

.. image:: images/factory_init_injections_underlying.png

To create an ``Algorithm`` you need to provide all the dependencies: ``ClassificationTask``,
``Loss``, and ``Regularizer``. The last object in the chain, the ``Regularizer`` has a dependency
on the ``alpha`` value. The ``alpha`` value varies from algorithm to algorithm:

.. code-block:: python

   Algorithm(
       task=ClassificationTask(
           loss=Loss(
               regularizer=Regularizer(
                   alpha=alpha,  # <-- the dependency
               ),
           ),
       ),
   )


``Factory`` provider helps to deal with the such assembly. You need to create the factories for
all the classes and use special double-underscore ``__`` syntax for passing the ``alpha`` argument:

.. literalinclude:: ../../examples/providers/factory_init_injections_underlying.py
   :language: python
   :lines: 3-
   :emphasize-lines: 24-35,39,42,45

When you use ``__`` separator in the name of the keyword argument the ``Factory`` looks for
the dependency with the same name as the left part of the ``__`` expression.

.. code-block::

   <dependency>__<keyword for the underlying provider>=<value>

If ``<dependency>`` is found the underlying provider will receive the
``<keyword for the underlying provider>=<value>`` as an argument.

.. _factory_providers_delegation:

Passing providers to the objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you need to inject the provider itself, but not the result of its call, use the ``.provider``
attribute of the provider that you're going to inject.

.. image:: images/factory_delegation.png

.. literalinclude:: ../../examples/providers/factory_delegation.py
   :language: python
   :lines: 3-
   :emphasize-lines: 25

.. note:: Any provider has a ``.provider`` attribute.

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
