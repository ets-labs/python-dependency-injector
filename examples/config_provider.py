"""
Config provider examples.
"""

from objects import AbstractCatalog
from objects.providers import (
    Config,
    NewInstance,
)
from objects.injections import InitArg


# Some example class.
class ObjectA(object):
    def __init__(self, setting_one, setting_two, setting_three):
        self.setting_one = setting_one
        self.setting_two = setting_two
        self.setting_three = setting_three


# Catalog of objects providers.
class Catalog(AbstractCatalog):
    """
    Objects catalog.
    """

    config = Config()
    """ :type: (objects.Config) """

    object_a = NewInstance(ObjectA,
                           InitArg('setting_one', config.SETTING_ONE),
                           InitArg('setting_two', config.SETTING_TWO),
                           InitArg('setting_three', config.GLOBAL.SETTING_THREE))
    """ :type: (objects.Provider) -> ObjectA """


# Setting config value and making some tests.
Catalog.config.update_from({
    'SETTING_ONE': 1,
    'SETTING_TWO': 2,
    'GLOBAL': {
        'SETTING_THREE': 3
    }
})

object_a1 = Catalog.object_a()

assert object_a1.setting_one == 1
assert object_a1.setting_two == 2
assert object_a1.setting_three == 3

# Changing config value one more time and making some tests.
Catalog.config.update_from({
    'SETTING_ONE': 11,
    'SETTING_TWO': 22,
    'GLOBAL': {
        'SETTING_THREE': 33
    }
})

object_a2 = Catalog.object_a()

assert object_a2.setting_one == 11
assert object_a2.setting_two == 22
assert object_a2.setting_three == 33

assert object_a1.setting_one == 1
assert object_a1.setting_two == 2
assert object_a1.setting_three == 3
