from .knot import KnotConnection
from .evt_flag import *
import logging as _logging
import sys as _sys
import os as _os
__flag_list = [
	'FLAG_TIME',
	'FLAG_LOWER',
	'FLAG_UPPER',
	'FLAG_CHANGE',
	'FLAG_MAX'
]
__all__ = ['KnotConnection'] +__flag_list
__version__ = 1.0
if _os.environ.get('DEBUG'):
	_logging.basicConfig(format='KNOT_DEBUG: %(message)s', stream=_sys.stderr, level=_logging.INFO)
