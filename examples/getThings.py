from knotpy import *
from credentials import *
conn = KnotConnection(credentials)

my_things = conn.get_devices()

for thing in my_things:
	print(thing)
	print(60*'-')
	print('DATA')
	# conn.set_data(thing['uuid'], 1, True)
	# conn.requestData(thing['uuid'], 1)
#	conn.send_config(thing['uuid'], 1, eventFlags=FLAG_CHANGE+FLAG_TIME, timeSec=30)
	# data = conn.get_data(thing['uuid'], limit=1)
	# print(data)
	'''print('Set data')
	if thing.get('schema'):
		for sensor in thing.get('schema'):
			if sensor['name'] == 'LED':
				conn.set_data(thing['id'], sensor['sensor_id'], True)
	print(60*'*')'''
