"""Static providers example."""

from dependency_injector import providers


# Provides class - `object`:
cls_provider = providers.Class(object)
assert cls_provider() is object

# Provides object - `object()`:
object_provider = providers.Object(object())
assert isinstance(object_provider(), object)

# Provides function - `len`:
function_provider = providers.Function(len)
assert function_provider() is len

# Provides value - `123`:
value_provider = providers.Value(123)
assert value_provider() == 123
