"""Complex example of the injecting of provided instance attributes and items."""

from dependency_injector import containers, providers


class Service:

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Container(containers.DeclarativeContainer):

    service = providers.Singleton(Service, value=42)

    dependency = providers.Object(
        {
            "foo": {
                "bar": 10,
                "baz": lambda arg: {"arg": arg}
            },
        },
    )

    demo_list = providers.List(
        dependency.provided["foo"]["bar"],
        dependency.provided["foo"]["baz"].call(22)["arg"],
        dependency.provided["foo"]["baz"].call(service)["arg"],
        dependency.provided["foo"]["baz"].call(service)["arg"].value,
        dependency.provided["foo"]["baz"].call(service)["arg"].get_value.call(),
    )


if __name__ == "__main__":
    container = Container()

    assert container.demo_list() == [
        10,
        22,
        container.service(),
        42,
        42,
    ]
