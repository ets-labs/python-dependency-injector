Factory of Factories pattern
============================

This example demonstrates "Factory of Factories" pattern.

The idea of the pattern is in creating a ``Factory`` that creates another ``Factory`` and adds
additional arguments.

.. code-block:: python

   base_factory = providers.Factory(
       providers.Factory
       SomeClass,
       base_argument=1,
   )

   concrete_factory = providers.Factory(
       OtherClass,
       instance=base_factory(extra_argument=1),
   )


   if __name__ == "__main__":
       instance = concrete_factory()
       # Same as: # instance = SomeClass(base_argument=1, extra_argument=2)

Sample code
-----------

Listing of the pattern example:

.. literalinclude:: ../../examples/miniapps/factory-patterns/factory_of_factories.py
   :language: python

Arguments priority
------------------

Passing of the arguments works the same way like for any other :ref:`factory-provider`.

.. code-block:: python

   # 1. Keyword arguments of upper level factory are added to lower level factory
   factory_of_dict_factories = providers.Factory(
       providers.Factory,
       dict,
       arg1=1,
   )
   dict_factory = factory_of_dict_factories(arg2=2)
   print(dict_factory())  # prints: {"arg1": 1, "arg2": 2}

   # 2. Keyword arguments of upper level factory have priority
   factory_of_dict_factories = providers.Factory(
       providers.Factory,
       dict,
       arg1=1,
   )
   dict_factory = factory_of_dict_factories(arg1=2)
   print(dict_factory())  # prints: {"arg1": 2}

   # 3. Keyword arguments provided from context have the most priority
   factory_of_dict_factories = providers.Factory(
       providers.Factory,
       dict,
       arg1=1,
   )
   dict_factory = factory_of_dict_factories(arg1=2)
   print(dict_factory(arg1=3))  # prints: {"arg1": 3}

Credits
-------

The "Factory of Factories" pattern was suggested by the ``Dependency Injector`` users.

.. disqus::
