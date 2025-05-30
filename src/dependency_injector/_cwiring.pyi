from typing import Any, Awaitable, Callable, Dict, Tuple, TypeVar

from .providers import Provider

T = TypeVar("T")

def _sync_inject(
    fn: Callable[..., T],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    injections: Dict[str, Provider[Any]],
    closings: Dict[str, Provider[Any]],
    /,
) -> T: ...
async def _async_inject(
    fn: Callable[..., Awaitable[T]],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    injections: Dict[str, Provider[Any]],
    closings: Dict[str, Provider[Any]],
    /,
) -> T: ...
def _isawaitable(instance: Any) -> bool: ...
