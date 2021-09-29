"""Main module."""

from .containers import Application


if __name__ == "__main__":
    application = Application()
    config = application.service.config()
    config.build()

    print(application.repository.site())
    # Output: Adapter=[DB Path=[~/test]], queue=[Some storage]
