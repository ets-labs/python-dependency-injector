from typing import List, Iterator, Generator

from dependency_injector import providers, resources


# Test 1: to check the return type with function
def init1() -> List[int]:
    return []


provider1 = providers.Resource(init1)
var1: List[int] = provider1()


# Test 2: to check the return type with iterator
def init2() -> Iterator[List[int]]:
    yield []


provider2 = providers.Resource(init2)
var2: List[int] = provider2()


# Test 3: to check the return type with generator
def init3() -> Generator[List[int], None, None]:
    yield []


provider3 = providers.Resource(init3)
var3: List[int] = provider3()


# Test 4: to check the return type with resource subclass
class MyResource4(resources.Resource[List[int]]):
    def init(self, *args, **kwargs) -> List[int]:
        return []

    def shutdown(self, resource: List[int]) -> None:
        ...


provider4 = providers.Resource(MyResource4)
var4: List[int] = provider4()
