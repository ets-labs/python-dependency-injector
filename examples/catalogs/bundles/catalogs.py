"""Catalog bundles example."""

from dependency_injector import catalogs
from dependency_injector import providers
from dependency_injector import errors

import services
import views


# Declaring services catalog:
class Services(catalogs.DeclarativeCatalog):
    """Example catalog of service providers."""

    users = providers.Factory(services.Users)
    """:type: providers.Provider -> services.Users"""

    auth = providers.Factory(services.Auth)
    """:type: providers.Provider -> services.Auth"""

    photos = providers.Factory(services.Photos)
    """:type: providers.Provider -> services.Photos"""


# Declaring views catalog:
class Views(catalogs.DeclarativeCatalog):
    """Example catalog of web views."""

    auth = providers.Factory(views.Auth,
                             services=Services.Bundle(Services.users,
                                                      Services.auth))
    """:type: providers.Provider -> views.Auth"""

    photos = providers.Factory(views.Photos,
                               services=Services.Bundle(Services.users,
                                                        Services.photos))
    """:type: providers.Provider -> views.Photos"""


# Creating example views:
auth_view = Views.auth()
photos_view = Views.photos()

print auth_view.services    # prints: <__main__.Services.Bundle(users, auth)>
print photos_view.services  # prints <__main__.Services.Bundle(photos, users)>

# Making some asserts:
assert auth_view.services.users is Services.users
assert auth_view.services.auth is Services.auth
try:
    auth_view.services.photos
except errors.Error:
    # `photos` service provider is not in scope of `auth_view` services bundle,
    # so `di.Error` will be raised.
    pass

assert photos_view.services.users is Services.users
assert photos_view.services.photos is Services.photos
try:
    photos_view.services.auth
except errors.Error as exception:
    # `auth` service provider is not in scope of `photo_processing_view`
    # services bundle, so `di.Error` will be raised.
    pass
