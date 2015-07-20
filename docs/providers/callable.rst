Callable providers
------------------

``Callable`` provider is a provider that wraps particular callable with
some injections. Every call of this provider returns result of call of initial
callable.

Callable providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Callable`` provider uses ``KwArg`` injections. ``KwArg`` injections are
done by passing injectable values as keyword arguments during call time.

Context keyword arguments have higher priority than ``KwArg`` injections.

Example:

.. image:: /images/callable.png
    :width: 100%
    :align: center

.. code-block:: python

    """`Callable` providers example."""

    from passlib.hash import sha256_crypt

    from objects.providers import Callable
    from objects.injections import KwArg


    # Password hasher and verifier providers (hash function could be changed
    # anytime (for example, to sha512) without any changes in client's code):
    password_hasher = Callable(sha256_crypt.encrypt,
                               KwArg('salt_size', 16),
                               KwArg('rounds', 10000))
    password_verifier = Callable(sha256_crypt.verify)

    # Making some asserts (client's code):
    hashed_password = password_hasher('super secret')
    assert password_verifier('super secret', hashed_password)

Callable providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Callable`` provider could be delegated to any other provider via any kind of
injection. Delegation of ``Callable`` providers is the same as ``Factory`` and
``Singleton`` providers delegation, please follow *Factory providers 
delegation* section for example.

``Callable`` delegate could be created obviously using 
``Delegate(Callable())`` or by calling ``Callable.delegate()`` method.

Example:

.. code-block:: python

    """`Callable` providers delegation example."""

    import sys

    from objects.providers import Callable
    from objects.providers import Delegate


    # Some callable provider and few delegates of it:
    callable_provider = Callable(sys.exit)
    callable_provider_delegate1 = callable_provider.delegate()
    callable_provider_delegate2 = Delegate(callable_provider)

    # Making some asserts:
    assert callable_provider_delegate1() is callable_provider
    assert callable_provider_delegate2() is callable_provider
