"""`Singleton` providers delegation example."""

from dependency_injector.providers import Singleton
from dependency_injector.providers import Delegate


# Some singleton provider and few delegates of it:
singleton_provider = Singleton(object)
singleton_provider_delegate1 = singleton_provider.delegate()
singleton_provider_delegate2 = Delegate(singleton_provider)

# Making some asserts:
assert singleton_provider_delegate1() is singleton_provider
assert singleton_provider_delegate2() is singleton_provider
