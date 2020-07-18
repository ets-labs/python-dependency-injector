Chained Factories pattern
=========================

This example demonstrate implementation of "Chained Factories" pattern.
Main idea of this pattern is about wrapping :py:class:`Factory` into
another :py:class:`Factory` that mix additional arguments or keyword
arguments to a wrapped one.

Listing of ``data.py``, demonstrates sample classes structure:

.. literalinclude:: ../../examples/miniapps/factory_patterns/data.py
   :language: python

Listing of ``chained_factories.py``, demonstrates "Chained Factories"
pattern and provide some explanation:

.. literalinclude:: ../../examples/miniapps/factory_patterns/chained_factories.py
   :language: python


.. disqus::
