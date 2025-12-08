from typing import Any
from typing_extensions import assert_type

from dependency_injector import providers

# Test 1: to check the getattr type
provider1 = providers.DependenciesContainer(
    a=providers.Provider(),
    b=providers.Provider(),
)
a1 = provider1.a
b1 = provider1.b
c1 = provider1.c.provided

assert_type(a1, providers.Provider[Any])
assert_type(b1, providers.Provider[Any])
assert_type(c1, providers.ProvidedInstance)
