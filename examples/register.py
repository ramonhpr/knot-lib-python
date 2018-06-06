from knotpy import *
from credentials import *

knot = KnotConnection('http',credentials)
try:
    device = knot.registerDevice()
    print(device.get('uuid'))
    print(device.get('token'))
except Exception as err:
	print('[ERR]: '+str(err))
