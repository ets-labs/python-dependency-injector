Writing of custom providers
---------------------------

.. currentmodule:: dependency_injector.providers

List of *Dependency Injector* providers could be widened with custom providers.

Below are some tips and recommendations that have to be met:

    1. Every custom provider has to extend base provider class - 
       :py:class:`Provider`.
    2. Cusom provider's ``__init__()`` could be overriden, but parent's
       initializer (:py:meth:`Provider.__init__`) has to be called.
    3. Providing strategy has to be implemented in custom provider's 
       :py:meth:`Provider._provide` method. All ``*args`` & ``**kwargs`` 
       that will be recieved by :py:meth:`Provider.__call__` will be 
       transefed to custom provider's :py:meth:`Provider._provide`. 
    4. If custom provider is based on some standard providers, it is better to
       use delegation of standard providers, then extending of them.
    5. If custom provider defines any attributes, it is good to list them in 
       ``__slots__`` attribute (as *Dependency Injector* does). It can save 
       some memory.
    6. If custom provider deals with injections, it is strongly recommended 
       to be consistent with :py:class:`Factory`, :py:class:`Singleton` and 
       :py:class:`Callable` providers style. 

Example:

.. image:: /images/providers/custom_provider.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/custom_factory.py
   :language: python
   :linenos:
