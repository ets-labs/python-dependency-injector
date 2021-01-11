from typing import List, Iterator, Generator, AsyncIterator, AsyncGenerator

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


# Test 5: to check the return type with async function
async def init5() -> List[int]:
    ...


provider5 = providers.Resource(init5)


async def _provide5() -> None:
    var1: List[int] = await provider5()  # type: ignore
    var2: List[int] = await provider5.async_()


# Test 6: to check the return type with async iterator
async def init6() -> AsyncIterator[List[int]]:
    yield []


provider6 = providers.Resource(init6)


async def _provide6() -> None:
    var1: List[int] = await provider6()  # type: ignore
    var2: List[int] = await provider6.async_()


# Test 7: to check the return type with async generator
async def init7() -> AsyncGenerator[List[int], None]:
    yield []


provider7 = providers.Resource(init7)


async def _provide7() -> None:
    var1: List[int] = await provider7()  # type: ignore
    var2: List[int] = await provider7.async_()


# Test 8: to check the return type with async resource subclass
class MyResource8(resources.AsyncResource[List[int]]):
    async def init(self, *args, **kwargs) -> List[int]:
        return []

    async def shutdown(self, resource: List[int]) -> None:
        ...


provider8 = providers.Resource(MyResource8)


async def _provide8() -> None:
    var1: List[int] = await provider8()  # type: ignore
    var2: List[int] = await provider8.async_()
