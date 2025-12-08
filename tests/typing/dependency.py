from typing import Any, Type
from typing_extensions import assert_type

from dependency_injector import providers


class Animal: ...


class Cat(Animal):

    def __init__(self, *a: Any, **kw: Any) -> None: ...


# Test 1: to check the return type
provider1 = providers.Dependency(instance_of=Animal)
provider1.override(providers.Factory(Cat))
var1 = provider1()
assert_type(var1, Animal)

# Test 2: to check the return type
provider2 = providers.Dependency(instance_of=Animal)
var2 = provider2.instance_of
assert_type(var2, Type[Animal])

# Test 3: to check the return type with await
provider3 = providers.Dependency(instance_of=Animal)


async def _async3() -> None:
    var1 = await provider3()  # type: ignore
    var2 = await provider3.async_()
    assert_type(var2, Animal)
