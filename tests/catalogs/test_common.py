"""Dependency injector common catalogs unittests."""

import unittest2 as unittest


class CatalogModuleBackwardCompatibility(unittest.TestCase):
    """Backward compatibility test of catalog module."""

    def test_import_catalog(self):
        """Test that module `catalog` is the same as `catalogs`."""
        from dependency_injector import catalog
        from dependency_injector import catalogs

        self.assertIs(catalog, catalogs)
