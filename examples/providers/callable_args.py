"""`Callable` providers with positional arguments example."""

import dependency_injector.providers as providers


# Creating even and odd filter providers:
even_filter = providers.Callable(filter, lambda x: x % 2 == 0)
odd_filter = providers.Callable(filter, lambda x: x % 2 != 0)

# Creating even and odd ranges using xrange() and filter providers:
even_range = even_filter(xrange(1, 10))
odd_range = odd_filter(xrange(1, 10))

# Making some asserts:
assert even_range == [2, 4, 6, 8]
assert odd_range == [1, 3, 5, 7, 9]
