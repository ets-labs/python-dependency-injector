from pathlib import Path
from typing import Any, Dict
from typing_extensions import assert_type

from pydantic_settings import BaseSettings as PydanticSettings

from dependency_injector import providers

# Test 1: to check the getattr
config1 = providers.Configuration()
provider1 = providers.Factory(dict[str, Any], a=config1.a)
assert_type(provider1, providers.Factory[Dict[str, Any]])

# Test 2: to check the from_*() method
config2 = providers.Configuration()

config2.from_dict({})
config2.from_value({})

config2.from_ini("config.ini")
config2.from_ini(Path("config.ini"))

config2.from_yaml("config.yml")
config2.from_yaml(Path("config.yml"))

config2.from_json("config.json")
config2.from_json(Path("config.json"))

config2.from_env("ENV", "default")
config2.from_env("ENV", as_=int, default=123)
config2.from_env("ENV", as_=float, required=True)
config2.from_env("ENV", as_=lambda env: str(env))

config2.from_pydantic(PydanticSettings())

# Test 3: to check as_*() methods
config3 = providers.Configuration()
int3 = config3.option.as_int()
float3 = config3.option.as_float()
int3_custom = config3.option.as_(int)

assert_type(int3, providers.TypedConfigurationOption[int])
assert_type(float3, providers.TypedConfigurationOption[float])
assert_type(int3_custom, providers.TypedConfigurationOption[int])

# Test 4: to check required() method
config4 = providers.Configuration()
option4 = config4.option.required()
assert_type(option4, providers.ConfigurationOption)


# Test 5: to check get/set config files' methods and init arguments
# Test 5: ini
config5_ini = providers.Configuration(
    ini_files=["config.ini", Path("config.ini")],
)
config5_ini.set_ini_files(["config.ini", Path("config.ini")])
config5_ini_files = config5_ini.get_ini_files()
assert_type(config5_ini_files, list[str | Path])

# Test 5: yaml
config5_yaml = providers.Configuration(
    yaml_files=["config.yml", Path("config.yml")],
)
config5_yaml.set_yaml_files(["config.yml", Path("config.yml")])
config5_yaml_files: list[str | Path] = config5_yaml.get_yaml_files()
assert_type(config5_yaml_files, list[str | Path])

# Test 5: json
config5_json = providers.Configuration(
    json_files=["config.json", Path("config.json")],
)
config5_json.set_json_files(["config.json", Path("config.json")])
config5_json_files = config5_json.get_json_files()
assert_type(config5_json_files, list[str | Path])

# Test 5: pydantic
config5_pydantic = providers.Configuration(
    pydantic_settings=[PydanticSettings()],
)
config5_pydantic.set_pydantic_settings([PydanticSettings()])

# NOTE: Using assignment since PydanticSettings is context-sensitive: conditional on whether pydantic is installed
config5_pydantic_settings: list[PydanticSettings] = (
    config5_pydantic.get_pydantic_settings()
)

# Test 6: to check init arguments
config6 = providers.Configuration(
    name="config",
    strict=True,
    default={},
)
