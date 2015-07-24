"""`Callable` providers delegation example."""

import sys

from objects.providers import Callable
from objects.providers import Delegate


# Some callable provider and few delegates of it:
callable_provider = Callable(sys.exit)
callable_provider_delegate1 = callable_provider.delegate()
callable_provider_delegate2 = Delegate(callable_provider)

# Making some asserts:
assert callable_provider_delegate1() is callable_provider
assert callable_provider_delegate2() is callable_provider
