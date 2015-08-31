Writing custom providers
------------------------

List of *Dependency Injector* providers could be widened with custom providers.

Below are some tips and recommendations that have to be met:

    1. Every custom provider has to extend base provider class -
       ``dependency_injector.providers.Provider``.
    2. Cusom provider's ``__init__()`` could be overriden with only condition: 
       parent initializer 
       (``dependency_injector.providers.Provider.__init__()``) has to be called.
    3. Providing strategy has to be implemented in custom provider's 
       ``_provide()`` method. All ``*args`` & ``**kwargs`` that will be
       recieved by ``dependency_injector.providers.Provider.__call__()`` will be
       transefed 
       to custom provider's ``_provide()``. 
    4. If custom provider is based on some standard providers, it is better to
       use delegation of standard providers, then extending of them.
    5. If custom provider defines any attributes, it is good to list them in 
       ``__slots__`` attribute (as *Dependency Injector* does). It can save 
       some memory.
    6. If custom provider deals with injections (e.g. ``Factory``, 
       ``Singleton`` providers), it is strongly recommended to use 
       ``dependency_injector.injections.Injection`` and its subclasses:
       ``dependency_injector.injections.KwArg``, 
       ``dependency_injector.injections.Attribute`` and 
       ``dependency_injector.injections.Method``. 

Example:

.. image:: /images/providers/custom_provider.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/providers/custom_factory.py
   :language: python
