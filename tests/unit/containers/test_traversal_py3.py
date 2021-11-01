"""Container traversing tests."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    obj_factory = providers.DelegatedFactory(
        dict,
        foo=providers.Resource(
            dict,
            foo="bar"
        ),
        bar=providers.Resource(
            dict,
            foo="bar"
        )
    )


def test_nested_providers():
    container = Container()
    all_providers = list(container.traverse())

    assert container.obj_factory in all_providers
    assert container.obj_factory.kwargs["foo"] in all_providers
    assert container.obj_factory.kwargs["bar"] in all_providers
    assert len(all_providers) == 3


def test_nested_providers_with_filtering():
    container = Container()
    all_providers = list(container.traverse(types=[providers.Resource]))

    assert container.obj_factory.kwargs["foo"] in all_providers
    assert container.obj_factory.kwargs["bar"] in all_providers
    assert len(all_providers) == 2


def test_container_cls_nested_providers():
    all_providers = list(Container.traverse())

    assert Container.obj_factory in all_providers
    assert Container.obj_factory.kwargs["foo"] in all_providers
    assert Container.obj_factory.kwargs["bar"] in all_providers
    assert len(all_providers) == 3


def test_container_cls_nested_providers_with_filtering():
    all_providers = list(Container.traverse(types=[providers.Resource]))

    assert Container.obj_factory.kwargs["foo"] in all_providers
    assert Container.obj_factory.kwargs["bar"] in all_providers
    assert len(all_providers) == 2
