from knotpy import *
from credentials import *
knot = KnotConnection(credentials, protocol='http')
try:
    device = knot.registerDevice({'id':'111'})
    print(device.get('id'))
    print(device.get('uuid'))
    print(device.get('token'))
except Exception as err:
	print('[ERR]: '+str(err))
