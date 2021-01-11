from dependency_injector import providers


# Test 1: to check .provided attribute
provider1: providers.Provider[int] = providers.Object(1)
provided: providers.ProvidedInstance = provider1.provided

# Test 2: to check async mode API
provider2: providers.Provider = providers.Provider()
provider2.enable_async_mode()
provider2.disable_async_mode()
provider2.reset_async_mode()
r1: bool = provider2.is_async_mode_enabled()
r2: bool = provider2.is_async_mode_disabled()
r3: bool = provider2.is_async_mode_undefined()
