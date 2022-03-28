"""Test module for wiring."""

import sys

if "pypy" not in sys.version.lower():
    import numpy  # noqa
    from numpy import *  # noqa
    if sys.version_info >= (3, 7):
        from numpy.typing import *  # noqa

    import scipy  # noqa
    from scipy import *  # noqa

    import builtins  # noqa
    from builtins import *  # noqa
