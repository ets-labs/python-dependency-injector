"""Test module for wiring with invalid type of marker for attribute injection."""

from dependency_injector.wiring import Closing


service = Closing["service"]
