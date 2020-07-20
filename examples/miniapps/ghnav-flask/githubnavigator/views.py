"""Views module."""

from flask import request, render_template

from .services import SearchService


def index(search_service: SearchService, default_search_term: str, default_search_limit: int):
    search_term = request.args.get('search_term', default_search_term)
    repositories = search_service.search_repositories(search_term, default_search_limit)

    return render_template(
        'index.html',
        search_term=search_term,
        repositories=repositories,
    )
