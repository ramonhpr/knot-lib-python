from knotpy.meshblu import Meshblu
from credentials import *

knot = Meshblu('http')
try:
	devices = knot.my_devices(credentials)
	print('Getting my_devices')
	for i,dev in enumerate(devices):
			print('Device:'+ str(i))
			print(dev.get('name'))
			print(dev.get('type'))
			print(dev.get('uuid'))
			print(dev.get('id'))
			print(dev.get('online'))
			print(''),
			knot.unregister_device(credentials, dev['id'])
except Exception as err:
	print('[ERR]: '+str(err))
