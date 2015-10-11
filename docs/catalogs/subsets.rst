Creating catalog subsets
------------------------

``di.AbstractCatalog`` subset is a limited collection of catalog providers. 
While catalog could be used as a centralized place for particular providers 
group, such subsets of catalog providers can be used for creating several 
limited scopes that could be passed to different subsystems.

``di.AbstractCatalog`` subsets could be created by instantiating of particular 
catalog with passing provider names to the constructor.

Example:

.. image:: /images/catalogs/subsets.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/catalogs/subsets.py
   :language: python
