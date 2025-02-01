"""`Dependency injector` setup script."""

import os

from Cython.Build import cythonize
from Cython.Compiler import Options
from setuptools import Extension, setup

debug = os.environ.get("DEPENDENCY_INJECTOR_DEBUG_MODE") == "1"
defined_macros = []
compiler_directives = {
    "language_level": 3,
    "profile": debug,
    "linetrace": debug,
}
Options.annotate = debug

# Adding debug options:
if debug:
    defined_macros.extend(
        [
            ("CYTHON_TRACE", "1"),
            ("CYTHON_TRACE_NOGIL", "1"),
            ("CYTHON_CLINE_IN_TRACEBACK", "1"),
        ]
    )


setup(
    ext_modules=cythonize(
        [
            Extension(
                "*",
                ["src/**/*.pyx"],
                define_macros=defined_macros,
            ),
        ],
        annotate=debug,
        show_all_warnings=True,
        compiler_directives=compiler_directives,
    ),
)
