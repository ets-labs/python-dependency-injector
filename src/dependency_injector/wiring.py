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
    Set,
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
    import fastapi.params
except ImportError:
    fastapi = None


try:
    import starlette.requests
except ImportError:
    starlette = None


try:
    import werkzeug.local
except ImportError:
    werkzeug = None


from . import providers


__all__ = (
    'wire',
    'unwire',
    'inject',
    'as_int',
    'as_float',
    'as_',
    'required',
    'invariant',
    'provided',
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


class PatchedRegistry:

    def __init__(self):
        self._callables: Set[Callable[..., Any]] = set()
        self._attributes: Set[PatchedAttribute] = set()

    def add_callable(self, patched: Callable[..., Any]) -> None:
        self._callables.add(patched)

    def get_callables_from_module(self, module: ModuleType) -> Iterator[Callable[..., Any]]:
        for patched in self._callables:
            if patched.__module__ != module.__name__:
                continue
            yield patched

    def add_attribute(self, patched: 'PatchedAttribute'):
        self._attributes.add(patched)

    def get_attributes_from_module(self, module: ModuleType) -> Iterator['PatchedAttribute']:
        for attribute in self._attributes:
            if not attribute.is_in_module(module):
                continue
            yield attribute

    def clear_module_attributes(self, module: ModuleType):
        for attribute in self._attributes.copy():
            if not attribute.is_in_module(module):
                continue
            self._attributes.remove(attribute)


class PatchedAttribute:

    def __init__(self, member: Any, name: str, marker: '_Marker'):
        self.member = member
        self.name = name
        self.marker = marker

    @property
    def module_name(self) -> str:
        if isinstance(self.member, ModuleType):
            return self.member.__name__
        else:
            return self.member.__module__

    def is_in_module(self, module: ModuleType) -> bool:
        return self.module_name == module.__name__


class ProvidersMap:

    CONTAINER_STRING_ID = '<container>'

    def __init__(self, container):
        self._container = container
        self._map = self._create_providers_map(
            current_container=container,
            original_container=(
                container.declarative_parent
                if container.declarative_parent
                else container
            ),
        )

    def resolve_provider(
            self,
            provider: Union[providers.Provider, str],
            modifier: Optional['Modifier'] = None,
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
        elif isinstance(provider, str):
            return self._resolve_string_id(provider, modifier)
        else:
            return self._resolve_provider(provider)

    def _resolve_string_id(
            self,
            id: str,
            modifier: Optional['Modifier'] = None,
    ) -> Optional[providers.Provider]:
        if id == self.CONTAINER_STRING_ID:
            return self._container.__self__

        provider = self._container
        for segment in id.split('.'):
            try:
                provider = getattr(provider, segment)
            except AttributeError:
                return None

        if modifier:
            provider = modifier.modify(provider, providers_map=self)
        return provider

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

    def _resolve_delegate(
            self,
            original: providers.Delegate,
    ) -> Optional[providers.Provider]:
        return self._resolve_provider(original.provides)

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
            return None

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


class InspectFilter:

    def is_excluded(self, instance: object) -> bool:
        if self._is_werkzeug_local_proxy(instance):
            return True
        elif self._is_starlette_request_cls(instance):
            return True
        elif self._is_builtin(instance):
            return True
        else:
            return False

    def _is_werkzeug_local_proxy(self, instance: object) -> bool:
        return werkzeug and isinstance(instance, werkzeug.local.LocalProxy)

    def _is_starlette_request_cls(self, instance: object) -> bool:
        return starlette \
               and isinstance(instance, type) \
               and issubclass(instance, starlette.requests.Request)

    def _is_builtin(self, instance: object) -> bool:
        return inspect.isbuiltin(instance)


def wire(  # noqa: C901
        container: Container,
        *,
        modules: Optional[Iterable[ModuleType]] = None,
        packages: Optional[Iterable[ModuleType]] = None,
) -> None:
    """Wire container providers with provided packages and modules."""
    if not modules:
        modules = []

    if packages:
        for package in packages:
            modules.extend(_fetch_modules(package))

    providers_map = ProvidersMap(container)

    for module in modules:
        for member_name, member in inspect.getmembers(module):
            if _inspect_filter.is_excluded(member):
                continue

            if _is_marker(member):
                _patch_attribute(module, member_name, member, providers_map)
            elif inspect.isfunction(member):
                _patch_fn(module, member_name, member, providers_map)
            elif inspect.isclass(member):
                cls = member
                try:
                    cls_members = inspect.getmembers(cls)
                except Exception:  # noqa
                    # Hotfix, see: https://github.com/ets-labs/python-dependency-injector/issues/441
                    continue
                else:
                    for cls_member_name, cls_member in cls_members:
                        if _is_marker(cls_member):
                            _patch_attribute(cls, cls_member_name, cls_member, providers_map)
                        elif _is_method(cls_member):
                            _patch_method(cls, cls_member_name, cls_member, providers_map)

        for patched in _patched_registry.get_callables_from_module(module):
            _bind_injections(patched, providers_map)


def unwire(  # noqa: C901
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

        for patched in _patched_registry.get_callables_from_module(module):
            _unbind_injections(patched)

        for patched_attribute in _patched_registry.get_attributes_from_module(module):
            _unpatch_attribute(patched_attribute)
        _patched_registry.clear_module_attributes(module)


def inject(fn: F) -> F:
    """Decorate callable with injecting decorator."""
    reference_injections, reference_closing = _fetch_reference_injections(fn)
    patched = _get_patched(fn, reference_injections, reference_closing)
    _patched_registry.add_callable(patched)
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
        _patched_registry.add_callable(fn)

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
        _patched_registry.add_callable(fn)

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


def _patch_attribute(
        member: Any,
        name: str,
        marker: '_Marker',
        providers_map: ProvidersMap,
) -> None:
    provider = providers_map.resolve_provider(marker.provider, marker.modifier)
    if provider is None:
        return

    _patched_registry.add_attribute(PatchedAttribute(member, name, marker))

    if isinstance(marker, Provide):
        instance = provider()
        setattr(member, name, instance)
    elif isinstance(marker, Provider):
        setattr(member, name, provider)
    else:
        raise Exception(f'Unknown type of marker {marker}')


def _unpatch_attribute(patched: PatchedAttribute) -> None:
    setattr(patched.member, patched.name, patched.marker)


def _fetch_reference_injections(  # noqa: C901
        fn: Callable[..., Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    # Hotfix, see:
    # - https://github.com/ets-labs/python-dependency-injector/issues/362
    # - https://github.com/ets-labs/python-dependency-injector/issues/398
    if GenericAlias and any((
                fn is GenericAlias,
                getattr(fn, '__func__', None) is GenericAlias
            )):
        fn = fn.__init__

    try:
        signature = inspect.signature(fn)
    except ValueError as exception:
        if 'no signature found' in str(exception):
            return {}, {}
        elif 'not supported by signature' in str(exception):
            return {}, {}
        else:
            raise exception

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
        provider = providers_map.resolve_provider(marker.provider, marker.modifier)

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


def _is_marker(member):
    return isinstance(member, _Marker)


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
    return fastapi and isinstance(param, fastapi.params.Depends)


def _is_patched(fn):
    return getattr(fn, '__wired__', False) is True


def _is_declarative_container(instance: Any) -> bool:
    return (isinstance(instance, type)
            and getattr(instance, '__IS_CONTAINER__', False) is True
            and getattr(instance, 'declarative_parent', None) is None)


class Modifier:

    def modify(
            self,
            provider: providers.ConfigurationOption,
            providers_map: ProvidersMap,
    ) -> providers.Provider:
        ...


class TypeModifier(Modifier):

    def __init__(self, type_: Type):
        self.type_ = type_

    def modify(
            self,
            provider: providers.ConfigurationOption,
            providers_map: ProvidersMap,
    ) -> providers.Provider:
        return provider.as_(self.type_)


def as_int() -> TypeModifier:
    """Return int type modifier."""
    return TypeModifier(int)


def as_float() -> TypeModifier:
    """Return float type modifier."""
    return TypeModifier(float)


def as_(type_: Type) -> TypeModifier:
    """Return custom type modifier."""
    return TypeModifier(type_)


class RequiredModifier(Modifier):

    def __init__(self):
        self.type_modifier = None

    def as_int(self) -> 'RequiredModifier':
        self.type_modifier = TypeModifier(int)
        return self

    def as_float(self) -> 'RequiredModifier':
        self.type_modifier = TypeModifier(float)
        return self

    def as_(self, type_: Type) -> 'RequiredModifier':
        self.type_modifier = TypeModifier(type_)
        return self

    def modify(
            self,
            provider: providers.ConfigurationOption,
            providers_map: ProvidersMap,
    ) -> providers.Provider:
        provider = provider.required()
        if self.type_modifier:
            provider = provider.as_(self.type_modifier.type_)
        return provider


def required() -> RequiredModifier:
    """Return required modifier."""
    return RequiredModifier()


class InvariantModifier(Modifier):

    def __init__(self, id: str) -> None:
        self.id = id

    def modify(
            self,
            provider: providers.ConfigurationOption,
            providers_map: ProvidersMap,
    ) -> providers.Provider:
        invariant_segment = providers_map.resolve_provider(self.id)
        return provider[invariant_segment]


def invariant(id: str) -> InvariantModifier:
    """Return invariant modifier."""
    return InvariantModifier(id)


class ProvidedInstance(Modifier):

    TYPE_ATTRIBUTE = 'attr'
    TYPE_ITEM = 'item'
    TYPE_CALL = 'call'

    def __init__(self):
        self.segments = []

    def __getattr__(self, item):
        self.segments.append((self.TYPE_ATTRIBUTE, item))
        return self

    def __getitem__(self, item):
        self.segments.append((self.TYPE_ITEM, item))
        return self

    def call(self):
        self.segments.append((self.TYPE_CALL, None))
        return self

    def modify(
            self,
            provider: providers.Provider,
            providers_map: ProvidersMap,
    ) -> providers.Provider:
        provider = provider.provided
        for type_, value in self.segments:
            if type_ == ProvidedInstance.TYPE_ATTRIBUTE:
                provider = getattr(provider, value)
            elif type_ == ProvidedInstance.TYPE_ITEM:
                provider = provider[value]
            elif type_ == ProvidedInstance.TYPE_CALL:
                provider = provider.call()
        return provider


def provided() -> ProvidedInstance:
    """Return provided instance modifier."""
    return ProvidedInstance()


class ClassGetItemMeta(GenericMeta):
    def __getitem__(cls, item):
        # Spike for Python 3.6
        if isinstance(item, tuple):
            return cls(*item)
        return cls(item)


class _Marker(Generic[T], metaclass=ClassGetItemMeta):

    def __init__(
            self,
            provider: Union[providers.Provider, Container, str],
            modifier: Optional[Modifier] = None,
    ) -> None:
        if _is_declarative_container(provider):
            provider = provider.__self__
        self.provider = provider
        self.modifier = modifier

    def __class_getitem__(cls, item) -> T:
        if isinstance(item, tuple):
            return cls(*item)
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
        return self._path_hook in sys.path_hooks

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

        class ExtensionFileLoader(importlib.machinery.ExtensionFileLoader):
            ...

        loader_details = [
            (SourcelessFileLoader, importlib.machinery.BYTECODE_SUFFIXES),
            (SourceFileLoader, importlib.machinery.SOURCE_SUFFIXES),
            (ExtensionFileLoader, importlib.machinery.EXTENSION_SUFFIXES),
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


_patched_registry = PatchedRegistry()
_inspect_filter = InspectFilter()
_loader = AutoLoader()
