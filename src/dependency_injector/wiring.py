"""Wiring module."""

import functools
import inspect
import sys
import pkgutil
from types import ModuleType
from typing import Optional, Iterable, Callable, Any, Type, Dict, Generic, TypeVar

# Spike for Python 3.6
# if sys.version_info < (3, 7):
#     from typing import GenericMeta
# else:
#     class GenericMeta(type):
#         ...

from . import providers

AnyContainer = Any
T = TypeVar('T')


def wire(
        container: AnyContainer,
        *,
        modules: Optional[Iterable[ModuleType]] = None,
        packages: Optional[Iterable[ModuleType]] = None,
) -> None:
    """Wire container providers with provided packages and modules by name."""
    if not modules:
        modules = []

    if packages:
        for package in packages:
            modules.extend(_fetch_modules(package))

    for module in modules:
        for name, member in inspect.getmembers(module):
            if inspect.isfunction(member):
                _patch_fn(module, name, member, container)
            elif inspect.isclass(member):
                _patch_cls(member, container)


def _patch_cls(
        cls: Type[Any],
        container: AnyContainer,
) -> None:
    if not hasattr(cls, '__init__'):
        return
    init_method = getattr(cls, '__init__')

    injections = _resolve_injections(init_method, container)
    if not injections:
        return

    setattr(cls, '__init__', _patch_with_injections(init_method, injections))


def _patch_fn(
        module: ModuleType,
        name: str,
        fn: Callable[..., Any],
        container: AnyContainer,
) -> None:
    injections = _resolve_injections(fn, container)
    if not injections:
        return

    setattr(module, name, _patch_with_injections(fn, injections))


def _resolve_injections(fn: Callable[..., Any], container: AnyContainer) -> Dict[str, Any]:
    config = _resolve_container_config(container)

    signature = inspect.signature(fn)

    injections = {}
    for parameter_name, parameter in signature.parameters.items():
        if not isinstance(parameter.default, _Marker):
            continue
        marker = parameter.default

        if config and isinstance(marker.provider, providers.ConfigurationOption):
            provider = _prepare_config_injection(marker.provider.get_name(), config)
        elif config and isinstance(marker.provider, providers.TypedConfigurationOption):
            provider = _prepare_config_injection(
                marker.provider.option.get_name(),
                config,
                marker.provider.provides,
            )
        elif isinstance(marker.provider, providers.Provider):
            provider_name = container.resolve_provider_name(marker.provider)
            if not provider_name:
                continue
            provider = container.providers[provider_name]
        else:
            continue

        if isinstance(marker, Provide):
            injections[parameter_name] = provider
        elif isinstance(marker, Provider):
            injections[parameter_name] = provider.provider

    return injections


def _prepare_config_injection(
        option_name: str,
        config: providers.Configuration,
        as_: Any = None,
) -> providers.Provider:
    _, *parts = option_name.split('.')
    relative_option_name = '.'.join(parts)
    provider = config.get_option_provider(relative_option_name)
    if as_:
        return provider.as_(as_)
    return provider


def _resolve_container_config(container: AnyContainer) -> Optional[providers.Configuration]:
    for provider in container.providers.values():
        if isinstance(provider, providers.Configuration):
            return provider
    else:
        return None


def _fetch_modules(package):
    modules = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + '.',
    ):
        module = loader.find_module(module_name).load_module(module_name)
        modules.append(module)
    return modules


def _patch_with_injections(fn, injections):
    @functools.wraps(fn)
    def _patched(*args, **kwargs):
        to_inject = {}
        for injection, provider in injections.items():
            to_inject[injection] = provider()

        to_inject.update(kwargs)

        return fn(*args, **to_inject)
    return _patched


class ClassGetItemMeta(type):

    def __getitem__(cls, item):
        # Spike for Python 3.6
        return cls(item)


class _Marker(Generic[T], metaclass=ClassGetItemMeta):
    def __init__(self, provider: providers.Provider) -> None:
        self.provider = provider

    def __class_getitem__(cls, item) -> T:
        return cls(item)


class Provide(_Marker):
    ...


class Provider(_Marker):
    ...
