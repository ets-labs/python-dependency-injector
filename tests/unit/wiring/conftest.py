"""Build Cython test fixtures at session start.

The wiring test suite includes regression coverage for Cython-compiled user
modules (see tests/unit/wiring/test_cython.py). This conftest compiles the
.pyx fixture into a .so before test collection so the import succeeds.

If Cython or a C toolchain is unavailable, the build is skipped silently
and the cython test module raises pytest.importorskip at collection.
"""

import logging
import sysconfig
from pathlib import Path

_LOG = logging.getLogger(__name__)

_FIXTURE_DIR = (
    Path(__file__).resolve().parent.parent / "samples" / "wiringcython"
)
_PYX = _FIXTURE_DIR / "cythonmodule.pyx"


def _ext_suffix() -> str:
    return sysconfig.get_config_var("EXT_SUFFIX") or ".so"


def _fixture_so_path() -> Path:
    """Exact .so path the build produces under the current interpreter.

    Includes the ABI tag (e.g. ``.cpython-313-x86_64-linux-gnu.so``) so a
    stray .so built against a different Python / platform is treated as a
    miss instead of skipping the build silently on cross-ABI CI runs.
    """
    return _FIXTURE_DIR / f"cythonmodule{_ext_suffix()}"


def _fixture_already_built() -> bool:
    so_path = _fixture_so_path()
    if not so_path.exists():
        return False
    return so_path.stat().st_mtime >= _PYX.stat().st_mtime


def _build_fixture() -> bool:
    if not _PYX.exists():
        return False
    if _fixture_already_built():
        return True
    try:
        from Cython.Build import cythonize
        from setuptools import Extension
        from setuptools.command.build_ext import build_ext
        from setuptools.dist import Distribution
    except ImportError as exc:
        _LOG.info("Cython fixture build skipped (missing dep): %s", exc)
        return False

    # Bare module name (no dots) means setuptools writes the .so directly
    # to ``<build_lib>/cythonmodule<EXT_SUFFIX>`` — no package-layout
    # subdir is created. With ``build_lib`` pointed at the fixture dir,
    # the .so lands next to the .pyx where
    # ``from samples.wiringcython.cythonmodule import ...`` resolves via
    # the ``tests/unit/conftest.py`` ``sys.path`` insertion.
    #
    # ``inplace`` MUST be 0 here: ``inplace=1`` ignores ``build_lib`` and
    # writes next to the source tree relative to CWD, which on a clean
    # checkout drops the .so at the repo root.
    ext = Extension(
        "cythonmodule",
        sources=[str(_PYX)],
    )
    ext_modules = cythonize(
        [ext],
        compiler_directives={
            "language_level": 3,
            "binding": True,
            "embedsignature": True,
            "annotation_typing": False,
        },
        quiet=True,
    )
    dist = Distribution(
        {"name": "wiringcython_fixture", "ext_modules": ext_modules}
    )
    cmd = build_ext(dist)
    cmd.inplace = 0
    cmd.build_lib = str(_FIXTURE_DIR)
    cmd.build_temp = str(_FIXTURE_DIR / "_build")
    cmd.ensure_finalized()
    try:
        cmd.run()
    except Exception as exc:  # noqa: BLE001 — surface every build failure mode
        _LOG.warning("Cython fixture build failed: %s", exc)
        return False

    # Positive post-condition — the .so must be where the test importer
    # will look. If setuptools silently changed layout under us, fail
    # loud here instead of letting test_cython.py skip on importorskip.
    so_path = _fixture_so_path()
    if not so_path.exists():
        _LOG.warning(
            "Cython fixture build completed but expected .so missing at %s",
            so_path,
        )
        return False
    return True


def pytest_configure(config):
    """Compile cythonmodule.pyx so test_cython.py can import the .so."""
    _build_fixture()
