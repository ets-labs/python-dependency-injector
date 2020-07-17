"""Application containers module."""

from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from flask_bootstrap import Bootstrap
from github import Github

from . import views, services


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    app = flask.Application(Flask, __name__)

    bootstrap = flask.Extension(Bootstrap)

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

    index_view = flask.View(
        views.index,
        search_service=search_service,
        default_search_term=config.search.default_term,
        default_search_limit=config.search.default_limit,
    )
