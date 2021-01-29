"""Wiring module."""

import asyncio
import functools
import inspect
import importlib
import importlib.machinery
import pkgutil
import sys
from types import ModuleType
from typing import (
    Optional,
    Iterable,
    Iterator,
    Callable,
    Any,
    Tuple,
    Dict,
    Generic,
    TypeVar,
    Type,
    Union,
    cast,
)

if sys.version_info < (3, 7):
    from typing import GenericMeta
else:
    class GenericMeta(type):
        ...

# Hotfix, see: https://github.com/ets-labs/python-dependency-injector/issues/362
if sys.version_info >= (3, 9):
    from types import GenericAlias
else:
    GenericAlias = None


try:
    from fastapi.params import Depends as FastAPIDepends
    fastapi_installed = True
except ImportError:
    fastapi_installed = False


from . import providers


__all__ = (
    'wire',
    'unwire',
    'inject',
    'Provide',
    'Provider',
    'Closing',
    'register_loader_containers',
    'unregister_loader_containers',
    'install_loader',
    'uninstall_loader',
    'is_loader_installed',
)

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])
Container = Any


class Registry:

    def __init__(self):
        self._storage = set()

    def add(self, patched: Callable[..., Any]) -> None:
        self._storage.add(patched)

    def get_from_module(self, module: ModuleType) -> Iterator[Callable[..., Any]]:
        for patched in self._storage:
            if patched.__module__ != module.__name__:
                continue
            yield patched


_patched_registry = Registry()


class ProvidersMap:

    def __init__(self, container):
        self._container = container
        self._map = self._create_providers_map(
            current_container=container,
            original_container=container.declarative_parent,
        )

    def resolve_provider(
            self,
            provider: providers.Provider,
    ) -> Optional[providers.Provider]:
        if isinstance(provider, providers.Delegate):
            return self._resolve_delegate(provider)
        elif isinstance(provider, (
            providers.ProvidedInstance,
            providers.AttributeGetter,
            providers.ItemGetter,
            providers.MethodCaller,
        )):
            return self._resolve_provided_instance(provider)
        elif isinstance(provider, providers.ConfigurationOption):
            return self._resolve_config_option(provider)
        elif isinstance(provider, providers.TypedConfigurationOption):
            return self._resolve_config_option(provider.option, as_=provider.provides)
        else:
            return self._resolve_provider(provider)

    def _resolve_delegate(
            self,
            original: providers.Delegate,
    ) -> Optional[providers.Provider]:
        return self._resolve_provider(original.provides)

    def _resolve_provided_instance(
            self,
            original: providers.Provider,
    ) -> Optional[providers.Provider]:
        modifiers = []
        while isinstance(original, (
                providers.ProvidedInstance,
                providers.AttributeGetter,
                providers.ItemGetter,
                providers.MethodCaller,
        )):
            modifiers.insert(0, original)
            original = original.provides

        new = self._resolve_provider(original)
        if new is None:
            return None

        for modifier in modifiers:
            if isinstance(modifier, providers.ProvidedInstance):
                new = new.provided
            elif isinstance(modifier, providers.AttributeGetter):
                new = getattr(new, modifier.name)
            elif isinstance(modifier, providers.ItemGetter):
                new = new[modifier.name]
            elif isinstance(modifier, providers.MethodCaller):
                new = new.call(
                    *modifier.args,
                    **modifier.kwargs,
                )

        return new

    def _resolve_config_option(
            self,
            original: providers.ConfigurationOption,
            as_: Any = None,
    ) -> Optional[providers.Provider]:
        original_root = original.root
        new = self._resolve_provider(original_root)
        if new is None:
            return None
        new = cast(providers.Configuration, new)

        for segment in original.get_name_segments():
            if providers.is_provider(segment):
                segment = self.resolve_provider(segment)
                new = new[segment]
            else:
                new = getattr(new, segment)

        if original.is_required():
            new = new.required()

        if as_:
            new = new.as_(as_)

        return new

    def _resolve_provider(
            self,
            original: providers.Provider,
    ) -> Optional[providers.Provider]:
        try:
            return self._map[original]
        except KeyError:
            pass

    @classmethod
    def _create_providers_map(
            cls,
            current_container: Container,
            original_container: Container,
    ) -> Dict[providers.Provider, providers.Provider]:
        current_providers = current_container.providers
        current_providers['__self__'] = current_container.__self__

        original_providers = original_container.providers
        original_providers['__self__'] = original_container.__self__

        providers_map = {}
        for provider_name, current_provider in current_providers.items():
            original_provider = original_providers[provider_name]
            providers_map[original_provider] = current_provider

            if isinstance(current_provider, providers.Container) \
                    and isinstance(original_provider, providers.Container):
                subcontainer_map = cls._create_providers_map(
                    current_container=current_provider.container,
                    original_container=original_provider.container,
                )
                providers_map.update(subcontainer_map)

        return providers_map


def wire(  # noqa: C901
        container: Container,
        *,
        modules: Optional[Iterable[ModuleType]] = None,
        packages: Optional[Iterable[ModuleType]] = None,
) -> None:
    """Wire container providers with provided packages and modules."""
    if not _is_declarative_container_instance(container):
        raise Exception('Can wire only an instance of the declarative container')

    if not modules:
        modules = []

    if packages:
        for package in packages:
            modules.extend(_fetch_modules(package))

    providers_map = ProvidersMap(container)

    for module in modules:
        for name, member in inspect.getmembers(module):
            if inspect.isfunction(member):
                _patch_fn(module, name, member, providers_map)
            elif inspect.isclass(member):
                for method_name, method in inspect.getmembers(member, _is_method):
                    _patch_method(member, method_name, method, providers_map)

        for patched in _patched_registry.get_from_module(module):
            _bind_injections(patched, providers_map)


def unwire(
        *,
        modules: Optional[Iterable[ModuleType]] = None,
        packages: Optional[Iterable[ModuleType]] = None,
) -> None:
    """Wire provided packages and modules with previous wired providers."""
    if not modules:
        modules = []

    if packages:
        for package in packages:
            modules.extend(_fetch_modules(package))

    for module in modules:
        for name, member in inspect.getmembers(module):
            if inspect.isfunction(member):
                _unpatch(module, name, member)
            elif inspect.isclass(member):
                for method_name, method in inspect.getmembers(member, inspect.isfunction):
                    _unpatch(member, method_name, method)

        for patched in _patched_registry.get_from_module(module):
            _unbind_injections(patched)


def inject(fn: F) -> F:
    """Decorate callable with injecting decorator."""
    reference_injections, reference_closing = _fetch_reference_injections(fn)
    patched = _get_patched(fn, reference_injections, reference_closing)
    _patched_registry.add(patched)
    return cast(F, patched)


def _patch_fn(
        module: ModuleType,
        name: str,
        fn: Callable[..., Any],
        providers_map: ProvidersMap,
) -> None:
    if not _is_patched(fn):
        reference_injections, reference_closing = _fetch_reference_injections(fn)
        if not reference_injections:
            return
        fn = _get_patched(fn, reference_injections, reference_closing)
        _patched_registry.add(fn)

    _bind_injections(fn, providers_map)

    setattr(module, name, fn)


def _patch_method(
        cls: Type,
        name: str,
        method: Callable[..., Any],
        providers_map: ProvidersMap,
) -> None:
    if hasattr(cls, '__dict__') \
            and name in cls.__dict__ \
            and isinstance(cls.__dict__[name], (classmethod, staticmethod)):
        method = cls.__dict__[name]
        fn = method.__func__
    else:
        fn = method

    if not _is_patched(fn):
        reference_injections, reference_closing = _fetch_reference_injections(fn)
        if not reference_injections:
            return
        fn = _get_patched(fn, reference_injections, reference_closing)
        _patched_registry.add(fn)

    _bind_injections(fn, providers_map)

    if isinstance(method, (classmethod, staticmethod)):
        fn = type(method)(fn)

    setattr(cls, name, fn)


def _unpatch(
        module: ModuleType,
        name: str,
        fn: Callable[..., Any],
) -> None:
    if hasattr(module, '__dict__') \
            and name in module.__dict__ \
            and isinstance(module.__dict__[name], (classmethod, staticmethod)):
        method = module.__dict__[name]
        fn = method.__func__

    if not _is_patched(fn):
        return

    _unbind_injections(fn)


def _fetch_reference_injections(
        fn: Callable[..., Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    # # Hotfix, see: https://github.com/ets-labs/python-dependency-injector/issues/362
    if GenericAlias and fn is GenericAlias:
        fn = fn.__init__

    signature = inspect.signature(fn)

    injections = {}
    closing = {}
    for parameter_name, parameter in signature.parameters.items():
        if not isinstance(parameter.default, _Marker) \
                and not _is_fastapi_depends(parameter.default):
            continue

        marker = parameter.default

        if _is_fastapi_depends(marker):
            marker = marker.dependency

            if not isinstance(marker, _Marker):
                continue

        if isinstance(marker, Closing):
            marker = marker.provider
            closing[parameter_name] = marker

        injections[parameter_name] = marker
    return injections, closing


def _bind_injections(fn: Callable[..., Any], providers_map: ProvidersMap) -> None:
    for injection, marker in fn.__reference_injections__.items():
        provider = providers_map.resolve_provider(marker.provider)

        if provider is None:
            continue

        if isinstance(marker, Provide):
            fn.__injections__[injection] = provider
        elif isinstance(marker, Provider):
            fn.__injections__[injection] = provider.provider

        if injection in fn.__reference_closing__:
            fn.__closing__[injection] = provider


def _unbind_injections(fn: Callable[..., Any]) -> None:
    fn.__injections__ = {}
    fn.__closing__ = {}


def _fetch_modules(package):
    modules = [package]
    for module_info in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + '.',
    ):
        module = importlib.import_module(module_info.name)
        modules.append(module)
    return modules


def _is_method(member):
    return inspect.ismethod(member) or inspect.isfunction(member)


def _get_patched(fn, reference_injections, reference_closing):
    if inspect.iscoroutinefunction(fn):
        patched = _get_async_patched(fn)
    else:
        patched = _get_sync_patched(fn)

    patched.__wired__ = True
    patched.__original__ = fn
    patched.__injections__ = {}
    patched.__reference_injections__ = reference_injections
    patched.__closing__ = {}
    patched.__reference_closing__ = reference_closing

    return patched


def _get_sync_patched(fn):
    @functools.wraps(fn)
    def _patched(*args, **kwargs):
        to_inject = kwargs.copy()
        for injection, provider in _patched.__injections__.items():
            if injection not in kwargs \
                    or _is_fastapi_default_arg_injection(injection, kwargs):
                to_inject[injection] = provider()

        result = fn(*args, **to_inject)

        for injection, provider in _patched.__closing__.items():
            if injection in kwargs \
                    and not _is_fastapi_default_arg_injection(injection, kwargs):
                continue
            if not isinstance(provider, providers.Resource):
                continue
            provider.shutdown()

        return result
    return _patched


def _get_async_patched(fn):
    @functools.wraps(fn)
    async def _patched(*args, **kwargs):
        to_inject = kwargs.copy()
        to_inject_await = []
        to_close_await = []
        for injection, provider in _patched.__injections__.items():
            if injection not in kwargs \
                    or _is_fastapi_default_arg_injection(injection, kwargs):
                provide = provider()
                if inspect.isawaitable(provide):
                    to_inject_await.append((injection, provide))
                else:
                    to_inject[injection] = provide

        async_to_inject = await asyncio.gather(*[provide for _, provide in to_inject_await])
        for provide, (injection, _) in zip(async_to_inject, to_inject_await):
            to_inject[injection] = provide

        result = await fn(*args, **to_inject)

        for injection, provider in _patched.__closing__.items():
            if injection in kwargs \
                    and not _is_fastapi_default_arg_injection(injection, kwargs):
                continue
            if not isinstance(provider, providers.Resource):
                continue
            shutdown = provider.shutdown()
            if inspect.isawaitable(shutdown):
                to_close_await.append(shutdown)

        await asyncio.gather(*to_close_await)

        return result
    return _patched


def _is_fastapi_default_arg_injection(injection, kwargs):
    """Check if injection is FastAPI injection of the default argument."""
    return injection in kwargs and isinstance(kwargs[injection], _Marker)


def _is_fastapi_depends(param: Any) -> bool:
    return fastapi_installed and isinstance(param, FastAPIDepends)


def _is_patched(fn):
    return getattr(fn, '__wired__', False) is True


def _is_declarative_container_instance(instance: Any) -> bool:
    return (not isinstance(instance, type)
            and getattr(instance, '__IS_CONTAINER__', False) is True
            and getattr(instance, 'declarative_parent', None) is not None)


def _is_declarative_container(instance: Any) -> bool:
    return (isinstance(instance, type)
            and getattr(instance, '__IS_CONTAINER__', False) is True
            and getattr(instance, 'declarative_parent', None) is None)


class ClassGetItemMeta(GenericMeta):
    def __getitem__(cls, item):
        # Spike for Python 3.6
        return cls(item)


class _Marker(Generic[T], metaclass=ClassGetItemMeta):

    def __init__(self, provider: Union[providers.Provider, Container]) -> None:
        if _is_declarative_container(provider):
            provider = provider.__self__
        self.provider: providers.Provider = provider

    def __class_getitem__(cls, item) -> T:
        return cls(item)

    def __call__(self) -> T:
        return self


class Provide(_Marker):
    ...


class Provider(_Marker):
    ...


class Closing(_Marker):
    ...


class AutoLoader:
    """Auto-wiring module loader.

    Automatically wire containers when modules are imported.
    """

    def __init__(self):
        self.containers = []
        self._path_hook = None

    def register_containers(self, *containers):
        self.containers.extend(containers)

        if not self.installed:
            self.install()

    def unregister_containers(self, *containers):
        for container in containers:
            self.containers.remove(container)

        if not self.containers:
            self.uninstall()

    def wire_module(self, module):
        for container in self.containers:
            container.wire(modules=[module])

    @property
    def installed(self):
        return self._path_hook is not None

    def install(self):
        if self.installed:
            return

        loader = self

        class SourcelessFileLoader(importlib.machinery.SourcelessFileLoader):
            def exec_module(self, module):
                super().exec_module(module)
                loader.wire_module(module)

        class SourceFileLoader(importlib.machinery.SourceFileLoader):
            def exec_module(self, module):
                super().exec_module(module)
                loader.wire_module(module)

        loader_details = [
            (SourcelessFileLoader, importlib.machinery.BYTECODE_SUFFIXES),
            (SourceFileLoader, importlib.machinery.SOURCE_SUFFIXES),
        ]

        self._path_hook = importlib.machinery.FileFinder.path_hook(*loader_details)

        sys.path_hooks.insert(0, self._path_hook)
        sys.path_importer_cache.clear()
        importlib.invalidate_caches()

    def uninstall(self):
        if not self.installed:
            return

        sys.path_hooks.remove(self._path_hook)
        sys.path_importer_cache.clear()
        importlib.invalidate_caches()


_loader = AutoLoader()


def register_loader_containers(*containers: Container) -> None:
    """Register containers in auto-wiring module loader."""
    _loader.register_containers(*containers)


def unregister_loader_containers(*containers: Container) -> None:
    """Unregister containers from auto-wiring module loader."""
    _loader.unregister_containers(*containers)


def install_loader() -> None:
    """Install auto-wiring module loader hook."""
    _loader.install()


def uninstall_loader() -> None:
    """Uninstall auto-wiring module loader hook."""
    _loader.uninstall()


def is_loader_installed() -> bool:
    """Check if auto-wiring module loader hook is installed."""
    return _loader.installed
