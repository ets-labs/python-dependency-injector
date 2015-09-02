Static providers
----------------

Static providers are family of providers that return their values "as is".
There are four types of static providers:

    - ``di.Class``
    - ``di.Object``
    - ``di.Function``
    - ``di.Value``

All of them have the same behaviour, but usage of anyone is predicted by
readability and providing object's type.

Example:

.. literalinclude:: ../../examples/providers/static.py
   :language: python
