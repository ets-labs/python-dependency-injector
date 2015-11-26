"""Example web views."""


class BaseWebView(object):
    """Example base class of web view."""

    def __init__(self, services):
        """Initializer.

        :param services: Bundle of service providers
        :type services: catalogs.Services
        """
        self.services = services


class Auth(BaseWebView):
    """Example auth web view."""


class Photos(BaseWebView):
    """Example photo processing web view."""
