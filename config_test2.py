from dependency_injector import containers, providers


def get_value(value):
    return value


class Core(containers.DeclarativeContainer):

    config = providers.Configuration('core')

    value_getter = providers.Callable(get_value, config.value)


class Services(containers.DeclarativeContainer):

    config = providers.Configuration('services')

    value_getter = providers.Callable(get_value, config.value)


root_config = providers.Configuration('main')
sub_config = providers.Configuration('sub')

sub_config.override(root_config.core)

root_config.override(
    {
        'core': {
            'value': 'core',
        },
    },
)

print(sub_config())
print(sub_config.value())
