from .knot import KnotConnection 
from .evt_flag import EvtFlagsEnum
import logging, sys, os
if os.environ.get('DEBUG'):
	logging.basicConfig(format='KNOT_DEBUG: %(message)s', stream=sys.stderr, level=logging.INFO)
