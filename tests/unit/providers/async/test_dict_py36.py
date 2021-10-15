"""Dict provider async mode tests."""

from dependency_injector import containers, providers
from pytest import mark


@mark.asyncio
async def test_provide():
    async def create_resource(param: str):
        return param

    class Container(containers.DeclarativeContainer):

        resources = providers.Dict(
            foo=providers.Resource(create_resource, "foo"),
            bar=providers.Resource(create_resource, "bar")
        )

    container = Container()
    resources = await container.resources()

    assert resources["foo"] == "foo"
    assert resources["bar"] == "bar"
