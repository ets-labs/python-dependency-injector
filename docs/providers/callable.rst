Callable providers
------------------

``Callable`` provider is a provider that decorates particular callable with
some injections. Every call of this provider returns result of call of initial
callable.

``Callable`` provider uses ``KwArg`` injections. ``KwArg`` injections are
done by passing injectable values like keyword arguments during call time.

Context keyword arguments have higher priority than ``KwArg`` injections.

Example:

.. code-block:: python

    """`Callable` providers examples."""

    from objects.providers import Callable
    from objects.providers import Singleton

    from objects.injections import KwArg


    class UserService(object):

        """Example class UserService."""

        def get_by_id(self, id):
            """Return user info by user id."""
            return {'id': id, 'login': 'example_user'}


    def get_user_by_id(user_id, users_service):
        """Example function that has input arg and dependency on database."""
        return users_service.get_by_id(user_id)


    # UserService and get_user_by_id providers:
    users_service = Singleton(UserService)
    get_user_by_id = Callable(get_user_by_id,
                              KwArg('users_service', users_service))

    # Making some asserts:
    assert get_user_by_id(1) == {'id': 1, 'login': 'example_user'}
    assert get_user_by_id(2) == {'id': 2, 'login': 'example_user'}


    # Context keyword arguments priority example:
    class UserServiceMock(object):

        """Example class UserService."""

        def get_by_id(self, id):
            """Return user info by user id."""
            return {'id': id, 'login': 'mock'}


    user_service_mock = UserServiceMock()

    user3 = get_user_by_id(1, users_service=user_service_mock)

    assert user3 == {'id': 1, 'login': 'mock'}

