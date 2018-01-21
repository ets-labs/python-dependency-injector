"""Run 'Use Cases' example application."""

import sys

from containers import Adapters, TestAdapters, UseCases


if __name__ == '__main__':
    environment, email = sys.argv[1:]

    if environment == 'prod':
        adapters = Adapters()
    elif environment == 'test':
        adapters = TestAdapters()

    use_cases = UseCases(adapters=adapters)

    use_case = use_cases.signup()
    use_case.execute(email)
