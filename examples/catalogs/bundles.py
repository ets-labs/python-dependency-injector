"""Catalog bundles example."""

import dependency_injector as di


# Declaring example services catalog:
class Services(di.AbstractCatalog):
    """Example catalog of service providers."""

    users = di.Provider()

    auth = di.Provider()

    photos = di.Provider()


# Declaring example base class for some web views:
class BaseWebView(object):
    """Example base class of web view."""

    def __init__(self, services):
        """Initializer.

        :type services: Services
        :param services: Bundle of service providers
        """
        self.services = services


# Declaring several example web views:
class AuthView(BaseWebView):
    """Example auth web view."""


class PhotosView(BaseWebView):
    """Example photo processing web view."""

# Creating example views with appropriate service provider bundles:
auth_view = AuthView(Services.Bundle(Services.users,
                                     Services.auth))
photos_view = PhotosView(Services.Bundle(Services.users,
                                         Services.photos))

# Making some asserts:
assert auth_view.services.users is Services.users
assert auth_view.services.auth is Services.auth
try:
    auth_view.services.photos
except di.Error:
    # `photos` service provider is not in scope of `auth_view` services bundle,
    # so `di.Error` will be raised.
    pass

assert photos_view.services.users is Services.users
assert photos_view.services.photos is Services.photos
try:
    photos_view.services.auth
except di.Error as exception:
    # `auth` service provider is not in scope of `photo_processing_view`
    # services bundle, so `di.Error` will be raised.
    pass
