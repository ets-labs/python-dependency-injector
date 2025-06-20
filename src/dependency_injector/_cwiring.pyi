from typing import Any, Dict

from .providers import Provider

class DependencyResolver:
    def __init__(
        self,
        kwargs: Dict[str, Any],
        injections: Dict[str, Provider[Any]],
        closings: Dict[str, Provider[Any]],
        /,
    ) -> None: ...
    def __enter__(self) -> Dict[str, Any]: ...
    def __exit__(self, *exc_info: Any) -> None: ...
    async def __aenter__(self) -> Dict[str, Any]: ...
    async def __aexit__(self, *exc_info: Any) -> None: ...

def _isawaitable(instance: Any) -> bool: ...
