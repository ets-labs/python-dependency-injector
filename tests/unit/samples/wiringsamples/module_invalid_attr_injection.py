"""Test module for wiring with invalid type of marker for attribute injection."""

from dependency_injector.wiring import Closing

from .container import Container


service = Closing[Container.service]
