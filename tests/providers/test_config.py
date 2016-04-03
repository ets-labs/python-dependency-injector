"""Dependency injector config providers unittests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    utils,
    errors,
)


class ConfigTests(unittest.TestCase):
    """Config test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.initial_data = dict(key='value',
                                 category=dict(setting='setting_value'))
        self.provider = providers.Config(self.initial_data)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(utils.is_provider(self.provider))

    def test_init_without_initial_value(self):
        """Test provider's creation with no initial value."""
        self.assertEqual(providers.Config()(), dict())

    def test_call(self):
        """Test returning of config value."""
        self.assertEqual(self.provider(), self.initial_data)

    def test_update_from(self):
        """Test update of config value."""
        self.assertEqual(self.provider(), self.initial_data)

        self.initial_data['key'] = 'other_value'
        self.provider.update_from(self.initial_data)
        self.assertEqual(self.provider(), self.initial_data)

    def test_call_child(self):
        """Test returning of child config values."""
        category = self.provider.category
        category_setting = self.provider.category.setting

        self.assertTrue(utils.is_provider(category))
        self.assertTrue(utils.is_provider(category_setting))

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_and_update_from(self):
        """Test returning of deferred child config values."""
        self.provider = providers.Config()
        category = self.provider.category
        category_setting = self.provider.category.setting

        self.assertTrue(utils.is_provider(category))
        self.assertTrue(utils.is_provider(category_setting))

        self.provider.update_from(self.initial_data)

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_with_empty_value(self):
        """Test returning of deferred child config values."""
        self.provider = providers.Config()
        category_setting = self.provider.category.setting
        self.assertRaises(errors.Error, category_setting)

    def test_repr(self):
        """Test representation of provider."""
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.config.'
                         'Config({0}) at {1}>'.format(
                             repr(self.initial_data),
                             hex(id(self.provider))))

        category_setting = self.provider.category.setting
        self.assertEqual(repr(category_setting),
                         '<dependency_injector.providers.config.'
                         'ChildConfig({0}) at {1}>'.format(
                             repr('.'.join(('category', 'setting'))),
                             hex(id(category_setting))))
