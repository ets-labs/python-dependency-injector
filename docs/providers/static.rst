Static providers
----------------

.. currentmodule:: dependency_injector.providers

Static providers are family of providers that return their values "as is".
There are four types of static providers:

    - :py:class:`Class`
    - :py:class:`Object`
    - :py:class:`Function`
    - :py:class:`Value`

All of them have the same behaviour (inherited from 
:py:class:`StaticProvider`), but usage of any is predicted by readability 
and providing object's type.

Example:

.. literalinclude:: ../../examples/providers/static.py
   :language: python
   :linenos:
