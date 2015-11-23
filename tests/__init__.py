"""Dependency injector unittests."""

import unittest2 as unittest

from dependency_injector import VERSION


class VersionTest(unittest.TestCase):
    """Version constant tests."""

    def test_version_follows_semantic_versioning(self):
        """Test that version follows semantic versioning."""
        self.assertEquals(len(VERSION.split('.')))
