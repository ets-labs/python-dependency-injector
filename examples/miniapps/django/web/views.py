"""Views module."""

from typing import List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dependency_injector.wiring import inject, Provide

from githubnavigator.containers import Container
from githubnavigator.services import SearchService


@inject
def index(
        request: HttpRequest,
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.DEFAULT_QUERY],
        default_limit: int = Provide[Container.config.DEFAULT_LIMIT.as_int()],
        limit_options: List[int] = Provide[Container.config.LIMIT_OPTIONS],
) -> HttpResponse:
    query = request.GET.get("query", default_query)
    limit = int(request.GET.get("limit", default_limit))

    repositories = search_service.search_repositories(query, limit)

    return render(
        request,
        template_name="index.html",
        context={
            "query": query,
            "limit": limit,
            "limit_options": limit_options,
            "repositories": repositories,
        }
    )
