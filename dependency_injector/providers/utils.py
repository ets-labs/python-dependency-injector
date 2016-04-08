"""Dependency injector provider utils."""


class OverridingContext(object):
    """Provider overriding context.

    :py:class:`OverridingContext` is used by :py:meth:`Provider.override` for
    implemeting ``with`` contexts. When :py:class:`OverridingContext` is
    closed, overriding that was created in this context is dropped also.

    .. code-block:: python

        with provider.override(another_provider):
            assert provider.is_overridden
        assert not provider.is_overridden
    """

    def __init__(self, overridden, overriding):
        """Initializer.

        :param overridden: Overridden provider.
        :type overridden: :py:class:`Provider`

        :param overriding: Overriding provider.
        :type overriding: :py:class:`Provider`
        """
        self.overridden = overridden
        self.overriding = overriding

    def __enter__(self):
        """Do nothing."""
        return self.overriding

    def __exit__(self, *_):
        """Exit overriding context."""
        self.overridden.reset_last_overriding()


def override(overridden):
    """Decorator for overriding providers.

    This decorator overrides ``overridden`` provider by decorated one.

    .. code-block:: python

        @Factory
        class SomeClass(object):
            pass


        @override(SomeClass)
        @Factory
        class ExtendedSomeClass(SomeClass.cls):
            pass

    :param overridden: Provider that should be overridden.
    :type overridden: :py:class:`Provider`

    :return: Overriding provider.
    :rtype: :py:class:`Provider`
    """
    def decorator(overriding):
        overridden.override(overriding)
        return overriding
    return decorator
