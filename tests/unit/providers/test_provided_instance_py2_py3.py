"""ProvidedInstance provider tests."""

from dependency_injector import containers, providers
from pytest import fixture


class Service:
    def __init__(self, value):
        self.value = value
        self.values = [self.value]

    def __call__(self):
        return self.value

    def __getitem__(self, item):
        return self.values[item]

    def get_value(self):
        return self.value

    def get_closure(self):
        def closure():
            return self.value
        return closure


class Client:
    def __init__(self, value):
        self.value = value


class Container(containers.DeclarativeContainer):

    service = providers.Singleton(Service, value="foo")

    client_attribute = providers.Factory(
        Client,
        value=service.provided.value,
    )

    client_item = providers.Factory(
        Client,
        value=service.provided[0],
    )

    client_attribute_item = providers.Factory(
        Client,
        value=service.provided.values[0],
    )

    client_method_call = providers.Factory(
        Client,
        value=service.provided.get_value.call(),
    )
    client_method_closure_call = providers.Factory(
        Client,
        value=service.provided.get_closure.call().call(),
    )

    client_provided_call = providers.Factory(
        Client,
        value=service.provided.call(),
    )


@fixture
def container():
    return Container()


def test_is_provider(container):
    assert providers.is_provider(container.service.provided) is True


def test_attribute(container):
    client = container.client_attribute()
    assert client.value == "foo"


def test_item(container):
    client = container.client_item()
    assert client.value == "foo"


def test_attribute_item(container):
    client = container.client_attribute_item()
    assert client.value == "foo"


def test_method_call(container):
    client = container.client_method_call()
    assert client.value == "foo"


def test_method_closure_call(container):
    client = container.client_method_closure_call()
    assert client.value == "foo"


def test_provided_call(container):
    client = container.client_provided_call()
    assert client.value == "foo"


def test_call_overridden(container):
    value = "bar"
    with container.service.override(Service(value)):
        assert container.client_attribute().value == value
        assert container.client_item().value == value
        assert container.client_attribute_item().value == value
        assert container.client_method_call().value == value


def test_repr_provided_instance(container):
    provider = container.service.provided
    assert repr(provider) == "ProvidedInstance(\"{0}\")".format(repr(container.service))


def test_repr_attribute_getter(container):
    provider = container.service.provided.value
    assert repr(provider) == "AttributeGetter(\"value\")"


def test_repr_item_getter(container):
    provider = container.service.provided["test-test"]
    assert repr(provider) == "ItemGetter(\"test-test\")"


def test_provided_instance():
    provides = providers.Object(object())
    provider = providers.ProvidedInstance()
    provider.set_provides(provides)
    assert provider.provides is provides
    assert provider.set_provides(providers.Provider()) is provider


def test_attribute_getter():
    provides = providers.Object(object())
    provider = providers.AttributeGetter()
    provider.set_provides(provides)
    provider.set_name("__dict__")
    assert provider.provides is provides
    assert provider.name == "__dict__"
    assert provider.set_provides(providers.Provider()) is provider
    assert provider.set_name("__dict__") is provider


def test_item_getter():
    provides = providers.Object({"foo": "bar"})
    provider = providers.ItemGetter()
    provider.set_provides(provides)
    provider.set_name("foo")
    assert provider.provides is provides
    assert provider.name == "foo"
    assert provider.set_provides(providers.Provider()) is provider
    assert provider.set_name("foo") is provider


def test_method_caller():
    provides = providers.Object(lambda: 42)
    provider = providers.MethodCaller()
    provider.set_provides(provides)
    assert provider.provides is provides
    assert provider() == 42
    assert provider.set_provides(providers.Provider()) is provider


def test_puzzled():
    service = providers.Singleton(Service, value="foo-bar")

    dependency = providers.Object(
        {
            "a": {
                "b": {
                    "c1": 10,
                    "c2": lambda arg: {"arg": arg}
                },
            },
        },
    )

    test_list = providers.List(
        dependency.provided["a"]["b"]["c1"],
        dependency.provided["a"]["b"]["c2"].call(22)["arg"],
        dependency.provided["a"]["b"]["c2"].call(service)["arg"],
        dependency.provided["a"]["b"]["c2"].call(service)["arg"].value,
        dependency.provided["a"]["b"]["c2"].call(service)["arg"].get_value.call(),
    )

    result = test_list()
    assert result == [
        10,
        22,
        service(),
        "foo-bar",
        "foo-bar",
    ]


def test_provided_attribute_in_base_class():
    provider = providers.Provider()
    assert isinstance(provider.provided, providers.ProvidedInstance)
