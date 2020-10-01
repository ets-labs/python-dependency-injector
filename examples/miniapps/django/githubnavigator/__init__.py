"""Main package."""

from .containers import Container


container = Container()
container.config.github.request_timeout.override(5)
container.config.default.query.override('Dependency Injector')
container.config.default.limit.override(5)
