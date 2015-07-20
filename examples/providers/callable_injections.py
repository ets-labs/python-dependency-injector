"""`Callable` providers example."""

from passlib.hash import sha256_crypt

from objects.providers import Callable
from objects.injections import KwArg


# Password hasher and verifier providers (hash function could be changed
# anytime (for example, to sha512) without any changes in client's code):
password_hasher = Callable(sha256_crypt.encrypt,
                           KwArg('salt_size', 16),
                           KwArg('rounds', 10000))
password_verifier = Callable(sha256_crypt.verify)

# Making some asserts (client's code):
hashed_password = password_hasher('super secret')
assert password_verifier('super secret', hashed_password)
