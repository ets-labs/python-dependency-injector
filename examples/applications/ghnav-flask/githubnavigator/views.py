"""Views module."""

from flask import request, render_template

from .github import GitHubApiClient


def index(github_client: GitHubApiClient, default_search_term, default_search_limit):
    search_term = request.args.get('search_term', default_search_term)
    limit = request.args.get('limit', default_search_limit)

    repositories = github_client.search_repositories(search_term, limit)

    return render_template(
        'index.html',
        search_term=search_term,
        limit=limit,
        repositories=repositories,
    )
