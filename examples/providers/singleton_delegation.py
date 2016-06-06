"""`Singleton` providers delegation example."""

import dependency_injector.providers as providers


# Some singleton provider and few delegates of it:
singleton_provider = providers.Singleton(object)
singleton_provider_delegate1 = singleton_provider.delegate()
singleton_provider_delegate2 = providers.Delegate(singleton_provider)

# Making some asserts:
assert singleton_provider_delegate1() is singleton_provider
assert singleton_provider_delegate2() is singleton_provider
