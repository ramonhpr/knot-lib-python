from knotpy import *
credentials = {
	'uuid': '533703c2-b60c-45c9-bc6b-1f7301ba0000',
	'token': '6ab7f76b86d1cf6a29f40ff1a1b053dec3e9d24c',
	'servername': 'localhost',
	'port': 3000
}

knot = KnotConnection('socketio',credentials)
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
			knot.unregisterDevice(dev)
except Exception as err:
	print('[ERR]: '+str(err))
