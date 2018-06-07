'''KNoT - Network of things

This API can access the meshblu and find data about KNoT devices
by a simple client connection.

KNoT can now support two protocol to get data from things:
	- http
	- socketio

In KNoT webui you can find your credentials
See an example:
> from knotpy import KnotConnection
> credentials = {
	'servername': '<your_local_IP>/<raspberry_IP>',
	'port': 3000,
	'uuid': <user_uuid>,
	'token': <user_token>
}
> conn = KnotConnection('http', credentials)
> myThings = conn.getThings()

`myThings` is an array with the things that is online and offline in your gateway
This things have informations like your id, if they are online or no, and the
sensors of this things.
'''
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
__version__ = 1.1
if _os.environ.get('DEBUG'):
	_logging.basicConfig(format='KNOT_DEBUG: %(message)s', stream=_sys.stderr, level=_logging.INFO)
