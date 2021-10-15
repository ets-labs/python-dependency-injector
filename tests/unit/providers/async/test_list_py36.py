"""List provider async mode tests."""

from dependency_injector import containers, providers
from pytest import mark


@mark.asyncio
async def test_provide():
    # See issue: https://github.com/ets-labs/python-dependency-injector/issues/450
    async def create_resource(param: str):
        return param

    class Container(containers.DeclarativeContainer):

        resources = providers.List(
            providers.Resource(create_resource, "foo"),
            providers.Resource(create_resource, "bar")
        )

    container = Container()
    resources = await container.resources()

    assert resources[0] == "foo"
    assert resources[1] == "bar"
