"""Enable on-import compilation of the .pyx wiring fixture via pyximport."""

import pyximport

pyximport.install(language_level=3)
