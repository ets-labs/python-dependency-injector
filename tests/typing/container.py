from typing import Any
from typing_extensions import assert_type

from dependency_injector import providers


class Container: ...


# Test 1: to check the return type
provider1 = providers.Container(Container)
var1 = provider1()
assert_type(var1, Container)


# Test 2: to check the getattr
provider2 = providers.Container(Container)
attr = provider2.attr
assert_type(attr, providers.Provider[Any])
