"""Tests module."""

from unittest.mock import Mock

import main
import api

# Mock ApiClient for testing:
with main.api_client.override(Mock(api.ApiClient)) as api_client_mock:
    user = main.user_factory('test')
    user.register()
    api_client_mock().call.assert_called_with('register', {'id': 'test'})
