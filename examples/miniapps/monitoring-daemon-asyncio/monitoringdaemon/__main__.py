"""Main module."""

from .containers import ApplicationContainer


def main() -> None:
    """Run the application."""
    container = ApplicationContainer()

    container.config.from_yaml('config.yml')
    container.configure_logging()

    dispatcher = container.dispatcher()
    dispatcher.run()


if __name__ == '__main__':
    main()
