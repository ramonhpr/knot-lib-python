from knotpy import *
from credentials import *
from base64 import b64encode, b64decode
import string

conn = KnotConnection('socketio', credentials)

myThings = conn.getThings()

for thing in myThings:
	print(thing)
	print(60*'-')
	data = conn.getData(thing['uuid'], limit='*')
	print('DATA', len(data))
	for d in data:
		print filter(lambda x: x in set(string.printable), b64decode(d['data']['value']))
	print 'Setting data ' + b64encode('foo')
	conn.setData(thing['uuid'], 1, b64encode('foo'))

	print(60*'*')
