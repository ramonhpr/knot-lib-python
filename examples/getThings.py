from knotpy import *
from credentials import *
conn = KnotConnection('socketio', credentials)

myThings = conn.myDevices()

for thing in myThings:
	print(thing)
	print(60*'-')
	print('DATA')
	data = conn.getData(thing['id'], limit=1)
	print(data)
	'''print('Set data')
	if thing.get('schema'):
		for sensor in thing.get('schema'):
			if sensor['name'] == 'LED':
				conn.setData(thing['id'], sensor['sensor_id'], True)
	print(60*'*')'''
