"""
`Objects` library.
"""


class Catalog(object):
    def __init__(self, *args):
        args = set(args)
        for attribute_name in set(dir(self.__class__)) - set(dir(Catalog)):
            provider = getattr(self, attribute_name)
            if not isinstance(provider, Provider):
                continue
            if provider not in args:
                setattr(self, attribute_name, None)


class Provider(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class NewInstance(Provider):
    def __init__(self, provides, **dependencies):
        self.provides = provides
        self.dependencies = dependencies

    def __call__(self, *args, **kwargs):
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
    def __init__(self, *args, **kwargs):
        self.instance = None
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if not self.instance:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance
