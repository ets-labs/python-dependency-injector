"""Creation of dynamic container based on the configuration example."""

from dependency_injector import containers, providers


class UserService:
    ...


class AuthService:
    ...


def populate_container(container, providers_config):
    for provider_name, provider_info in providers_config.items():
        provided_cls = globals().get(provider_info["class"])
        provider_cls = getattr(providers, provider_info["provider_class"])
        setattr(container, provider_name, provider_cls(provided_cls))


if __name__ == "__main__":
    services_config = {
        "user": {
            "class": "UserService",
            "provider_class": "Factory",
        },
        "auth": {
            "class": "AuthService",
            "provider_class": "Factory",
        },
    }
    services = containers.DynamicContainer()

    populate_container(services, services_config)

    user_service = services.user()
    auth_service = services.auth()

    assert isinstance(user_service, UserService)
    assert isinstance(auth_service, AuthService)
