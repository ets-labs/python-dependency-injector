"""`Configuration` provider values loading example."""

from dependency_injector import providers


config = providers.Configuration()

config.from_yaml('examples/providers/configuration/config.yml')
config.from_yaml('examples/providers/configuration/config.local.yml')

assert config() == {'aws': {'access_key_id': 'LOCAL-KEY', 'secret_access_key': 'LOCAL-SECRET'}}
assert config.aws() == {'access_key_id': 'LOCAL-KEY', 'secret_access_key': 'LOCAL-SECRET'}
assert config.aws.access_key_id() == 'LOCAL-KEY'
assert config.aws.secret_access_key() == 'LOCAL-SECRET'
