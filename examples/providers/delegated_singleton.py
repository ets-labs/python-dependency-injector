"""`DelegatedSingleton` providers example."""

from dependency_injector import providers


# Some delegated singleton provider:
singleton_provider = providers.DelegatedSingleton(object)
registry = providers.DelegatedSingleton(dict,
                                        object1=singleton_provider,
                                        object2=singleton_provider)

# Getting several references to singleton object:
registry = registry()
singleton_object1 = registry['object1']()
singleton_object2 = registry['object2']()

# Making some asserts:
assert singleton_object1 is singleton_object2
