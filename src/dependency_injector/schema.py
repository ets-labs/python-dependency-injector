"""Schema module."""

import importlib
from typing import Dict, Any, Type, Optional

from . import containers, providers


Schema = Dict[Any, Any]


def build_schema(schema: Schema) -> Dict[str, providers.Provider]:
    """Build provider schema."""
    container = containers.DynamicContainer()
    _create_providers(container, schema['providers'])
    _setup_injections(container, schema['providers'])
    return container.providers


def _create_providers(
        container: containers.Container,
        providers_data: Dict[str, Any],
):
    for provider_name, data in providers_data.items():
        provider_type = _get_provider_cls(data['provider'])
        args = []

        provides = data.get('provides')
        if provides:
            provides = _import_string(provides)
            if provides:
                args.append(provides)

        if provider_type is providers.Container:
            provides = containers.DynamicContainer
            args.append(provides)

        provider = provider_type(*args)
        container.set_provider(provider_name, provider)

        if isinstance(provider, providers.Container):
            _create_providers(provider, data['providers'])


def _setup_injections(
        container: containers.Container,
        providers_data: Dict[str, Any],
        *,
        current_container: Optional[containers.Container] = None,
):
    if not current_container:
        current_container = container

    for provider_name, data in providers_data.items():
        provider = getattr(current_container, provider_name)
        args = []
        kwargs = {}

        arg_injections = data.get('args')
        if arg_injections:
            for arg in arg_injections:
                injection = _resolve_provider(container, arg)
                if not injection:
                    injection = arg
                args.append(injection)
        if args:
            provider.add_args(*args)

        kwarg_injections = data.get('kwargs')
        if kwarg_injections:
            for name, arg in kwarg_injections.items():
                injection = _resolve_provider(container, arg)
                if not injection:
                    injection = arg
                kwargs[name] = injection
        if kwargs:
            provider.add_kwargs(**kwargs)

        if isinstance(provider, providers.Container):
            _setup_injections(container, data['providers'], current_container=provider)


def _resolve_provider(container: containers.Container, name: str) -> Optional[providers.Provider]:
    segments = name.split('.')
    try:
        provider = getattr(container, segments[0])
    except AttributeError:
        return None

    for segment in segments[1:]:
        if segment == 'as_int()':
            provider = provider.as_int()
        elif segment == 'as_float()':
            provider = provider.as_float()
        elif segment.startswith('is_'):  # TODO
            provider = provider.as_(str)
            ...
        else:
            try:
                provider = getattr(provider, segment)
            except AttributeError:
                return None
    return provider


def _get_provider_cls(provider_cls_name: str) -> Type[providers.Provider]:
    std_provider_type = _fetch_provider_cls_from_std(provider_cls_name)
    if std_provider_type:
        return std_provider_type

    custom_provider_type = _import_provider_cls(provider_cls_name)
    if custom_provider_type:
        return custom_provider_type

    raise SchemaError(f'Undefined provider class: "{provider_cls_name}"')


def _fetch_provider_cls_from_std(provider_cls_name: str) -> Optional[Type[providers.Provider]]:
    return getattr(providers, provider_cls_name, None)


def _import_provider_cls(provider_cls_name: str) -> Optional[Type[providers.Provider]]:
    try:
        cls = _import_string(provider_cls_name)
    except (ImportError, ValueError) as exception:
        raise SchemaError(f'Can not import provider "{provider_cls_name}"') from exception
    except AttributeError:
        return None
    else:
        if isinstance(cls, type) and not issubclass(cls, providers.Provider):
            raise SchemaError(f'Provider class "{cls}" is not a subclass of providers base class')
        return cls


def _import_string(string_name: str) -> Optional[object]:
    segments = string_name.split('.')
    module_name = '.'.join(segments[:-1])
    member = segments[-1]
    module = importlib.import_module(module_name)
    return getattr(module, member, None)


class SchemaError(Exception):
    """Schema-related error."""
