from knotpy import *
from credentials import *

knot = KnotConnection(credentials, protocol='http')
try:
	devices = knot.myDevices()
	print('Getting mydevices')
	for i,dev in enumerate(devices):
			print('Device:'+ str(i))
			print(dev.get('name'))
			print(dev.get('type'))
			print(dev.get('uuid'))
			print(dev.get('id'))
			print(dev.get('online'))
			print(''),
			knot.unregisterDevice(dev['id'])
except Exception as err:
	print('[ERR]: '+str(err))
