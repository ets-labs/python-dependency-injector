from typing import Any, Dict
from typing_extensions import assert_type

from dependency_injector import containers, providers

# Test 1: to check setattr
container1 = containers.DynamicContainer()
container1.abc = providers.Provider()

# Test 2: to check override()
container2 = containers.DynamicContainer()
container2.override(containers.DynamicContainer())

# Test 3: to check override_providers()
container3 = containers.DynamicContainer()
container3.override_providers(a=providers.Provider())
with container3.override_providers(a=providers.Provider()):
    ...

# Test 4: to check set_providers()
container4 = containers.DynamicContainer()
container4.set_providers(a=providers.Provider())

# Test 5: to check .dependencies attribute
container5 = containers.DynamicContainer()
dependencies = container5.dependencies
assert_type(dependencies, Dict[str, providers.Provider[Any]])

# Test 6: to check base class
# NOTE: Using assignment to check base class instead of exact type
container6: containers.Container = containers.DynamicContainer()
