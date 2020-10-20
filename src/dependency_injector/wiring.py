"""Wiring module."""

import functools
import inspect
import pkgutil
import sys
from types import ModuleType
from typing import Optional, Iterable, Callable, Any, Dict, Generic, TypeVar, cast

if sys.version_info < (3, 7):
    from typing import GenericMeta
else:
    class GenericMeta(type):
        ...


from . import providers


__all__ = (
    'wire',
    'unwire',
    'Provide',
    'Provider',
)

T = TypeVar('T')
Container = Any


class ProvidersMap:

    def __init__(self, container):
        self._container = container
        self._map = self._create_providers_map(
            current_providers=container.providers,
            original_providers=container.declarative_parent.providers,
        )

    def resolve_provider(self, provider: providers.Provider) -> providers.Provider:
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

    def _resolve_delegate(self, original: providers.Delegate) -> providers.Provider:
        return self._resolve_provider(original.provides)

    def _resolve_provided_instance(self, original: providers.Provider) -> providers.Provider:
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
    ) -> providers.Provider:
        original_root = original.root
        new = self._resolve_provider(original_root)
        new = cast(providers.Configuration, new)

        for segment in original.get_name_segments():
            if providers.is_provider(segment):
                segment = self.resolve_provider(segment)
                new = new[segment]
            else:
                new = getattr(new, segment)

        if as_:
            new = new.as_(as_)

        return new

    def _resolve_provider(self, original: providers.Provider) -> providers.Provider:
        try:
            return self._map[original]
        except KeyError:
            raise Exception('Unable to resolve original provider')

    @classmethod
    def _create_providers_map(
            cls,
            current_providers: Dict[str, providers.Provider],
            original_providers: Dict[str, providers.Provider],
    ) -> Dict[providers.Provider, providers.Provider]:
        providers_map = {}
        for provider_name, current_provider in current_providers.items():
            original_provider = original_providers[provider_name]
            providers_map[original_provider] = current_provider

            if isinstance(current_provider, providers.Container) \
                    and isinstance(original_provider, providers.Container):
                subcontainer_map = cls._create_providers_map(
                    current_providers=current_provider.container.providers,
                    original_providers=original_provider.container.providers,
                )
                providers_map.update(subcontainer_map)

        return providers_map


def wire(
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
                for method_name, method in inspect.getmembers(member, inspect.isfunction):
                    _patch_fn(member, method_name, method, providers_map)


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
                _unpatch_fn(module, name, member)
            elif inspect.isclass(member):
                for method_name, method in inspect.getmembers(member, inspect.isfunction):
                    _unpatch_fn(member, method_name, method)


def _patch_fn(
        module: ModuleType,
        name: str,
        fn: Callable[..., Any],
        providers_map: ProvidersMap,
) -> None:
    injections = _resolve_injections(fn, providers_map)
    if not injections:
        return
    setattr(module, name, _patch_with_injections(fn, injections))


def _unpatch_fn(
        module: ModuleType,
        name: str,
        fn: Callable[..., Any],
) -> None:
    if not _is_patched(fn):
        return
    setattr(module, name, _get_original_from_patched(fn))


def _resolve_injections(fn: Callable[..., Any], providers_map: ProvidersMap) -> Dict[str, Any]:  # noqa
    signature = inspect.signature(fn)

    injections = {}
    for parameter_name, parameter in signature.parameters.items():
        if not isinstance(parameter.default, _Marker):
            continue
        marker = parameter.default

        provider = providers_map.resolve_provider(marker.provider)
        if isinstance(marker, Provide):
            injections[parameter_name] = provider
        elif isinstance(marker, Provider):
            injections[parameter_name] = provider.provider

    return injections


def _fetch_modules(package):
    modules = [package]
    for loader, module_name, is_pkg in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + '.',
    ):
        module = loader.find_module(module_name).load_module(module_name)
        modules.append(module)
    return modules


def _patch_with_injections(fn, injections):
    if inspect.iscoroutinefunction(fn):
        @functools.wraps(fn)
        async def _patched(*args, **kwargs):
            to_inject = {}
            for injection, provider in injections.items():
                to_inject[injection] = provider()

            to_inject.update(kwargs)

            return await fn(*args, **to_inject)
    else:
        @functools.wraps(fn)
        def _patched(*args, **kwargs):
            to_inject = {}
            for injection, provider in injections.items():
                to_inject[injection] = provider()

            to_inject.update(kwargs)

            return fn(*args, **to_inject)

    _patched.__wired__ = True
    _patched.__original__ = fn
    _patched.__injections__ = injections

    return _patched


def _is_patched(fn):
    return getattr(fn, '__wired__', False) is True


def _get_original_from_patched(fn):
    return getattr(fn, '__original__')


def _is_declarative_container_instance(instance: Any) -> bool:
    return (not isinstance(instance, type)
            and getattr(instance, '__IS_CONTAINER__', False) is True
            and getattr(instance, 'declarative_parent', None) is not None)


class ClassGetItemMeta(GenericMeta):
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
