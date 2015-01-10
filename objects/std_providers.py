"""
Standard providers.
"""

from .injections import InitArg, Attribute, Method


class Provider(object):
    """
    Base provider class.
    """

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        raise NotImplementedError()

    @staticmethod
    def prepare_injections(injections):
        """
        Prepares injections list to injection.
        """
        prepared_injections = dict()
        for injection in injections:
            if isinstance(injection.injectable, Provider):
                value = injection.injectable.__call__()
            else:
                value = injection.injectable
            prepared_injections[injection.name] = value
        return prepared_injections


class NewInstance(Provider):
    """
    New instance providers will create and return new instance on every call.
    """

    def __init__(self, provides, *injections):
        """
        Initializer.
        """
        self.provides = provides
        self.init_injections = InitArg.fetch(injections)
        self.attribute_injections = Attribute.fetch(injections)
        self.method_injections = Method.fetch(injections)

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        init_injections = Provider.prepare_injections(self.init_injections)
        init_injections.update(kwargs)

        provided = self.provides(*args, **init_injections)

        attribute_injections = Provider.prepare_injections(
            self.attribute_injections)
        for name, injectable in attribute_injections.iteritems():
            setattr(provided, name, injectable)

        method_injections = Provider.prepare_injections(self.method_injections)
        for name, injectable in method_injections.iteritems():
            getattr(provided, name)(injectable)

        return provided


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
