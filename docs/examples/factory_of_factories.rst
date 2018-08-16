Factory of Factories pattern
============================

This example demonstrate implementation of "Factory of Factories" pattern.
Main idea of this pattern is about creation of a :py:class:`Factory` that
creates another :py:class:`Factory` and mix additional arguments to it.

Listing of ``data.py``, demonstrates sample classes structure:

.. literalinclude:: ../../examples/miniapps/factory_patterns/data.py
   :language: python
   :linenos:

Listing of ``factory_of_factories.py``, demonstrates "Chained Factories"
pattern and provide some explanation:

.. literalinclude:: ../../examples/miniapps/factory_patterns/factory_of_factories.py
   :language: python
   :linenos:


.. disqus::
