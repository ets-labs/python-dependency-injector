"""
Injections module.
"""


class Injection(object):
    """
    Base injection class.
    """

    def __init__(self, name, injectable):
        """
        Initializer.
        """
        self.name = name
        self.injectable = injectable

    @classmethod
    def fetch(cls, injections):
        """
        Fetches injections of self type from list.
        """
        return tuple([injection
                      for injection in injections
                      if isinstance(injection, cls)])


class InitArg(Injection):
    """
    Init argument injection.
    """


class Attribute(Injection):
    """
    Attribute injection.
    """


class Method(Injection):
    """
    Method injection.
    """
