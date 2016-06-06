"""`Callable` providers delegation example."""

import sys
import dependency_injector.providers as providers


# Creating some callable provider and few delegates of it:
callable_provider = providers.Callable(sys.exit)
callable_provider_delegate1 = callable_provider.delegate()
callable_provider_delegate2 = providers.Delegate(callable_provider)

# Making some asserts:
assert callable_provider_delegate1() is callable_provider
assert callable_provider_delegate2() is callable_provider
