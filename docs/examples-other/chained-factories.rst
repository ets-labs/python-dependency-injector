Chained Factories pattern
=========================

This example demonstrates "Chained Factories" pattern.

The idea of the pattern is in wrapping ``Factory`` into another ``Factory`` that adds
additional arguments.

.. code-block:: python

   base_factory = providers.Factory(
       SomeClass,
       base_argument=1,
   )

   concrete_factory = providers.Factory(
       base_factory,
       extra_argument=2,
   )


   if __name__ == "__main__":
       instance = concrete_factory()
       # Same as: # instance = SomeClass(base_argument=1, extra_argument=2)

Sample code
-----------

Listing of the pattern example:

.. literalinclude:: ../../examples/miniapps/factory-patterns/chained_factories.py
   :language: python

Arguments priority
------------------

Passing of the arguments works the same way like for any other :ref:`factory-provider`.

.. code-block:: python

   # 1. Keyword arguments of upper level factory are added to lower level factory
   chained_dict_factory = providers.Factory(
       providers.Factory(dict, arg1=1),
       arg2=2,
   )
   print(chained_dict_factory())  # prints: {"arg1": 1, "arg2": 2}

   # 2. Keyword arguments of upper level factory have priority
   chained_dict_factory = providers.Factory(
       providers.Factory(dict, arg1=1),
       arg1=2,
   )
   print(chained_dict_factory())  # prints: {"arg1": 2}

   # 3. Keyword arguments provided from context have the most priority
   chained_dict_factory = providers.Factory(
       providers.Factory(dict, arg1=1),
       arg1=2,
   )
   print(chained_dict_factory(arg1=3))  # prints: {"arg1": 3}


Credits
-------

The "Chained Factories" pattern was suggested by the ``Dependency Injector`` users.

.. disqus::
