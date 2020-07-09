"""Application module."""

from dependency_injector import containers, providers

from . import github, views, webapp


class Application(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration()

    github_client = providers.Factory(
        github.GitHubApiClient,
        auth_token=config.github.auth_token,
        request_timeout=config.github.request_timeout,
    )

    index_view = providers.Callable(
        views.index,
        github_client=github_client,
        default_search_term=config.search.default_term,
        default_search_limit=config.search.default_limit,
    )

    app = providers.Factory(
        webapp.create_app,
        name=__name__,
        routes=[
            webapp.Route('/', 'index', index_view, methods=['GET']),
        ],
    )
