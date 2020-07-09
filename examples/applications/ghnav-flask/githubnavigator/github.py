"""Github API module."""

import requests


class GitHubApiClient:
    """GitHub API client performs operations with Github API."""

    API_URL = 'https://api.github.com/'
    DEFAULT_LIMIT = 5

    def __init__(self, auth_token, request_timeout):
        """Initialize search."""
        self._auth_token = auth_token
        self._request_timeout = request_timeout

    def search_repositories(self, search_term, limit):
        """Search repositories."""
        if not search_term:
            return []

        repositories = self._make_search('repositories', search_term, limit)
        latest_commits = [
            self._get_latest_commit(repository, search_term)
            for repository in repositories
        ]
        return list(zip(repositories, latest_commits))

    def _make_search(self, entity, search_term, limit):
        headers = {}
        if self._auth_token:
            headers['authorization'] = f'token {self._auth_token}'

        response = requests.get(
            url=f'{self.API_URL}search/{entity}',
            params={
                'q': f'{search_term} in:name',
                'sort': 'updated',
                'order': 'desc',
                'page': 1,
                'per_page': limit,
            },
            headers=headers,
            timeout=self._request_timeout,
        )
        data = response.json()
        return data['items']

    def _get_latest_commit(self, repository, search_term):
        headers = {}
        if self._auth_token:
            headers['authorization'] = f'token {self._auth_token}'

        response = requests.get(
            url=repository['commits_url'].replace('{/sha}', ''),
            params={
                'q': f'{search_term} in:name',
                'sort': 'updated',
                'order': 'desc',
                'page': 1,
                'per_page': 1,
            },
            headers=headers,
            timeout=self._request_timeout,
        )
        data = response.json()
        return data[0]
