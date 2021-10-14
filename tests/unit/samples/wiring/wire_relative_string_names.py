"""Wiring sample package."""


def wire_with_relative_string_names(container):
    container.wire(
        modules=[".module"],
        packages=[".package"],
    )
