from knot import *
credentials = {
	'uuid': '153c7fb6-1c29-44da-9337-3dcc32260000',
	'token': '2559ce38a12a9c19cdd6787d7b84cd4ddda10531',
	'servername': 'localhost',
	'port': 3000
}

knot = KnotConnection('socketio',credentials)
try:
	devices = knot.getDevices()
	print('Getting devices from gateway')
	for i,dev in enumerate(devices):
			print('Device:'+ str(i))
			print(dev['name'])
			print(dev['type'])
			print(dev['uuid'])
			print(dev['online'])
			print(''),
except Exception as err:
	print('[ERR]: '+str(err))