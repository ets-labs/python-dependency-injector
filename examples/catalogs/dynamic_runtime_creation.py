"""Dynamic catalog creation and runtime filling of it example."""

from dependency_injector import catalogs


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
    if len(path_components) == 1:
        path_components.insert(0, '__main__')
    module = __import__('.'.join(path_components[0:-1]),
                        locals(),
                        globals(),
                        fromlist=path_components[-1:])
    return getattr(module, path_components[-1])


# "Parsing" some configuration:
config = {
    'services': {
        'users': {
            'class': 'UsersService',
            'provider_class': 'dependency_injector.providers.Factory',
        },
        'auth': {
            'class': 'AuthService',
            'provider_class': 'dependency_injector.providers.Factory',
        }
    }
}

# Defining dynamic service providers catalog:
services = catalogs.DynamicCatalog()

# Filling dynamic service providers catalog according to the configuration:
for service_name, service_info in config['services'].iteritems():
    # Runtime importing of service and service provider classes:
    service_cls = import_cls(service_info['class'])
    service_provider_cls = import_cls(service_info['provider_class'])

    # Creating service provider:
    service_provider = service_provider_cls(service_cls)

    # Binding service provider to the dynamic service providers catalog:
    services.bind_provider(service_name, service_provider)

# Creating some objects:
users_service = services.users()
auth_service = services.auth()

# Making some asserts:
assert isinstance(users_service, UsersService)
assert isinstance(auth_service, AuthService)
