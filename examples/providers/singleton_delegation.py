"""`di.Singleton` providers delegation example."""

import dependency_injector as di


# Some singleton provider and few delegates of it:
singleton_provider = di.Singleton(object)
singleton_provider_delegate1 = singleton_provider.delegate()
singleton_provider_delegate2 = di.Delegate(singleton_provider)

# Making some asserts:
assert singleton_provider_delegate1() is singleton_provider
assert singleton_provider_delegate2() is singleton_provider
