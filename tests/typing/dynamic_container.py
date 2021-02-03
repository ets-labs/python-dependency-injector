from typing import Dict

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

# Test 4: to check set_providers()
container4 = containers.DynamicContainer()
container4.set_providers(a=providers.Provider())

# Test 5: to check .dependencies attribute
container5 = containers.DynamicContainer()
dependencies: Dict[str, providers.Provider] = container5.dependencies

# Test 6: to check base class
container6: containers.Container = containers.DynamicContainer()
