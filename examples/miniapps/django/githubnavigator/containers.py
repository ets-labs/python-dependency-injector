"""Containers module."""

from dependency_injector import containers, providers
from github import Github

from . import services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    github_client = providers.Factory(
        Github,
        login_or_token=config.GITHUB_TOKEN,
        timeout=config.GITHUB_REQUEST_TIMEOUT,
    )

    search_service = providers.Factory(
        services.SearchService,
        github_client=github_client,
    )
