Writing custom providers
------------------------

List of *Objects* providers could be widened with custom providers.

Below are some tips and recommendations that have to be met:

    1. Every custom provider has to extend base provider class -
       ``objects.providers.Provider``.
    2. Cusom provider's ``__init__()`` could be overriden with only condition: 
       parent initializer (``objects.providers.Provider.__init__()``) has
       to be called.
    3. Providing strategy has to be implemented in custom provider's 
       ``_provide()`` method. All ``*args`` & ``**kwargs`` that will be
       recieved by ``objects.providers.Provider.__call__()`` will be transefed 
       to custom provider's ``_provide()``. 
    4. If custom provider is based on some standard providers, it is better to
       use delegation of standard providers, then extending of them.
    5. If custom provider defines any attributes, it is good to list them in 
       ``__slots__`` attribute (as *Objects* does). It can save some memory.
    6. If custom provider deals with injections (e.g. ``Factory``, 
       ``Singleton`` providers), it is strongly recommended to use 
       ``objects.injections.Injection`` and its subclasses:
       ``objects.injections.KwArg``, ``objects.injections.Attribute`` and 
       ``objects.injections.Method``. 

Example:

.. image:: /images/providers/custom_provider.png
    :width: 100%
    :align: center

.. code-block:: python

    """Custom `Factory` example."""

    from objects.providers import Provider
    from objects.providers import Factory


    class User(object):

        """Example class User."""


    class UsersFactory(Provider):

        """Example users factory."""

        __slots__ = ('_factory',)

        def __init__(self):
            """Initializer."""
            self._factory = Factory(User)
            super(UsersFactory, self).__init__()

        def _provide(self, *args, **kwargs):
            """Return provided instance."""
            return self._factory(*args, **kwargs)


    # Users factory:
    users_factory = UsersFactory()

    # Creating several User objects:
    user1 = users_factory()
    user2 = users_factory()

    # Making some asserts:
    assert isinstance(user1, User)
    assert isinstance(user2, User)
    assert user1 is not user2

