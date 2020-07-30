"""Application containers module."""

from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp

from aiohttp import web
from . import giphy, services, views


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    app = aiohttp.Application(web.Application)

    config = providers.Configuration()

    giphy_client = providers.Factory(
        giphy.GiphyClient,
        api_key=config.giphy.api_key,
        timeout=config.giphy.request_timeout,
    )

    search_service = providers.Factory(
        services.SearchService,
        giphy_client=giphy_client,
    )

    index_view = aiohttp.View(
        views.index,
        search_service=search_service,
        default_query=config.search.default_query,
        default_limit=config.search.default_limit,
    )
