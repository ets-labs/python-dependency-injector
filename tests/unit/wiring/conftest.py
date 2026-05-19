"""Enable on-import compilation of the .pyx wiring fixture via pyximport.

Cython is not installed in every tox env (e.g. pydantic-{v1,v2}), so the
import is guarded — test_cython.py skips at importorskip in that case.
"""

try:
    import pyximport

    pyximport.install(language_level=3)
except ImportError:
    pass
