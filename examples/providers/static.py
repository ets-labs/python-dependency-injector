"""Static providers example."""

import dependency_injector as di


# Provides class - `object`:
cls_provider = di.Class(object)
assert cls_provider() is object

# Provides object - `object()`:
object_provider = di.Object(object())
assert isinstance(object_provider(), object)

# Provides function - `len`:
function_provider = di.Function(len)
assert function_provider() is len

# Provides value - `123`:
value_provider = di.Value(123)
assert value_provider() == 123
