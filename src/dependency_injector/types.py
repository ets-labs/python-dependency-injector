from typing import TypeVar, Generic, Any
import warnings


warnings.warn(
    message=(
        'Types module is deprecated since version 3.44.0. Use "Provider" class from the '
        '"providers" module: providers.Provider[SomeClass]'
    ),
    category=DeprecationWarning,
)

Injection = Any
T = TypeVar('T')


class Provider(Generic[T]):
    def __call__(self, *args: Injection, **kwargs: Injection) -> T: ...
