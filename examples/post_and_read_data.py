from knotpy import *
from credentials import *

knot = KnotConnection('http',credentials)
try:
	thing_uuid = 'b4db3ef2-b969-4a49-aba1-1577d40f0000'
	knot.postData(thing_uuid, {'test': 'mydata'})
	datas = knot.getData(thing_uuid)
	for data in datas:
		print(data)
except Exception as err:
	print('[ERR]: '+str(err))
