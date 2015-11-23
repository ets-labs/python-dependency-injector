"""`Callable` providers with keyword arguments example."""

import passlib.hash

from dependency_injector import providers


# Password hasher and verifier providers (hash function could be changed
# anytime (for example, to sha512) without any changes in client's code):
password_hasher = providers.Callable(passlib.hash.sha256_crypt.encrypt,
                                     salt_size=16,
                                     rounds=10000)
password_verifier = providers.Callable(passlib.hash.sha256_crypt.verify)

# Making some asserts:
hashed_password = password_hasher('super secret')
assert password_verifier('super secret', hashed_password)
