"""`Configuration` provider values loading example."""

import os

from dependency_injector import providers


# Emulate environment variables
os.environ['AWS_ACCESS_KEY_ID'] = 'KEY'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'SECRET'


config = providers.Configuration()

config.aws.access_key_id.from_env('AWS_ACCESS_KEY_ID')
config.aws.secret_access_key.from_env('AWS_SECRET_ACCESS_KEY')
config.optional.from_env('UNDEFINED', 'default_value')

assert config.aws.access_key_id() == 'KEY'
assert config.aws.secret_access_key() == 'SECRET'
assert config.optional() == 'default_value'
