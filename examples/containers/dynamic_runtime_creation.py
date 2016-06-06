"""Creation of dynamic container based on some configuration example."""

import dependency_injector.containers as containers


# Defining several example services:
class UsersService(object):
    """Example users service."""


class AuthService(object):
    """Example auth service."""


def import_cls(cls_name):
    """Import class by its fully qualified name.

    In terms of current example it is just a small helper function. Please,
    don't use it in production approaches.
    """
    path_components = cls_name.split('.')
    module = __import__('.'.join(path_components[:-1]),
                        locals(),
                        globals(),
                        fromlist=path_components[-1:])
    return getattr(module, path_components[-1])


# "Parsing" some configuration:
config = {
    'services': {
        'users': {
            'class': '__main__.UsersService',
            'provider_class': 'dependency_injector.providers.Factory',
        },
        'auth': {
            'class': '__main__.AuthService',
            'provider_class': 'dependency_injector.providers.Factory',
        }
    }
}

# Creating empty container of service providers:
services = containers.DynamicContainer()

# Filling dynamic container with service providers using configuration:
for service_name, service_info in config['services'].iteritems():
    # Runtime importing of service and service provider classes:
    service_cls = import_cls(service_info['class'])
    service_provider_cls = import_cls(service_info['provider_class'])

    # Binding service provider to the dynamic service providers catalog:
    setattr(services, service_name, service_provider_cls(service_cls))

# Creating some objects:
users_service = services.users()
auth_service = services.auth()

# Making some asserts:
assert isinstance(users_service, UsersService)
assert isinstance(auth_service, AuthService)
