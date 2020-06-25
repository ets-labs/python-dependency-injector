"""`Configuration` provider values loading example."""

from dependency_injector import providers


config = providers.Configuration()

config.from_ini('examples/providers/configuration/config.ini')

assert config() == {'aws': {'access_key_id': 'KEY', 'secret_access_key': 'SECRET'}}
assert config.aws() == {'access_key_id': 'KEY', 'secret_access_key': 'SECRET'}
assert config.aws.access_key_id() == 'KEY'
assert config.aws.secret_access_key() == 'SECRET'
