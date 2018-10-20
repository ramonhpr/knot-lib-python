from knotpy import *
from credentials import *

knot = KnotConnection(credentials, protocol='http')
try:
	thing_uuid = '113'
	knot.postData(thing_uuid, {'test': 'mydata'})
	datas = knot.getData(thing_uuid)
	for data in datas:
		print(data)
except Exception as err:
	print('[ERR]: '+str(err))
