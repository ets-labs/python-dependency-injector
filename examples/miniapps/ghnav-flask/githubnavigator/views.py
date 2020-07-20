"""Views module."""

from flask import request, render_template

from .services import SearchService


def index(
        search_service: SearchService,
        default_query: str,
        default_limit: int,
):
    query = request.args.get('query', default_query)
    limit = request.args.get('limit', default_limit, int)

    repositories = search_service.search_repositories(query, limit)

    return render_template(
        'index.html',
        query=query,
        limit=limit,
        repositories=repositories,
    )
