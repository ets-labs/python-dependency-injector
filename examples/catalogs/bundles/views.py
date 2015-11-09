"""Example web views."""


class BaseWebView(object):
    """Example base class of web view."""

    def __init__(self, services):
        """Initializer.

        :type services: catalogs.Services
        :param services: Bundle of service providers
        """
        self.services = services


class AuthView(BaseWebView):
    """Example auth web view."""


class PhotosView(BaseWebView):
    """Example photo processing web view."""
