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
core = Core(config=root_config.core)
services = Services(config=root_config.services)

root_config.override(
    {
        'core': {
            'value': 'core',
        },
        'services': {
            'value': 'services',
        },
    },
)

print(core.value_getter())
print(services.value_getter())

print(core.config(), core.config.value())
print(services.config(), services.config.value())

print(root_config.children)
print(core.config.children)
print(services.config.children)
