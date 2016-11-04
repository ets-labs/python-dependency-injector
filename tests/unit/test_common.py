"""Dependency injector common unit tests."""

import unittest2 as unittest

from dependency_injector import VERSION


class VersionTest(unittest.TestCase):

    def test_version_follows_semantic_versioning(self):
        self.assertEquals(len(VERSION.split('.')), 3)
