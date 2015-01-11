"""
Catalog module.
"""

from .providers import Provider


class Catalog(object):
    """
    Object provides catalog.
    """

    def __init__(self, *used_providers):
        """
        Initializer.
        """
        self._clean_unused_providers(used_providers)

    def _clean_unused_providers(self, used_providers):
        """
        Sets every catalog's provider in None except of `used_providers` list.

        :param list|tuple|set used_providers:
        :return:
        """
        used_providers = set(used_providers)
        for attribute_name in set(dir(self.__class__)) - set(dir(Catalog)):
            provider = getattr(self, attribute_name)
            if not isinstance(provider, Provider):
                continue
            if provider not in used_providers:
                setattr(self, attribute_name, None)
