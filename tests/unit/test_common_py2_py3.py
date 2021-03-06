"""Dependency injector common unit tests."""

import unittest

from dependency_injector import __version__


class VersionTest(unittest.TestCase):

    def test_version_follows_semantic_versioning(self):
        self.assertEqual(len(__version__.split('.')), 3)
