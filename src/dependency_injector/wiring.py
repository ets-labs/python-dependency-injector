"""Wiring module."""

import functools
import inspect
import pkgutil
from types import ModuleType
from typing import Optional, Iterable, Callable, Any, Type, Dict

from . import providers

AnyContainer = Any


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
    signature = inspect.signature(fn)

    config = _resolve_container_config(container)

    injections = {}
    for parameter_name, parameter in signature.parameters.items():
        if parameter_name in container.providers:
            injections[parameter_name] = container.providers[parameter_name]

        if parameter_name.endswith('_provider'):
            provider_name = parameter_name[:-9]
            if provider_name in container.providers:
                injections[parameter_name] = container.providers[provider_name].provider

        if config and isinstance(parameter.default, ConfigurationOption):
            option_provider = config.get_option_provider(parameter.default.selector)
            if parameter.annotation:
                injections[parameter_name] = option_provider.as_(parameter.annotation)
            else:
                injections[parameter_name] = option_provider

    return injections


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


class ConfigurationOption:
    """Configuration option marker."""

    def __init__(self, selector: str):
        self.selector = selector

    def __class_getitem__(cls, item):
        return cls(item)


