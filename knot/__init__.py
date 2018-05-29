from .knot import KnotConnection 
from .evt_flag import EvtFlagsEnum
import logging as _logging
import sys as _sys
import os as _os
__all__ = ['KnotConnection', 'EvtFlagsEnum']
__version__ = 1.0
if _os.environ.get('DEBUG'):
	_logging.basicConfig(format='KNOT_DEBUG: %(message)s', stream=_sys.stderr, level=_logging.INFO)
