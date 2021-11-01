"""Main module."""

import sys

from .containers import UseCases, Adapters, TestAdapters


def main(environment: str, email: str) -> None:
    if environment == "prod":
        adapters = Adapters()
    elif environment == "test":
        adapters = TestAdapters()
    else:
        raise RuntimeError("Unknown environment")

    use_cases = UseCases(adapters=adapters)

    use_case = use_cases.signup()
    use_case.execute(email)


if __name__ == "__main__":
    main(*sys.argv[1:])
