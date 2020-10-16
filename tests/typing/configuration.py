from pathlib import Path
from dependency_injector import providers


# Test 1: to check the getattr
config1 = providers.Configuration()
provider1 = providers.Factory(dict, a=config1.a)

# Test 2: to check the from_*() method
config2 = providers.Configuration()
config2.from_dict({})
config2.from_ini('config.ini')
config2.from_ini(Path('config.ini'))

config2.from_yaml('config.yml')
config2.from_yaml(Path('config.yml'))
config2.from_env('ENV', 'default')

# Test 3: to check as_*() methods
config3 = providers.Configuration()
int3: providers.Callable[int] = config3.option.as_int()
float3: providers.Callable[float] = config3.option.as_float()
int3_custom: providers.Callable[int] = config3.option.as_(int)
