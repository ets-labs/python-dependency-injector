Singleton providers
-------------------

``Singleton`` provider creates new instance of specified class on first call
and returns same instance on every next call.

.. code-block:: python

    """`Singleton` providers example."""

    from objects.providers import Singleton


    class UserService(object):

        """Example class UserService."""


    # Singleton provider creates new instance of specified class on first call and
    # returns same instance on every next call.
    users_service_provider = Singleton(UserService)

    # Retrieving several UserService objects:
    user_service1 = users_service_provider()
    user_service2 = users_service_provider()

    # Making some asserts:
    assert user_service1 is user_service2
    assert isinstance(user_service1, UserService)
    assert isinstance(user_service2, UserService)


Singleton providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Singleton`` providers use ``Factory`` providers for first creation of
specified class instance, so, all of the rules about injections are the same,
as for ``Factory`` providers.

.. note::

    Due that ``Singleton`` provider creates specified class instance only on
    the first call, all injections are done once, during the first call, also.
    Every next call, while instance has been already created and memorized, no
    injections are done, ``Singleton`` provider just returns memorized earlier
    instance.

    This may cause some problems, for example, in case of trying to bind
    ``Factory`` provider with ``Singleton`` provider (provided by dependent
    ``Factory`` instance will be injected only once, during the first call).
    Be aware that such behaviour was made with opened eyes and is not a bug.

    By the way, in such case, ``Delegate`` provider can be useful. It makes
    possible to inject providers *as is*. Please check out full example in
    *Providers delegation* section.

Singleton providers resetting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Created and memorized by ``Singleton`` instance can be reset. Reset of
``Singleton``'s memorized instance is done by clearing reference to it. Further
lifecycle of memorized instance is out of ``Singleton`` provider's control.

.. code-block:: python

    """`Singleton` providers resetting example."""

    from objects.providers import Singleton


    class UserService(object):

        """Example class UserService."""


    # Singleton provider creates new instance of specified class on first call and
    # returns same instance on every next call.
    users_service_provider = Singleton(UserService)

    # Retrieving several UserService objects:
    user_service1 = users_service_provider()
    user_service2 = users_service_provider()

    # Making some asserts:
    assert user_service1 is user_service2
    assert isinstance(user_service1, UserService)
    assert isinstance(user_service2, UserService)

    # Resetting of memorized instance:
    users_service_provider.reset()

    # Retrieving one more UserService object:
    user_service3 = users_service_provider()

    # Making some asserts:
    assert user_service3 is not user_service1

