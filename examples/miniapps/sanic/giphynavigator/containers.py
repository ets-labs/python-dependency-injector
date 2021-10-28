"""Containers module."""

from dependency_injector import containers, providers

from . import giphy, services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    giphy_client = providers.Factory(
        giphy.GiphyClient,
        api_key=config.giphy.api_key,
        timeout=config.giphy.request_timeout,
    )

    search_service = providers.Factory(
        services.SearchService,
        giphy_client=giphy_client,
    )
