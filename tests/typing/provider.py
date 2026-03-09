from typing import Any
from typing_extensions import assert_type

from dependency_injector import providers

# Test 1: to check .provided attribute
provider1: providers.Provider[int] = providers.Object(1)
provided1 = provider1.provided
provided_val1 = provided1()
provider1_delegate = provider1.provider
assert_type(provider1, providers.Provider[int])
assert_type(provided1, providers.ProvidedInstance)
assert_type(provided_val1, Any)
assert_type(provider1_delegate, providers.Provider[int])

# Test 2: to check async mode API
provider2 = providers.Provider[Any]()
provider2.enable_async_mode()
provider2.disable_async_mode()
provider2.reset_async_mode()
r1 = provider2.is_async_mode_enabled()
r2 = provider2.is_async_mode_disabled()
r3 = provider2.is_async_mode_undefined()
assert_type(r1, bool)
assert_type(r2, bool)
assert_type(r3, bool)
