.. _factory-provider:

Factory provider
================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Factory,Abstract Factory,
              Pattern,Example,Aggregate
   :description: Factory provider helps to implement dependency injection in Python. This page
                 demonstrates how to use Factory provider, inject the dependencies, and assemble
                 object graphs passing the injections deep inside. It also provides the examples
                 of the Abstract Factory pattern & provider and Factories Aggregation pattern.

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

``Factory`` provider can inject attributes. Use ``.add_attributes()`` method to specify
attribute injections.

.. literalinclude:: ../../examples/providers/factory_attribute_injections.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18-18

Passing arguments to the underlying providers
---------------------------------------------

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
   :emphasize-lines: 44,49

When you use ``__`` separator in the name of the keyword argument the ``Factory`` looks for
the dependency with the same name as the left part of the ``__`` expression.

.. code-block:: none

   <dependency>__<keyword for the underlying provider>=<value>

If ``<dependency>`` is found the underlying provider will receive the
``<keyword for the underlying provider>=<value>`` as an argument.

.. _factory_providers_delegation:

Passing providers to the objects
--------------------------------

When you need to inject the provider itself, but not the result of its call, use the ``.provider``
attribute of the provider that you're going to inject.

.. image:: images/factory_delegation.png

.. literalinclude:: ../../examples/providers/factory_delegation.py
   :language: python
   :lines: 3-
   :emphasize-lines: 28

.. note:: Any provider has a ``.provider`` attribute.

.. _factory-string-imports:

String imports
--------------

``Factory`` provider can handle string imports:

.. code-block:: python

   class Container(containers.DeclarativeContainer):

       service = providers.Factory("myapp.mypackage.mymodule.Service")

You can also make a relative import:

.. code-block:: python

   # in myapp/container.py

   class Container(containers.DeclarativeContainer):

       service = providers.Factory(".mypackage.mymodule.Service")

or import a member of the current module just specifying its name:

.. code-block:: python

   class Service:
       ...


   class Container(containers.DeclarativeContainer):

       service = providers.Factory("Service")

.. note::
   ``Singleton``, ``Callable``, ``Resource``, and ``Coroutine`` providers handle string imports
   the same way as a ``Factory`` provider.

.. _factory-specialize-provided-type:

Specializing the provided type
------------------------------

You can create a specialized ``Factory`` provider that provides only specific type. For doing
this you need to create a subclass of the ``Factory`` provider and define the ``provided_type``
class attribute.

.. literalinclude:: ../../examples/providers/factory_provided_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12-14

.. _abstract-factory:

Abstract factory
----------------

:py:class:`AbstractFactory` provider helps when you need to create a provider of some base class
and the particular implementation is not yet know. ``AbstractFactory`` provider is a ``Factory``
provider with two peculiarities:

+ Provides only objects of a specified type.
+ Must be overridden before usage.

.. image:: images/abstract_factory.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/abstract_factory.py
   :language: python
   :lines: 3-
   :emphasize-lines: 34

.. _factory-aggregate-provider:

Factory aggregate
-----------------

:py:class:`FactoryAggregate` provider aggregates multiple factories.

.. seealso::
   :ref:`aggregate-provider` – it's a successor of ``FactoryAggregate`` provider that can aggregate
   any type of provider, not only ``Factory``.

The aggregated factories are associated with the string keys. When you call the
``FactoryAggregate`` you have to provide one of the these keys as a first argument.
``FactoryAggregate`` looks for the factory with a matching key and calls it with the rest of the arguments.

.. image:: images/factory_aggregate.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/factory_aggregate.py
   :language: python
   :lines: 3-
   :emphasize-lines: 33-37,47

You can get a dictionary of the aggregated providers using ``.providers`` attribute.
To get a game provider dictionary from the previous example you can use
``game_factory.providers`` attribute.

You can also access an aggregated factory as an attribute. To create the ``Chess`` object from the
previous example you can do ``chess = game_factory.chess("John", "Jane")``.

.. note::
   You can not override the ``FactoryAggregate`` provider.

.. note::
   When you inject the ``FactoryAggregate`` provider it is passed "as is".

To use non-string keys or string keys with ``.`` and ``-``, you can provide a dictionary as a positional argument:

.. code-block:: python

   providers.FactoryAggregate({
       SomeClass: providers.Factory(...),
       "key.with.periods": providers.Factory(...),
       "key-with-dashes": providers.Factory(...),
   })

Example:

.. literalinclude:: ../../examples/providers/factory_aggregate_non_string_keys.py
   :language: python
   :lines: 3-
   :emphasize-lines: 30-33,39-40


.. disqus::
