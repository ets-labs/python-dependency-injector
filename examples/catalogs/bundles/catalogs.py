"""Catalog bundles example."""

import dependency_injector as di

import services
import views


# Declaring services catalog:
class Services(di.AbstractCatalog):
    """Example catalog of service providers."""

    users = di.Factory(services.UsersService)
    """:type: di.Provider -> services.UsersService"""

    auth = di.Factory(services.AuthService)
    """:type: di.Provider -> services.AuthService"""

    photos = di.Factory(services.PhotosService)
    """:type: di.Provider -> services.PhotosService"""


# Declaring views catalog:
class Views(di.AbstractCatalog):
    """Example catalog of web views."""

    auth = di.Factory(views.AuthView,
                      services=Services.Bundle(Services.users,
                                               Services.auth))
    """:type: di.Provider -> views.AuthView"""

    photos = di.Factory(views.PhotosView,
                        services=Services.Bundle(Services.users,
                                                 Services.photos))
    """:type: di.Provider -> views.PhotosView"""


# Creating example views:
auth_view = Views.auth()
photos_view = Views.photos()

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
