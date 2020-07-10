"""Application module."""

from dependency_injector import containers, providers
from dependency_injector.ext import flask
from github import Github

from . import services, views


class Application(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration()

    github_client = providers.Factory(
        Github,
        login_or_token=config.github.auth_token,
        timeout=config.github.request_timeout,
    )

    search_service = providers.Factory(
        services.SearchService,
        github_client=github_client,
    )

    index_view = providers.Callable(
        views.index,
        search_service=search_service,
        default_search_term=config.search.default_term,
        default_search_limit=config.search.default_limit,
    )

    app = providers.Factory(
        flask.create_app,
        name=__name__,
        routes=[
            flask.Route('/', view_provider=index_view),
        ],
    )
