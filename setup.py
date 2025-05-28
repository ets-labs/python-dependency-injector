"""`Dependency injector` setup script."""

import os
import sys

from Cython.Build import cythonize
from Cython.Compiler import Options
from setuptools import Extension, setup

debug = os.environ.get("DEPENDENCY_INJECTOR_DEBUG_MODE") == "1"
limited_api = (
    os.environ.get("DEPENDENCY_INJECTOR_LIMITED_API") == "1"
    and sys.implementation.name == "cpython"
)
defined_macros = []
options = {}
compiler_directives = {
    "language_level": 3,
    "profile": debug,
    "linetrace": debug,
}
Options.annotate = debug

# Adding debug options:
if debug:
    limited_api = False  # line tracing is not part of the Limited API
    defined_macros.extend(
        [
            ("CYTHON_TRACE", "1"),
            ("CYTHON_TRACE_NOGIL", "1"),
            ("CYTHON_CLINE_IN_TRACEBACK", "1"),
        ]
    )

if limited_api:
    options.setdefault("bdist_wheel", {})
    options["bdist_wheel"]["py_limited_api"] = "cp38"
    defined_macros.append(("Py_LIMITED_API", "0x03080000"))

setup(
    options=options,
    ext_modules=cythonize(
        [
            Extension(
                "*",
                ["src/**/*.pyx"],
                define_macros=defined_macros,
                py_limited_api=limited_api,
            ),
        ],
        annotate=debug,
        show_all_warnings=True,
        compiler_directives=compiler_directives,
    ),
)
