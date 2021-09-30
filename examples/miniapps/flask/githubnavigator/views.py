"""Views module."""

from flask import request, render_template
from dependency_injector.wiring import inject, Provide

from .services import SearchService
from .containers import Container


@inject
def index(
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.default.query],
        default_limit: int = Provide[Container.config.default.limit.as_int()],
):
    query = request.args.get("query", default_query)
    limit = request.args.get("limit", default_limit, int)

    repositories = search_service.search_repositories(query, limit)

    return render_template(
        "index.html",
        query=query,
        limit=limit,
        repositories=repositories,
    )
