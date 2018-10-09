from knotpy import *
from credentials import *
conn = KnotConnection(credentials, protocol='http')

myThings = conn.myDevices()

for thing in myThings:
	print(thing)
	print(60*'-')
	print('DATA')
	# conn.setData(thing['uuid'], 1, True)
	# conn.requestData(thing['uuid'], 1)
#	conn.sendConfig(thing['uuid'], 1, eventFlags=FLAG_CHANGE+FLAG_TIME, timeSec=30)
	# data = conn.getData(thing['uuid'], limit=1)
	# print(data)
	'''print('Set data')
	if thing.get('schema'):
		for sensor in thing.get('schema'):
			if sensor['name'] == 'LED':
				conn.setData(thing['uuid'], sensor['sensor_id'], True)
	print(60*'*')'''
