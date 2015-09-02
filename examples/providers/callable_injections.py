"""`di.Callable` providers example."""

import passlib.hash
import dependency_injector as di

# Password hasher and verifier providers (hash function could be changed
# anytime (for example, to sha512) without any changes in client's code):
password_hasher = di.Callable(passlib.hash.sha256_crypt.encrypt,
                              salt_size=16,
                              rounds=10000)
password_verifier = di.Callable(passlib.hash.sha256_crypt.verify)

# Making some asserts (client's code):
hashed_password = password_hasher('super secret')
assert password_verifier('super secret', hashed_password)
