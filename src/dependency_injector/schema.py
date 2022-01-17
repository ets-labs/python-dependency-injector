"""Schema module."""

import builtins
import importlib
from typing import Dict, Any, Type, Optional

from . import containers, providers


ContainerSchema = Dict[Any, Any]
ProviderSchema = Dict[Any, Any]


class SchemaProcessorV1:

    def __init__(self, schema: ContainerSchema) -> None:
        self._schema = schema
        self._container = containers.DynamicContainer()

    def process(self):
        """Process schema."""
        self._create_providers(self._schema["container"])
        self._setup_injections(self._schema["container"])

    def get_providers(self):
        """Return providers."""
        return self._container.providers

    def _create_providers(
            self,
            provider_schema: ProviderSchema,
            container: Optional[containers.Container] = None,
    ) -> None:
        if container is None:
            container = self._container
        for provider_name, data in provider_schema.items():
            provider = None

            if "provider" in data:
                provider_type = _get_provider_cls(data["provider"])
                args = []

                # provides = data.get("provides")
                # if provides:
                #     provides = _import_string(provides)
                #     if provides:
                #         args.append(provides)

                provider = provider_type(*args)

            if provider is None:
                provider = providers.Container(containers.DynamicContainer)

            container.set_provider(provider_name, provider)

            if isinstance(provider, providers.Container):
                self._create_providers(provider_schema=data, container=provider)

    def _setup_injections(  # noqa: C901
            self,
            provider_schema: ProviderSchema,
            container: Optional[containers.Container] = None,
    ) -> None:
        if container is None:
            container = self._container

        for provider_name, data in provider_schema.items():
            provider = getattr(container, provider_name)
            args = []
            kwargs = {}

            provides = data.get("provides")
            if provides:
                if isinstance(provides, str) and provides.startswith("container."):
                    provides = self._resolve_provider(provides[len("container."):])
                else:
                    provides = _import_string(provides)
                provider.set_provides(provides)

            arg_injections = data.get("args")
            if arg_injections:
                for arg in arg_injections:
                    injection = None

                    if isinstance(arg, str) and arg.startswith("container."):
                        injection = self._resolve_provider(arg[len("container."):])

                    # TODO: refactoring
                    if isinstance(arg, dict):
                        provider_args = []
                        provider_type = _get_provider_cls(arg.get("provider"))
                        provides = arg.get("provides")
                        if provides:
                            if isinstance(provides, str) and provides.startswith("container."):
                                provides = self._resolve_provider(provides[len("container."):])
                            else:
                                provides = _import_string(provides)
                            provider_args.append(provides)
                        for provider_arg in arg.get("args", []):
                            if isinstance(provider_arg, str) \
                                    and provider_arg.startswith("container."):
                                provider_args.append(
                                    self._resolve_provider(provider_arg[len("container."):]),
                                )
                        injection = provider_type(*provider_args)

                    if not injection:
                        injection = arg

                    args.append(injection)
            if args:
                provider.add_args(*args)

            kwarg_injections = data.get("kwargs")
            if kwarg_injections:
                for name, arg in kwarg_injections.items():
                    injection = None

                    if isinstance(arg, str) and arg.startswith("container."):
                        injection = self._resolve_provider(arg[len("container."):])

                    # TODO: refactoring
                    if isinstance(arg, dict):
                        provider_args = []
                        provider_type = _get_provider_cls(arg.get("provider"))
                        provides = arg.get("provides")
                        if provides:
                            if isinstance(provides, str) and provides.startswith("container."):
                                provides = self._resolve_provider(provides[len("container."):])
                            else:
                                provides = _import_string(provides)
                            provider_args.append(provides)
                        for provider_arg in arg.get("args", []):
                            if isinstance(provider_arg, str) \
                                    and provider_arg.startswith("container."):
                                provider_args.append(
                                    self._resolve_provider(provider_arg[len("container."):]),
                                )
                        injection = provider_type(*provider_args)

                    if not injection:
                        injection = arg

                    kwargs[name] = injection
            if kwargs:
                provider.add_kwargs(**kwargs)

            if isinstance(provider, providers.Container):
                self._setup_injections(provider_schema=data, container=provider)

    def _resolve_provider(self, name: str) -> Optional[providers.Provider]:
        segments = name.split(".")
        try:
            provider = getattr(self._container, segments[0])
        except AttributeError:
            return None

        for segment in segments[1:]:
            parentheses = ""
            if "(" in segment and ")" in segment:
                parentheses = segment[segment.find("("):segment.rfind(")")+1]
                segment = segment.replace(parentheses, "")

            try:
                provider = getattr(provider, segment)
            except AttributeError:
                # TODO
                return None

            if parentheses:
                # TODO
                provider = provider()

        return provider


def build_schema(schema: ContainerSchema) -> Dict[str, providers.Provider]:
    """Build provider schema."""
    schema_processor = SchemaProcessorV1(schema)
    schema_processor.process()
    return schema_processor.get_providers()


def _get_provider_cls(provider_cls_name: str) -> Type[providers.Provider]:
    std_provider_type = _fetch_provider_cls_from_std(provider_cls_name)
    if std_provider_type:
        return std_provider_type

    custom_provider_type = _import_provider_cls(provider_cls_name)
    if custom_provider_type:
        return custom_provider_type

    raise SchemaError(f"Undefined provider class \"{provider_cls_name}\"")


def _fetch_provider_cls_from_std(provider_cls_name: str) -> Optional[Type[providers.Provider]]:
    return getattr(providers, provider_cls_name, None)


def _import_provider_cls(provider_cls_name: str) -> Optional[Type[providers.Provider]]:
    try:
        cls = _import_string(provider_cls_name)
    except (ImportError, ValueError) as exception:
        raise SchemaError(f"Can not import provider \"{provider_cls_name}\"") from exception
    except AttributeError:
        return None
    else:
        if isinstance(cls, type) and not issubclass(cls, providers.Provider):
            raise SchemaError(f"Provider class \"{cls}\" is not a subclass of providers base class")
        return cls


def _import_string(string_name: str) -> Optional[object]:
    segments = string_name.split(".")

    if len(segments) == 1:
        member = getattr(builtins, segments[0], None)
        if member:
            return member

    module_name = ".".join(segments[:-1])
    if not module_name:
        return None

    member = segments[-1]
    module = importlib.import_module(module_name)
    return getattr(module, member, None)


class SchemaError(Exception):
    """Schema-related error."""
