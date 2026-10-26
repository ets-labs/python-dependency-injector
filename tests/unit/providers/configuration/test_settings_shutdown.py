"""Imported settings classes must participate in interpreter cleanup."""

import subprocess
import sys
import textwrap

import pytest


@pytest.mark.pydantic
def test_settings_released_after_exit_callbacks():
    result = subprocess.run(
        [
            sys.executable,
            "-u",
            "-c",
            textwrap.dedent(
                """
                import atexit
                import os

                def check_provider():
                    config.from_pydantic(Settings(value=43))
                    assert config.value() == 43
                    print("EXIT_CALLBACK_OK")

                atexit.register(check_provider)
                from dependency_injector import providers
                try:
                    from pydantic_settings import BaseSettings
                except ImportError:
                    from pydantic import BaseSettings

                class Marker:
                    def __del__(self, write=os.write):
                        write(1, b"SETTINGS_RELEASED\\n")

                BaseSettings.shutdown_test_marker = Marker()

                class Settings(BaseSettings):
                    value: int = 42

                config = providers.Configuration()
                config.from_pydantic(Settings)
                assert config.value() == 42
                atexit.register(check_provider)
                """
            ),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    assert result.stdout.splitlines() == [
        "EXIT_CALLBACK_OK",
        "EXIT_CALLBACK_OK",
        "SETTINGS_RELEASED",
    ]
    assert result.stderr == ""
