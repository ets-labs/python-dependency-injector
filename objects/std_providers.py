"""
Standard providers.
"""


class Provider(object):
    """
    Base provider class.
    """

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        raise NotImplementedError()


class NewInstance(Provider):
    """
    New instance providers will create and return new instance on every call.
    """

    def __init__(self, provides, **dependencies):
        """
        Initializer.
        """
        self.provides = provides
        self.dependencies = dependencies

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        for name, dependency in self.dependencies.iteritems():
            if name in kwargs:
                continue

            if isinstance(dependency, Provider):
                value = dependency.__call__()
            else:
                value = dependency

            kwargs[name] = value
        return self.provides(*args, **kwargs)


class Singleton(NewInstance):
    """
    Singleton provider will create instance once and return it on every call.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializer.
        """
        self.instance = None
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        if not self.instance:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance


class _StaticProvider(Provider):
    """
    Static provider is base implementation that provides exactly the same as
    it got on input.
    """

    def __init__(self, provides):
        """
        Initializer.
        """
        self.provides = provides

    def __call__(self):
        """
        Returns provided instance.
        """
        return self.provides


class Class(_StaticProvider):
    """
    Class provider provides class.
    """


class Object(_StaticProvider):
    """
    Object provider provides object.
    """


class Function(_StaticProvider):
    """
    Function provider provides function.
    """


class Value(_StaticProvider):
    """
    Value provider provides value.
    """
