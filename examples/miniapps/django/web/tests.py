"""Tests module."""

from unittest import mock

from django.urls import reverse
from django.test import TestCase
from github import Github

from githubnavigator import container


class IndexTests(TestCase):

    def test_index(self):
        github_client_mock = mock.Mock(spec=Github)
        github_client_mock.search_repositories.return_value = [
            mock.Mock(
                html_url="repo1-url",
                name="repo1-name",
                owner=mock.Mock(
                    login="owner1-login",
                    html_url="owner1-url",
                    avatar_url="owner1-avatar-url",
                ),
                get_commits=mock.Mock(return_value=[mock.Mock()]),
            ),
            mock.Mock(
                html_url="repo2-url",
                name="repo2-name",
                owner=mock.Mock(
                    login="owner2-login",
                    html_url="owner2-url",
                    avatar_url="owner2-avatar-url",
                ),
                get_commits=mock.Mock(return_value=[mock.Mock()]),
            ),
        ]

        with container.github_client.override(github_client_mock):
            response = self.client.get(reverse("index"))

        self.assertContains(response, "Results found: 2")

        self.assertContains(response, "repo1-url")
        self.assertContains(response, "repo1-name")
        self.assertContains(response, "owner1-login")
        self.assertContains(response, "owner1-url")
        self.assertContains(response, "owner1-avatar-url")

        self.assertContains(response, "repo2-url")
        self.assertContains(response, "repo2-name")
        self.assertContains(response, "owner2-login")
        self.assertContains(response, "owner2-url")
        self.assertContains(response, "owner2-avatar-url")

    def test_index_no_results(self):
        github_client_mock = mock.Mock(spec=Github)
        github_client_mock.search_repositories.return_value = []

        with container.github_client.override(github_client_mock):
            response = self.client.get(reverse("index"))

        self.assertContains(response, "Results found: 0")
